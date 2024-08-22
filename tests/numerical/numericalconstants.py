#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalNumericalConstants(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"e", 'expected': Number('2.71828182845904523536028747135266249775724709369995') },
        { 'test': r"pi", 'expected': Number('3.14159265358979323846264338327950288419716939937511') },
        { 'test': r"tau", 'expected': Number('6.28318530717958647692528676655900576839433879875022') },
        { 'test': r"tau / 2 pi", 'expected': Number('1') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalNumericalConstants.prepare_tests()

if __name__ == '__main__':
    execute_tests()
