import enum
from datetime import datetime

from travertine.matrix import ast
from travertine.matrix.procedure import BaseMatrixProcedure
from travertine.matrix.typechecker import (
    BaseTypeMap,
    DemandTypeMap,
    RequestTypeMap,
    TypeChecker,
    TypeCheckerResult,
    TypeMapRegistry,
)
from travertine.types import AttributeLocator, SimpleType, TypedAttribute


class MatrixProcedure(BaseMatrixProcedure):
    def typecheck(self, spec: ast.MatrixSpecification) -> TypeCheckerResult:
        """Type-checks and resolves locators for the matrix specification.

        Subclasses MUST reimplement this method so that columns in the matrix
        specification are fully resolved.

        """
        return TestingTypeChecker(spec).result


class TestingTypeChecker(TypeChecker):
    """A really simple type-checker to test the matrix using mock objects.

    This type checker resolves the following columns:

    - ``demand.date`` to datetime.
    - ``request.quantity`` to float.
    - ``commodity.start_date``
    - ``commodity.regimen`` to a selection of 'cp', 'map', 'ai', 'ap'
    - ``commodity.occupation`` to objects SGL, DBL.

    """

    def __init__(self, spec: ast.MatrixSpecification):
        super().__init__(spec, registry=_TYPE_MAP_BUILDERS_REGISTRY)


class CommodityTypeMap(BaseTypeMap):
    def __getitem__(self, name: str) -> AttributeLocator:
        return COLUMN_LOCATOR[name.lower()]


_TYPE_MAP_BUILDERS_REGISTRY: TypeMapRegistry = {
    "demand": lambda _checker: DemandTypeMap(),
    "request": lambda _checker: RequestTypeMap(),
    "commodity": lambda _checker: CommodityTypeMap(),
}


class OCCUPATION(enum.Enum):
    SGL = "SGL"
    DBL = "DBL"
    TPR = "TRP"


class REGIMEN(enum.Enum):
    AI = "ai"
    AP = "ap"
    MAP = "map"
    CP = "cp"


COLUMN_LOCATOR = {
    "start_date": AttributeLocator.of_commodity("start_date", datetime),
    "occupation": AttributeLocator.of_commodity(
        TypedAttribute(
            "occupation",
            SimpleType.from_simple_selection(
                [(name, v.value, None) for name, v in OCCUPATION.__members__.items()]
            ),
        )
    ),
    "regimen": AttributeLocator.of_commodity(
        TypedAttribute(
            "regimen",
            SimpleType.from_simple_selection(
                [(name, v.value, None) for name, v in REGIMEN.__members__.items()]
            ),
        )
    ),
    "travelers_count": AttributeLocator.of_commodity(
        "traverlers_count",
        int,
    ),
}
