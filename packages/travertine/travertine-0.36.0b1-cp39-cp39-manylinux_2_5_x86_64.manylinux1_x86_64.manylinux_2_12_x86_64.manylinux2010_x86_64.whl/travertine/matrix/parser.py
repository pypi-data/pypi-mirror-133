#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import datetime
import re
from functools import wraps
from typing import Dict

import dateutil.parser
from lark import Lark, Token, Transformer, v_args

from travertine.types import MATCH, RANGE

from .ast import ColumnSpec, FormulaCell
from .ast import MatrixSpecification as Spec
from .ast import RangeCell, ValueCell

# Cache two possible parsers: one with debug=False, and the other with
# debug=True
_parsers: Dict[bool, Lark] = {}


def parse(spec: str, *, debug=False) -> Spec:
    """Parse the `code` and return an AST."""
    spec = spec.strip()
    parser = _parsers.get(debug)
    if parser is None:
        parser = _parsers[debug] = Lark(
            grammar, start="spec", propagate_positions=True, debug=debug
        )
    code = spec.strip()
    builder = ASTBuilder(code)
    return builder.transform(parser.parse(code))


ALPHA = re.compile(r"[a-zA-Z ]")

grammar = r"""
%import common (NEWLINE, WS, WS_INLINE, SIGNED_NUMBER, ESCAPED_STRING)

DATE : /\d{4}-\d{2}-\d{2}/
DATETIME : /\d{4}-\d{2}-\d{2}[ ]+\d{2}:\d{2}(:\d{2})?([ ]+(\w+|[-+]\d+))?/

DAYS : /\d+[ ]*d(ays|ay)?/i
HOURS: /\d+[ ]*h(ours|our)?/i
MINUTES: /\d+[ ]*m(inutes|inute|ins|in)?/i
SECONDS: /\d+[ ]*s(econds|econd|ecs|ec)?/i

KEYWORD_MATCH : "match"
KEYWORD_IN_RANGE : /in[ ]+range/

%ignore WS_INLINE

_hyphen : "-" | "–"
_quot : "\""
_newline : NEWLINE

spec : header _newline rows

_sep : ";" | ","

rows : row (_newline row)*
row : _cell (_sep _cell)* _sep _price


header : _column_headers
_column_headers : column_header (_sep column_header)* _sep price_locator

column_header : _quoted_column_header | _unquoted_column_header
_unquoted_column_header : locator (locator_kind)?
_quoted_column_header : _quot _unquoted_column_header _quot

locator : /[\w_]+\.[\w_]+/
locator_kind : KEYWORD_MATCH | KEYWORD_IN_RANGE

price_locator : "_" | _quot "_" _quot
_price : price_number | price_formula

price_number : number | _quot number _quot
price_formula : _quot formula _quot

_cell : _unquoted_cell | _quoted_cell
_unquoted_cell : interval | value
_quoted_cell : _quot _unquoted_cell _quot | string_cell

interval : _bare_value _hyphen _bare_value
value : _bare_value

_bare_value : number | date | datetime | timedelta

string_cell: ESCAPED_STRING
number : SIGNED_NUMBER
date : DATE
datetime : DATETIME

timedelta : days hours? minutes? seconds?
          | days? hours minutes? seconds?
          | days? hours? minutes seconds?
          | days? hours? minutes? seconds


days: DAYS
hours : HOURS
minutes : MINUTES
seconds : SECONDS

// Embedded formula grammar to allow formulas to be computed inside the
// matrix.  We don't allow substeps in the grammar, cause MatrixProcedure
// doesn't support sub-steps.

_ADD : "+"
_SUB : "-"
_MUL : "*"
_TRUEDIV : "/"
_FLOORDIV : "//"
_LPAREN : "("
_RPAREN : ")"
_single_quot: "'"

formula : expression

expression : expression _ADD term
           | expression _SUB term
           | term

term : term _MUL factor
     | term _FLOORDIV factor
     | term _TRUEDIV factor
     | factor

factor : variable | number | _SUB expression | _LPAREN expression _RPAREN
variable : _single_quot /[^']+/ _single_quot
"""


def return_asis():
    @v_args(inline=True)
    def result(self, val):
        return val

    return result


def with_meta(f):
    """An extension to @v_args(tree=True) that copies the metadata to the result."""

    @v_args(tree=True)
    @wraps(f)
    def result(self, tree):
        res = f(self, tree)
        res.meta = tree.meta
        return res

    return result


class ASTBuilder(Transformer):
    def __init__(self, source_code):
        super().__init__()
        self.source_code = source_code

    @with_meta
    def spec(self, tree):
        header, _newline, rows = tree.children
        return Spec(header, rows)

    @v_args(tree=True)
    def header(self, tree):
        assert all(
            isinstance(item, ColumnSpec) for item in tree.children
        ), f"Not all children are specs: {tree.children}"
        return tree.children

    @with_meta
    def price_locator(self, tree):
        return ColumnSpec(None, ("", "_"), None)

    @v_args(inline=True)
    def locator(self, token: Token):
        owner, attr = token.value.split(".")
        return (owner, attr)

    @with_meta
    def column_header(self, tree):
        original_spec, *rest = tree.children
        if rest:
            [kind] = rest
            assert kind is RANGE or kind is MATCH
        else:
            kind = None
        # The type-checker will fill the attribute locator.
        return ColumnSpec(None, original_spec, kind)

    @v_args(inline=True)
    def locator_kind(self, token: Token):
        if token.type == "KEYWORD_MATCH":
            return MATCH
        else:
            return RANGE

    @v_args(tree=True)
    def row(self, tree):
        return tree.children

    @v_args(tree=True)
    def rows(self, tree):
        return [row for row in tree.children if isinstance(row, list)]

    @with_meta
    def price_number(self, tree):
        return ValueCell(tree.children[0])

    @with_meta
    def price_formula(self, tree):
        return FormulaCell(
            self.source_code[tree.meta.start_pos + 1 : tree.meta.end_pos - 1]
        )

    @v_args(inline=True)
    def string_cell(self, s):
        return ValueCell(s[1:-1])

    @v_args(inline=True)
    def date(self, literal_date):
        y, m, d = literal_date.split("-")
        return datetime.date(int(y), int(m), int(d))

    @v_args(inline=True)
    def datetime(self, literal_datetime):
        return dateutil.parser.parse(literal_datetime)

    @v_args(inline=True)
    def number(self, literal_number):
        if "." in literal_number or "e" in literal_number:
            return float(literal_number)
        else:
            return int(literal_number)

    # We use a little trick: each component of the 'timedelta' production
    # returns a datetime.timedelta, which means we can simply sum all the
    # components together.
    @v_args(inline=True)
    def timedelta(self, *deltas):
        return sum(deltas, datetime.timedelta(0))

    @v_args(inline=True)
    def days(self, token):
        days = int(ALPHA.sub("", token.value))
        return datetime.timedelta(hours=24 * days)

    @v_args(inline=True)
    def hours(self, token):
        hrs = int(ALPHA.sub("", token.value))
        return datetime.timedelta(hours=hrs)

    @v_args(inline=True)
    def minutes(self, token):
        mins = int(ALPHA.sub("", token.value))
        return datetime.timedelta(minutes=mins)

    @v_args(inline=True)
    def seconds(self, token):
        secs = int(ALPHA.sub("", token.value))
        return datetime.timedelta(seconds=secs)

    @with_meta
    def value(self, tree):
        return ValueCell(tree.children[0])

    @with_meta
    def interval(self, tree):
        return RangeCell(tree.children[0], tree.children[-1])
