import enum
import typing as t
from datetime import datetime

from travertine.matrix import ast
from travertine.matrix.parser import parse
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


class TypecheckerTestMixin:
    TypeChecker = TestingTypeChecker

    def parseSpec(
        self,
        spec: t.Union[str, ast.MatrixSpecification],
    ) -> ast.MatrixSpecification:
        if isinstance(spec, ast.MatrixSpecification):
            return spec
        return parse(spec)

    def assertTypecheckSpec(self, spec: ast.MatrixSpecification, msg=None):
        checker = self.TypeChecker(spec)
        result = checker.result
        err = "\n".join(str(e) for e in result.errors)
        self.assertTrue(  # type: ignore
            result,
            msg=msg or f"The specification fails to type-check with errors:\n{err}",
        )

    def assertTypechecks(self, spec: t.Union[str, ast.MatrixSpecification]):
        self.assertTypecheckSpec(
            self.parseSpec(spec),
            msg=f"The specification '{spec!r}' fails to type-check",
        )

    def assertFailsTypecheck(self, spec: t.Union[str, ast.MatrixSpecification], msg=None):
        checker = TestingTypeChecker(self.parseSpec(spec))
        result = checker.result
        self.assertFalse(  # type: ignore
            result,
            msg=msg or f"The specification '{spec!r}' should have failed type-checking",
        )


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
