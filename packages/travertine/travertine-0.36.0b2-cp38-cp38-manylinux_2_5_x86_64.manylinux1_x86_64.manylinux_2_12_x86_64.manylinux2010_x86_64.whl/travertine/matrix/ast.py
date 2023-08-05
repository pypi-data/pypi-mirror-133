#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence, Tuple, Type, Union

from lark.tree import Meta
from xotless.domains import EquivalenceSet
from xotless.ranges import Range
from xotless.types import Domain, EqTypeClass, OrdTypeClass

from travertine.predicates import MATCH, RANGE
from travertine.types import AttributeLocator, Demand

# NB: We're mixing parsing/compilation features into this module for two main
# reasons:
#
# - it's easier now and we can get a rapid functioning module; and
#
# - more importantly, in Python Land this is more efficient.
#
# This is also the reason why the Lark parser in 'models/' (needs the Odoo
# environment for type-checking) inherit from this classes.


@dataclass
class AST:
    def describe(self) -> str:
        "Return a description of the AST suitable to be presented to the user."
        return str(self)

    meta: Meta = field(init=False, compare=False, hash=False, repr=False)


@dataclass
class MatrixSpecification(AST):
    columns: Sequence[ColumnSpec]
    data: Sequence[Sequence[Union[ValueCell, RangeCell, FormulaCell]]]

    # This is set to True after type-checking.
    typechecked: bool = False


@dataclass
class ColumnSpec(AST):
    # None means that this is the Price column specification.
    locator: Optional[AttributeLocator]

    # This is the original 'owner.attr' that happens in the string of the
    # matrix spec.
    _original_spec: Tuple[str, str]

    # None means the *default* according to the type of the attribute locator.
    kind: Optional[Union[Type[MATCH], Type[RANGE]]]

    @property
    def original_spec(self) -> str:
        return ".".join(self._original_spec)


class Cell:
    def match_with_locator(self, locator: AttributeLocator, demand: Demand) -> bool:
        return False

    @property
    def domain(self) -> Domain:
        return EquivalenceSet(set([]))


@dataclass
class ValueCell(AST, Cell):
    val: EqTypeClass

    def match_with_locator(self, locator: AttributeLocator, demand: Demand) -> bool:
        values = locator.lookup(demand, object())
        return bool(values and all(self.val == value for value in values))

    @property
    def domain(self) -> Domain:
        return EquivalenceSet({self.val})


@dataclass
class FormulaCell(AST, Cell):
    code: str


@dataclass
class RangeCell(AST, Cell):
    lower: OrdTypeClass
    upper: OrdTypeClass

    def match_with_locator(self, locator: AttributeLocator, demand: Demand) -> bool:
        Unset = object()
        values = locator.lookup(demand, Unset)
        if values is not Unset:
            try:
                return bool(
                    values and all(self.lower <= value < self.upper for value in values)
                )
            except TypeError:
                pass
        return False

    @property
    def domain(self) -> Domain:
        return Range.new_open_right(self.lower, self.upper).lift()
