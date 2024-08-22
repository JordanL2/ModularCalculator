#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalAdvancedArithmetic(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r'14 % 3', 'expected': Number('2') },
        { 'test': r'4 \ 3', 'expected': Number('1') },
        { 'test': r'(1000 \ 10) \ 10', 'expected': Number('10') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalAdvancedArithmetic.prepare_tests()

if __name__ == '__main__':
    execute_tests()
