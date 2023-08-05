from __future__ import annotations

import logging
import typing as t
from dataclasses import dataclass
from datetime import datetime

from xotless.immutables import ImmutableWrapper

from travertine.i18n import _
from travertine.types import MATCH, RANGE, AttributeLocator, SimpleType, TypeName

from . import ast

try:
    from odoo.models import BaseModel
except ImportError:

    class BaseModel:  # type: ignore
        pass


# fmt: off
class TypeMap(t.Protocol):
    """A type map resolves the name of an attribute to a locator."""
    def __getitem__(self, attr) -> AttributeLocator: ...  # noqa
    def get(self, attr, default=None) -> AttributeLocator: ... # noqa


class TypeMapBuilder(t.Protocol):
    def __call__(self, checker: C) -> TypeMap: ...  # noqa


class TypeMapRegistry(t.Protocol):
    def __getitem__(self, name: str) -> TypeMapBuilder: ...  # noqa
    def __setitem__(self, name: str, builder: TypeMapBuilder) -> None: ...  # noqa
    def __contains__(self, name: str) -> bool: ...  # noqa
# fmt: on


@dataclass
class TypeCheckerResult:
    typechecks: bool
    spec: ast.MatrixSpecification
    errors: t.Sequence[t.Any]

    __slots__ = ("typechecks", "spec", "errors")

    def __post_init__(self):
        self.errors = tuple(self.errors)

    def __bool__(self):
        return self.typechecks

    def __iter__(self):
        yield self.typechecks
        yield self.spec
        yield self.errors

    def raise_if_illtyped(self):
        if not self:
            errs = "\n".join(str(e) for e in self.errors)
            if errs:
                raise ValueError(
                    _(
                        "Could not type-check the given specification.\nErrors:\n{errs}"
                    ).format(errs=errs)
                )
            else:
                raise ValueError(_("Could not type-check the given specification."))


C = t.TypeVar("C", bound="TypeChecker")


class TypeChecker:
    """A base type checker for the matrix."""

    def __init__(self, spec: ast.MatrixSpecification, *, registry: TypeMapRegistry):
        self.errors: t.List[t.Any] = []
        self._result: t.Optional[TypeCheckerResult] = None
        self.spec = ast.MatrixSpecification(spec.columns, spec.data)
        self.spec.meta = spec.meta
        self.typemaps: t.Dict[str, TypeMap] = {}
        self.registry = registry

    @property
    def result(self) -> TypeCheckerResult:
        res = self._result
        if res is None:
            res = self._result = self._perform_typecheck()
        return res

    def _perform_typecheck(self) -> TypeCheckerResult:
        self._check_cells(self.spec)
        self._fill_types(self.spec)
        self._check_rows(self.spec)
        return TypeCheckerResult(not self.errors, self.spec, self.errors)

    def _check_cells(self, spec: ast.MatrixSpecification):
        cols = len(spec.columns)
        for row_index, row in enumerate(spec.data, start=1):
            cells = len(row)
            if cells < cols:
                self._report_error(
                    _("Row {row} has only {cells} cells; expected {cols}").format(
                        cells=cells,
                        row=row_index,
                        cols=cols,
                    ),
                )
            elif cells > cols:
                self._report_error(
                    _("Row {row} has {cells} cells; expected only {cols}").format(
                        cells=cells,
                        row=row_index,
                        cols=cols,
                    ),
                )

    def _fill_types(self, spec: ast.MatrixSpecification):
        """Complete the column specification with the AttributeLocator.

        The AttributeLocator is typed so it has the type information we need.

        We also check if the any explicit 'kind' applies to the type of the
        attribute.

        """
        # The last column is always the price and the parser disallows
        # anything but numbers in the cells of the columns, thus we don't need
        # to type-check it.
        *columns, _price = spec.columns
        for index, column in enumerate(columns, start=1):
            self._fill_column_locator(index, column)
            self._check_column_kind(index, column)

    def _fill_column_locator(self, index: int, column: ast.ColumnSpec):
        """Fill the attribute 'locator' of the column specification.

        The original_spec in the matrix specification is of the form
        'object.attr', we look for a registered type map which corresponds to
        'object' and look for the type of attribute there.  If either the
        'object' is not a registered object or the 'attr' is not a known
        attribute, an error is *reported*.

        """
        if column.locator is not None:
            return
        obj, attr = column._original_spec
        typemap = self._get_type_map(obj)
        if typemap:
            try:
                locator = typemap[attr]
            except KeyError:
                self._report_error(
                    _(
                        "The attribute '{attr}' is not found in the object '{obj}' "
                        "in column {index}"
                    ).format(obj=obj, attr=attr, index=index),
                )
            else:
                column.locator = locator
        else:
            self._report_error(
                _("Unknown object '{obj}' in column {index}").format(
                    obj=obj,
                    index=index,
                ),
            )

    def _get_type_map(self, obj: str):
        """Return the type map for an object."""
        result = self.typemaps.get(obj, None)
        if result is None:
            try:
                builder = get_registered_type_map_builder(self.registry, obj)
            except KeyError:
                return None
            else:
                result = self.typemaps[obj] = builder(self)
        return result

    def _check_column_kind(self, index: int, column: ast.ColumnSpec):
        """Checks if the type of the column matches the kind.

        If the kind is not given explicitly, fill it with the default kind for
        the type.  Number-like types default to RANGE, and other types default
        to MATCH.

        If the given kind doesn't match the type of the attribute, report an
        error.

        """
        if column.locator is not None:
            type_ = column.locator.attr.type.name
            if column.kind is None:
                column.kind = _DEFAULT_KIND_MAP.get(type_, None)
            if column.kind is None:
                self._report_error(
                    _("Cannot get the kind of column '{original_spec}").format(
                        original_spec=column.original_spec
                    ),
                )
            else:
                if column.kind not in _TYPE_ALLOWED_KINDS.get(type_, set([])):
                    self._report_error(
                        _("Invalid kind for the  of column '{original_spec}").format(
                            original_spec=column.original_spec
                        ),
                    )
                    # Unmark the kind so that we can skip cells.
                    column.kind = None

    def _check_rows(self, spec: ast.MatrixSpecification):
        for rowindex, row in enumerate(spec.data, start=1):
            *cells, _price_cell = row
            for cellindex, cell in enumerate(cells, start=1):
                column = spec.columns[cellindex - 1]
                if column.locator and column.kind:
                    kinded = self._check_cell_kind(rowindex, cellindex, column, cell)
                    if kinded:
                        self._check_cell_type(rowindex, cellindex, column, cell)

    def _check_cell_kind(
        self,
        rowindex: int,
        cellindex: int,
        column: ast.ColumnSpec,
        cell: t.Union[ast.RangeCell, ast.ValueCell, ast.FormulaCell],
    ) -> bool:
        if column.kind is RANGE and not isinstance(cell, ast.RangeCell):
            self._report_error(
                _(
                    "Kind mismatch in row {rowindex} at cell {cellindex}. The column {column} "
                    "requires a range but was given something else."
                ).format(
                    rowindex=rowindex,
                    cellindex=cellindex,
                    column=column,
                ),
            )
            return False
        elif column.kind is MATCH and not isinstance(cell, ast.ValueCell):
            self._report_error(
                _(
                    "Kind mismatch in row {rowindex} at cell {cellindex}. The column {column} "
                    "requires a value but was given something else."
                ).format(
                    rowindex=rowindex,
                    cellindex=cellindex,
                    column=column,
                )
            )
            return False
        else:
            return True

    def _check_cell_type(
        self,
        rowindex: int,
        cellindex: int,
        column: ast.ColumnSpec,
        cell: t.Union[ast.RangeCell, ast.ValueCell, ast.FormulaCell],
    ):
        if column.kind is RANGE:
            assert isinstance(cell, ast.RangeCell)
            cell.lower = self._check_value_type(
                rowindex,
                cellindex,
                column,
                value=cell.lower,
                obj=cell,
            )
            cell.upper = self._check_value_type(
                rowindex,
                cellindex,
                column,
                value=cell.upper,
                obj=cell,
            )
            self._check_range_cell(rowindex, cellindex, cell)
        else:
            assert isinstance(cell, ast.ValueCell)
            cell.val = self._check_value_type(
                rowindex,
                cellindex,
                column,
                value=cell.val,
                obj=cell,
            )

    def _check_value_type(
        self,
        rowindex: int,
        cellindex: int,
        column: ast.ColumnSpec,
        value: t.Any,
        obj: ast.AST,
    ):
        assert column.locator is not None
        coltype: SimpleType = column.locator.attr.type
        retvalue = value
        if coltype.name == TypeName.SELECTION:
            try:
                val = coltype.find_value(value)
            except Exception:
                logger.exception("While trying to type-check column %r", column)
                result = False
            else:
                result = val is not None
                retvalue = val
        else:
            result = coltype.typecheck_value(value)
        if not result:
            self._report_error(
                _(
                    "Value {val!r} at {rowindex}, {cellindex} does not match "
                    "expected type for its column."
                ).format(val=value, rowindex=rowindex, cellindex=cellindex),
            )
        if isinstance(retvalue, BaseModel):
            # This achieves two goals: the object is immutable, and pickable
            # as required for procedures.
            return ImmutableWrapper(retvalue)
        return retvalue

    def _check_range_cell(self, rowindex, cellindex, cell: ast.RangeCell) -> None:
        if not cell.lower <= cell.upper:
            self._report_error(
                _(
                    "The range given at row {rowindex}, cell {cellindex} is "
                    "not valid: {lower} - {upper}"
                ).format(
                    rowindex=rowindex,
                    cellindex=cellindex,
                    lower=cell.lower,
                    upper=cell.upper,
                )
            )

    def _report_error(self, msg: str):
        self.errors.append(msg)


class BaseTypeMap:
    """Base class for type maps.

    Type Maps resolve a given attribute name by returning an AttributeLocator.

    """

    def __getitem__(self, attr) -> AttributeLocator:
        raise KeyError(attr)

    def get(self, attr, default=None):
        try:
            return self[attr]
        except KeyError:
            return default


class DemandTypeMap(BaseTypeMap):
    """The type map for the demand"""

    def __getitem__(self, attr) -> AttributeLocator:
        if attr == "date":
            return AttributeLocator.of_demand("date", datetime)
        raise KeyError(attr)


class RequestTypeMap(BaseTypeMap):
    """The type map for the request"""

    def __getitem__(self, attr) -> AttributeLocator:
        if attr == "quantity":
            return AttributeLocator.of_request(attr, float)
        raise KeyError(attr)


class ChainedTypeMap(BaseTypeMap):
    """A type map which simply looks for a match in a list of bases.

    This allows for instance to create a type map for models which have part
    of its attributes defined in an AbstractModel (mixin).  For instance, for
    the name 'commodity' we actually create a chain for models
    'commodity.scheme.mixin', and 'operation.commodity'.

    """

    def __init__(self, *bases: BaseTypeMap) -> None:
        self.bases = bases

    def __getitem__(self, attr_name) -> AttributeLocator:
        Unset: AttributeLocator = object()  # type: ignore
        result = Unset
        bases = list(self.bases)
        while result is Unset and bases:
            base = bases.pop(0)
            result = base.get(attr_name, Unset)
        if result is not Unset:
            return result
        raise KeyError(attr_name)


def register_type_map_builder(
    registry: TypeMapRegistry,
    name: str,
    builder: TypeMapBuilder,
):
    """Registers a type map builder for a given name.

    This registry makes a static relation of names like 'demand', 'request',
    'commodity', 'consumible', etc.  to the builders of type maps we need to
    know the types of attributes.

    Having this registry allows for other addons to register builders for
    their own Odoo models.

    It's an error to register the same name twice.  Names are case-insensitive
    and must be identifiers.

    """
    name = name.lower()
    assert name.isidentifier()
    if name in registry:
        raise DuplicatedNamedError(name)
    registry[name] = builder
    return builder


def get_registered_type_map_builder(
    registry: TypeMapRegistry,
    name: str,
) -> TypeMapBuilder:
    """Gets the registered builder for a given name.

    Raises a KeyError if the name is not registered.

    """
    name = name.lower()
    return registry[name]


class DuplicatedNamedError(ValueError):
    "Error indicating a register a duplicated object name"


# The default kind for a given type.
_DEFAULT_KIND_MAP: t.Mapping[TypeName, t.Union[t.Type[MATCH], t.Type[RANGE]]] = {
    TypeName.INT: RANGE,
    TypeName.FLOAT: RANGE,
    TypeName.STR: MATCH,
    TypeName.SELECTION: MATCH,
    TypeName.DATE: RANGE,
    TypeName.DATETIME: RANGE,
    TypeName.BOOL: MATCH,
    TypeName.TIMEDELTA: RANGE,
}

# The possible kinds for a given type.
_TYPE_ALLOWED_KINDS: t.Mapping[
    TypeName,
    t.AbstractSet[t.Union[t.Type[MATCH], t.Type[RANGE]]],
] = {
    TypeName.INT: {RANGE, MATCH},
    TypeName.FLOAT: {RANGE, MATCH},
    TypeName.STR: {MATCH},
    TypeName.SELECTION: {MATCH},
    TypeName.DATE: {RANGE, MATCH},
    TypeName.DATETIME: {RANGE, MATCH},
    TypeName.BOOL: {MATCH},
    TypeName.TIMEDELTA: {RANGE, MATCH},
}

logger = logging.getLogger(__name__)
