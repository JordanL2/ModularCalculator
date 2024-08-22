#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalDecimalNumbers(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': '123', 'expected': Number(123) },
        { 'test': '123.45', 'expected': Number("123.45") },
        { 'test': '-123.45', 'expected': Number("-123.45") },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalDecimalNumbers.prepare_tests()

if __name__ == '__main__':
    execute_tests()
