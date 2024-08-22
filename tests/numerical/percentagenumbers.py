#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalPercentageNumbers(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"100%", 'expected': Number('1') },
        { 'test': r"200% * 4", 'expected': Number('8') },
        { 'test': r"200% * 4", 'cast': str, 'expected': '800%' },
        { 'test': r"51.23%", 'expected': Number('0.5123') },
        { 'test': r"round(51.23%)", 'expected': Number('0.51') },
        { 'test': r"round(51.23%, 1)", 'expected': Number('0.512') },
        { 'test': r"ceil(51.23%, 1)", 'expected': Number('0.513') },
        { 'test': r"floor(51.29%, 1)", 'expected': Number('0.512') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalPercentageNumbers.prepare_tests()

if __name__ == '__main__':
    execute_tests()
