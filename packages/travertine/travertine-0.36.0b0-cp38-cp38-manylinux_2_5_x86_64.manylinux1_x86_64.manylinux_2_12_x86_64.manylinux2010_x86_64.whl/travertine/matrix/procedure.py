#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
"""An implementation of the MatrixProcedure.

This implementation is under 'models/' because we require an Odoo environment
to type-check the specification.

"""
import typing as t

from xotl.tools.context import context

from travertine import Program
from travertine.avm import CascadingAVM, merge_avms
from travertine.i18n import _
from travertine.matrix import MatrixProcedure as TravertineMatrix
from travertine.matrix import MatrixRow
from travertine.procedures import (
    BACK_TRACKING_EXECUTION,
    EMPTY_EVM,
    FormulaProcedure,
    NamedProcedure,
    NoMatchingBranchError,
    UndefinedProcedure,
)
from travertine.structs import PriceResult, _convert_to_runtime_value
from travertine.types import (
    ATTRIBUTE_OWNER,
    AVM,
    EVM,
    MATCH,
    RANGE,
    AttributeLocator,
    Demand,
    Environment,
    PriceResultType,
    Procedure,
    Text,
    Undefined,
)

from . import ast, parser
from .typechecker import TypeCheckerResult


class BaseMatrixProcedure(NamedProcedure):
    """A matrix of prices.

    Price matrices are a simplified form to represent a bunch of conditional
    (backtracking) branches.

    Subclasses MUST implement the method `typecheck`:meth:.

    """

    __slots__ = ("envdata", "title", "spec", "_avm")

    def __init__(self, specification: Text, *, title: str = None):
        self._avm: t.Optional[AVM] = None
        self.title = title or _("Matrix procedure")
        self.spec = spec = parser.parse(specification)
        self.typecheck(spec).raise_if_illtyped()

    def typecheck(self, spec: ast.MatrixSpecification) -> TypeCheckerResult:
        """Type-checks and resolves locators for the matrix specification.

        Subclasses MUST reimplement this method so that columns in the matrix
        specification are fully resolved.

        """
        raise NotImplementedError

    @property
    def env(self):
        return self.envdata.find(ignore_user=True, ignore_context=True)

    def __call__(self, demand: Demand, env: Environment) -> PriceResultType:
        locators: t.List[AttributeLocator] = [
            column.locator for column in self.spec.columns[:-1]  # type: ignore
        ]
        rowindex = 0
        while rowindex < len(self.spec.data):
            row = self.spec.data[rowindex]
            rowindex += 1
            if all(
                cell.match_with_locator(locator, demand)
                for cell, locator in zip(row, locators)
            ):
                pricecol = row[-1]
                if isinstance(pricecol, ast.ValueCell):
                    result = pricecol.val
                elif isinstance(pricecol, ast.FormulaCell):
                    proc = FormulaProcedure(code=pricecol.code)
                    result = proc(demand, env).result
                else:
                    assert False
                    result = Undefined
                return PriceResult(
                    _('Matched row {rowindex} of "{title}"').format(
                        rowindex=rowindex, title=self.title
                    ),
                    self,
                    result,  # type: ignore
                    demand,
                    env,
                )
        # At this point no row matched, so we need to behave as backtracking
        # procedure.
        if context[BACK_TRACKING_EXECUTION]:
            raise NoMatchingBranchError
        else:
            return_undefined = UndefinedProcedure(
                title=_('Undefined because not row matched in "%s"') % self.title
            )
            return return_undefined(demand, env)

    def __len__(self):
        return 1

    @property
    def depth(self):
        return 1

    @property
    def avm(self) -> AVM:
        # The AVM of a matrix should be almost the same as an equivalent graph
        # of branching procedures.  But since, I know the same attribute
        # cannot be given twice in the same matrix FilteringAVM is not needed,
        # only CascadingAVM has a role.
        #
        # For example, in the following specification:
        #
        #     demand.date;                          _
        #     2020-01-01 00:00 - 2020-02-01 00:00;  1
        #     2020-01-01 00:00 - 2020-03-01 00:00;  2
        #     2020-01-01 00:00 - 2020-04-01 00:00;  3
        #
        # each *branch* overlaps with next; if I were to simply merge the
        # intervals the price table would try the first example available
        # (2020-01-01) and would hit the same row each time.
        #
        # Notice, however, that for columns of kind MATCH we can skip the
        # CascadingAVM.
        #
        #     demand.date;                          commodity.occupation;  _
        #     2020-01-01 00:00 - 2020-02-01 00:00;  "SGL";                 1
        #     2020-01-01 00:00 - 2020-03-01 00:00;  "SGL";                 2
        #     2020-01-01 00:00 - 2020-04-01 00:00;  "DBL";                 3
        #
        # The cascade of the second column would return nothing in the second
        # row, but still "SGL" has to be in the AVM because of the first row.
        #
        # So, we can say that the AVM is the simple merge of the AVMs per each
        # column.
        result: t.Optional[AVM] = self._avm
        if result is None:
            result = self._avm = merge_avms(
                self._get_column_avm(index, column)
                for index, column in enumerate(self.spec.columns[:-1])
            )
        assert result is not None
        return result

    def _get_column_avm(self, colindex: int, colspec: ast.ColumnSpec) -> AVM:
        if colspec.kind is RANGE:
            return self._get_range_column_avm(colindex, colspec)
        else:
            assert colspec.kind is MATCH
            return self._get_match_column_avm(colindex, colspec)

    def _get_range_column_avm(self, colindex: int, colspec: ast.ColumnSpec) -> AVM:
        cascade: AVM = {}
        locator = colspec.locator
        assert locator is not None
        avms = []
        for row in self.spec.data:
            current = {locator: (row[colindex].domain,)}
            if not cascade:
                cascade = current
            else:
                # Create a single flat cascade out of all the bases.  This may impact
                # adversely in the _cache (it won't be shared by branches) but cascading
                # is not associative:
                #
                #    CascadingAVM(a1, a2, a3) != CascadingAVM(CascadingAVM(a1, a2), a3)
                #
                # The first is like ``a3 - (a2 | a1)``; whereas the second is
                # a3 - (a2 - a1) -- where '-'  is sets difference operator.
                if isinstance(cascade, CascadingAVM):
                    cascade = CascadingAVM(*cascade.bases, current)
                else:
                    cascade = CascadingAVM(cascade, current)
            avms.append(cascade)
        return merge_avms(avms)

    def _get_match_column_avm(self, colindex: int, colspec: ast.ColumnSpec) -> AVM:
        locator = colspec.locator
        assert locator is not None
        return merge_avms({locator: (row[colindex].domain,)} for row in self.spec.data)

    @property
    def evm(self) -> EVM:
        return EMPTY_EVM

    def __getstate__(self):
        return {"title": self.title, "spec": self.spec}

    def __setstate__(self, state):
        self.title: str = state["title"]
        self.spec: ast.MatrixSpecification = state["spec"]
        self._avm = None

    def __iter__(self) -> t.Iterator[Procedure]:
        return
        yield

    def add_to_travertine_program(self, program: Program):
        matrix = TravertineMatrix()
        for rowdata in self.spec.data:
            *cells, price = rowdata
            row = MatrixRow()
            for colindex, cell in enumerate(cells):
                colspec = self.spec.columns[colindex]
                assert colspec.locator is not None
                if colspec.locator.owner == ATTRIBUTE_OWNER.DEMAND:
                    if colspec.kind is RANGE:
                        assert isinstance(cell, ast.RangeCell)
                        row.add_condition_demand_date_in_range(
                            cell.lower, cell.upper  # type: ignore
                        )
                    else:
                        assert isinstance(cell, ast.ValueCell)
                        row.add_condition_demand_date_is(cell.val)  # type: ignore
                elif colspec.locator.owner == ATTRIBUTE_OWNER.REQUEST:
                    if colspec.kind is RANGE:
                        assert isinstance(cell, ast.RangeCell)
                        row.add_condition_quantity_in_range(cell.lower, cell.upper)  # type: ignore
                    else:
                        assert isinstance(cell, ast.ValueCell)
                        row.add_condition_quantity_is(cell.val)  # type: ignore
                else:
                    assert colspec.locator.owner == ATTRIBUTE_OWNER.COMMODITY
                    if colspec.locator.attr.name == "start_name":
                        if colspec.kind is RANGE:
                            assert isinstance(cell, ast.RangeCell)
                            row.add_condition_start_date_in_range(
                                cell.lower, cell.upper  # type: ignore
                            )
                        else:
                            assert isinstance(cell, ast.ValueCell)
                            row.add_condition_start_date_is(cell.val)  # type: ignore
                    else:
                        if colspec.kind is RANGE:
                            assert isinstance(cell, ast.RangeCell)
                            row.add_condition_attr_in_range(
                                colspec.locator.attr.name,
                                _convert_to_runtime_value(cell.lower),
                                _convert_to_runtime_value(cell.upper),
                            )
                        else:
                            assert isinstance(cell, ast.ValueCell)
                            row.add_condition_attr_is(
                                colspec.locator.attr.name,
                                _convert_to_runtime_value(cell.val),
                            )
            if isinstance(price, ast.ValueCell):
                matrix.add_row(row, price.val)  # type: ignore
            elif isinstance(price, ast.FormulaCell):
                matrix.add_row(row, price.code)
            else:
                assert False
        program.add_matrix_procedure(id(self), matrix)
