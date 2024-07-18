#!/usr/bin/python3

from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *


class TestErrorHandling(CalculatorTestCase):

    c = ModularCalculator('Computing')

    tests = [
        { 'test': r"1 2", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': r"Could not parse: 2",
                                                'pos': 2,
                                                'items': ['1', ' '] } },

        { 'test': r"1 + + 1", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Invalid input for operator + - '+'",
                                                'pos': 2,
                                                'items': ['1',' '] } },

        { 'test': r"1+ + 1", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Invalid input for operator + - '+'",
                                                'pos': 1,
                                                'items': ['1'] } },

        { 'test': r"+ 1", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Missing left operands for operator +",
                                                'pos': 0,
                                                'items': [] } },

        { 'test': r" + ", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Missing left operands for operator +",
                                                'pos': 1,
                                                'items': [' '] } },

        { 'test': r"+", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Missing left operands for operator +",
                                                'pos': 0,
                                                'items': [] } },

        { 'test': r"1 +", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Missing right operands for operator +",
                                                'pos': 2,
                                                'items': ['1',' '] } },

        { 'test': r"1 + (2 3)", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': r"Could not parse: 3)",
                                                'pos': 7,
                                                'items': ['1',' ','+',' ','(','2',' '] } },

        { 'test': r"1 + (2  3)", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': r"Could not parse: 3)",
                                                'pos': 8,
                                                'items': ['1',' ','+',' ','(','2',' ',' '] } },

        { 'test': r"min([1, 2, ''])", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Function min parameter 1 must be of type(s) array[number]",
                                                'pos': 0,
                                                'items': [] } },

        { 'test': r"1 + (min([1, 2, '']))", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Function min parameter 1 must be of type(s) array[number]",
                                                'pos': 5,
                                                'items': ['1',' ','+',' ','(',],
                                                'next': 'min([1, 2, \'\'])' } },

        { 'test': r"1 + (min([1, 2, 3 +])", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': r"Inner expression missing close symbol",
                                                'pos': 4,
                                                'items': ['1',' ','+',' '] } },

        { 'test': r"1 + (min([1, 2, 3 +]))", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Missing right operands for operator +",
                                                'pos': 18,
                                                'items': ['1',' ','+',' ','(','min','(','[','1',',',' ','2',',',' ','3',' '],
                                                'next': '+' } },

        { 'test': r"1 + (min([1, 2, 3] +))", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Missing right operands for operator +",
                                                'pos': 19,
                                                'items': ['1',' ','+',' ','(','min','(','[','1',',',' ','2',',',' ','3',']',' '],
                                                'next': '+' } },

        { 'test': r"1 + (min([1, 2, (1 2)])", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': r"Could not parse: 2)])",
                                                'pos': 19,
                                                'items': ['1',' ','+',' ','(','min','(','[','1',',',' ','2',',',' ','(','1',' '] } },

        { 'test': r"sort([1, 2, 3], [4, 5, 6])", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Cannot pass multiple arrays to an operation that returns an array",
                                                'pos': 0,
                                                'items': [] } },

        { 'test': r"1 / 0", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with operands: 1, 0 - Could not execute Operator /",
                                                'pos': 2,
                                                'items': ['1',' '] } },

        { 'test': r"2 + (1 / 0) + 3", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with operands: 1, 0 - Could not execute Operator /",
                                                'pos': 7,
                                                'items': ['2',' ','+',' ','(','1',' '] } },

        { 'test': "(2 + #comment\n(1 / 0) + 3)", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with operands: 1, 0 - Could not execute Operator /",
                                                'pos': 17,
                                                'items': ['(','2',' ','+',' ','#comment',"\n",'(','1',' '] } },

        { 'test': r"(2 + (((1 / 0)) + 3))", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with operands: 1, 0 - Could not execute Operator /",
                                                'pos': 10,
                                                'items': ['(','2',' ','+',' ','(','(','(','1',' '] } },

        { 'test': r"1 + ''", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator + with operands: 1, '' - Operator + parameter 2 must be of type(s) number",
                                                'pos': 2,
                                                'items': ['1',' '] } },

        { 'test': r"true then 1 else 2 3", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': r"Could not parse: 3",
                                                'pos': 19,
                                                'items': ['true',' ','then',' ','1',' ','else',' ','2',' '] } },

        { 'test': r"true then 1 2 else 3", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': r"Could not parse: 2 else 3",
                                                'pos': 12,
                                                'items': ['true',' ','then',' ','1',' '] } },

        { 'test': r"false then 1 else (+)", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Missing left operands for operator +",
                                                'pos': 19,
                                                'items': ['false',' ','then',' ','1',' ','else',' ','('] } },

        { 'test': r"false then 1 else ( +)", 'expected_exception': {
                                                'message': r"Missing left operands for operator +",
                                                'exception': ExecutionException,
                                                'pos': 20,
                                                'items': ['false',' ','then',' ','1',' ','else',' ','(',' '] } },

        { 'test': r"true then 1 else 2 else 3", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator: else",
                                                'pos': 19,
                                                'items': ['true',' ','then',' ','1',' ','else',' ','2',' '] } },

        { 'test': r"true else false then 1 else 2", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator: else",
                                                'pos': 5,
                                                'items': ['true',' '] } },

        { 'test': r"(1 hectare to 2)^0.5", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator to with operands: 1 hectares^1, 2 - Operator to parameter 2 must be of type(s) unit",
                                                'pos': 11,
                                                'items': ['(','1',' ','hectare',' '] } },

        { 'test': r"(1 hectare to 2) ^ 0.5", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator to with operands: 1 hectares^1, 2 - Operator to parameter 2 must be of type(s) unit",
                                                'pos': 11,
                                                'items': ['(','1',' ','hectare',' '] } },

        { 'test': "(1 hectare to 2)#comment\n^ 0.5", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator to with operands: 1 hectares^1, 2 - Operator to parameter 2 must be of type(s) unit",
                                                'pos': 11,
                                                'items': ['(','1',' ','hectare',' '] } },

        { 'test': "#comment\n(1 hectare to 2) ^ 0.5", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator to with operands: 1 hectares^1, 2 - Operator to parameter 2 must be of type(s) unit",
                                                'pos': 20,
                                                'items': ['#comment',"\n",'(','1',' ','hectare',' '] } },

        { 'test': "dateadd('2017-01-01', 3)", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Function dateadd parameter 2 must have unit dimensions: time^1",
                                                'pos': 0,
                                                'items': [] } },

        { 'test': "(1/0) else", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator: else",
                                                'pos': 6,
                                                'items': ['(','1','/','0',')',' '] } },

        { 'test': "f = './tests/externalfunctions/does_not_exist'\n@f(1, 2)", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not read file './tests/externalfunctions/does_not_exist'",
                                                'pos': 47,
                                                'items': ['f',' ','=',' ',"'./tests/externalfunctions/does_not_exist'","\n"] } },

        { 'test': "f = './tests/externalfunctions/ext_func_addition2'\n@f(1, 2)", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator + with operands: 3, None - Operator + parameter 2 must be of type(s) number",
                                                'pos': 51,
                                                'items': ['f',' ','=',' ',"'./tests/externalfunctions/ext_func_addition2'","\n"] } },

        { 'test': "round((+))", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Missing left operands for operator +",
                                                'pos': 7,
                                                'items': ['round','(','('] } },

        { 'test': "(1/0) +", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Missing right operands for operator +",
                                                'pos': 6,
                                                'items': ['(','1','/','0',')',' '],
                                                'next': '+' } },

        { 'test': "[1, 2 / 0]", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with operands: 2, 0 - Could not execute Operator /",
                                                'pos': 6,
                                                'items': ['[','1',',',' ','2',' '] } },

        { 'test': "[1, (2 / 0)]", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with operands: 2, 0 - Could not execute Operator /",
                                                'pos': 7,
                                                'items': ['[','1',',',' ','(','2',' '] } },

        { 'test': "[1 .. 2 / 0 step 2]", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with operands: 2, 0 - Could not execute Operator /",
                                                'pos': 8,
                                                'items': ['[','1',' ','..',' ','2',' '] } },

        { 'test': "[1 .. (2 / 0) step 2]", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with operands: 2, 0 - Could not execute Operator /",
                                                'pos': 9,
                                                'items': ['[','1',' ','..',' ','(','2',' '] } },

        { 'test': "[1 .. 2 step 2 / 0]", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with operands: 2, 0 - Could not execute Operator /",
                                                'pos': 15,
                                                'items': ['[','1',' ','..',' ','2',' ','step',' ','2',' '] } },

        { 'test': "[1 .. 2 step (2 / 0)]", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with operands: 2, 0 - Could not execute Operator /",
                                                'pos': 16,
                                                'items': ['[','1',' ','..',' ','2',' ','step',' ','(','2',' '] } },

        { 'test': "[1 .. 2 step -1]", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Can't get from 1 to 2 with step -1",
                                                'pos': 15,
                                                'items': ['[','1',' ','..',' ','2',' ','step',' ','-1'] } },

        { 'test': "[1 step 2]", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': r"Parsing error in array",
                                                'pos': 3,
                                                'items': ['[','1',' '] } },

        { 'test': "@mean([", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': r"Array missing close symbol",
                                                'pos': 6,
                                                'items': ['@mean','('] } },

        { 'test': "simplefunc = './tests/externalfunctions/simplefunc'\n@simplefunc(@simplefunc(*))", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Missing left operands for operator *",
                                                'pos': 76,
                                                'items': ['simplefunc',' ','=',' ',"'./tests/externalfunctions/simplefunc'",'\n','@simplefunc','(','@simplefunc','('] } },

        { 'test': "f = { £ }", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': r"Could not parse: £ }",
                                                'pos': 6,
                                                'items': ['f',' ','=',' ','{',' '] } },

        { 'test': "f = {\n£}", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': r"Could not parse: £}",
                                                'pos': 6,
                                                'items': ['f',' ','=',' ','{',"\n"] } },

       { 'test': "f = {\nff = {\n£\n}\n}", 'expected_exception': {
                                                'exception': ParsingException,
                                                'message': "Could not parse: £\n}\n}",
                                                'pos': 13,
                                                'items': ['f',' ','=',' ','{','\n','ff',' ','=',' ','{','\n'] } },
    #    { 'test': r"", 'expected': { 'exception': ParsingException, 'message': r"", 'pos': 0, 'items': [] } },
    ]

    def setUp(self):
        self.c = ModularCalculator('Computing')
        self.hl = SyntaxHighlighter()


TestErrorHandling.prepare_tests()

if __name__ == '__main__':
    execute_tests()
