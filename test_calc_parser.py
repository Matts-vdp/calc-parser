# This file contains all test routines for the calc_parser project

from calc_parser import *
import pytest
#================================================
# Lexer test routines
def test_lex():
    op = lexer("1.1")
    o = Operation(op)
    assert len(o.ops) == 1
    assert o.ops[0] == ["1.1", 'number']

def test_lex2():
    op = lexer("1 + 1")
    o = Operation(op)
    assert len(o.ops) == 3
    assert o.ops == [
        ["1", 'number'],
        ["+", 'operator'],
        ["1", 'number'],
    ]

def test_lex3():
    op = lexer("1+(1+1)")
    o = Operation(op)
    assert len(o.ops) == 7

def test_lex4():
    op = lexer("sum:1")
    o = Operation(op)
    assert len(o.ops) == 2
    assert o.ops == [
        ["sum:", 'special'],
        ["1", 'number'],
    ]

#================================================
# Test number class
def test_parseNumber():
    op = lexer("1")
    o = Operation(op)
    o.parse()
    assert len(o.ops) == 1
    assert isinstance(o.ops[0], Number)
    assert o.calculate() == 1

#================================================
# Test Math class and its children
def test_parseMath():
    op = lexer("1+1+1")
    o = Operation(op)
    o.parse()
    assert len(o.ops) == 1
    assert isinstance(o.ops[0], Math)
    assert o.calculate() == 3

def test_parseMath2():
    op = lexer("2*2+1")
    o = Operation(op)
    o.parse()
    assert len(o.ops) == 1
    assert isinstance(o.ops[0], Math)
    assert o.calculate() == 5

def test_parseMath3():
    op = lexer("2*2+1-2*1")
    o = Operation(op)
    o.parse()
    assert len(o.ops) == 1
    assert isinstance(o.ops[0], Math)
    assert o.calculate() == 3

#================================================
# Test Comma class
def test_Comma():
    op = lexer("1 , 2")
    o = Operation(op)
    o.parse()
    assert len(o.ops) == 1
    assert isinstance(o.ops[0], Comma)
    assert o.calculate() == [1,2]

#================================================
# Test Brackets class
def test_parseBrack():
    op = lexer("(1)")
    o = Operation(op)
    o.parse()
    assert len(o.ops) == 1
    assert isinstance(o.ops[0], Bracket)
    assert o.calculate() == 1

def test_parseBrack2():
    op = lexer("(1+(1))")
    o = Operation(op)
    o.parse()
    assert len(o.ops) == 1
    assert isinstance(o.ops[0], Bracket)
    assert o.calculate() == 2

def test_parseBrack3():
    op = lexer("(1+(1) + (2+1))")
    o = Operation(op)
    o.parse()
    assert len(o.ops) == 1
    assert isinstance(o.ops[0], Bracket)
    assert o.calculate() == 5

#================================================
# Test special functions
def test_special_sqrt():
    op = lexer("sqrt:4")
    o = Operation(op)
    o.parse()
    assert isinstance(o.ops[0], Special)
    assert o.calculate() == 2

def test_special_pow():
    op = lexer("pow:(2,3)")
    o = Operation(op)
    o.parse()
    assert isinstance(o.ops[0], Special)
    assert o.calculate() == 8

#================================================
# Test calculate function
def test_calculate():
    res = calculate("1+1 * (2+2)")
    assert res == 5
