#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStringsStringFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"length('ABCabc')", 'expected': Number(6) },

        { 'test': r"lower('ABCabc')", 'expected': 'abcabc' },

        { 'test': r"upper('ABCabc')", 'expected': 'ABCABC' },

        { 'test': r"lstrip('   ABCabc   ', ' ')", 'expected': 'ABCabc   ' },

        { 'test': r"rstrip('   ABCabc   ', ' ')", 'expected': '   ABCabc' },

        { 'test': r"strip('   ABCabc   ', ' ')", 'expected': 'ABCabc' },

        { 'test': r"find('ABCabc', 'ab')", 'expected': Number(3) },

        { 'test': r"replace('ABCabc', 'BC', 'fgh')", 'expected': 'Afghabc' },
        { 'test': r"replace('ABCabc', '123', 'fgh')", 'expected': 'ABCabc' },
        { 'test': r"replace('ABCaBCbc', 'BC', 'fgh')", 'expected': 'Afghafghbc' },

        { 'test': r"substr('ABCabc', 3)", 'expected': 'abc' },
        { 'test': r"substr('ABCabc', -4)", 'expected': 'Cabc' },
        { 'test': r"substr('ABCabc', 3, 4)", 'expected': 'ab' },
        { 'test': r"substr('ABCabc', 4, 4)", 'expected': 'b' },
        { 'test': r"substr('ABCabc', 3, -1)", 'expected': 'abc' },
        { 'test': r"substr('ABCabc', 3, -2)", 'expected': 'ab' },
        { 'test': r"substr('ABCabc', -3, -2)", 'expected': 'ab' },
        { 'test': r"substr('123456', 4, 4)", 'expected': '5' },
        { 'test': r"substr('123456', 0b100, 0b100)", 'expected': '5' },
        { 'test': r"substr('123456', 0.5, 4)", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute substr with parameters: '123456', 0.5, 4 - substr parameter 2 must be of type(s) integer" } },
        { 'test': r"substr('123456', 4, 0.5)", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute substr with parameters: '123456', 4, 0.5 - substr parameter 3 must be of type(s) integer" } },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStringsStringFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
