#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *

from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStructureInnerExpressions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': '4 * (2 + (3)) - 3', 'expected': Number('17') },
        { 'test': r"(10 / 3) * 3", 'expected': Number('10') },
        { 'test': r"10 / 3 (3)", 'expected': Number('10', '9') },
        { 'test': '123 + (1 * 3) - 456', 'expected': Number('-330') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStructureInnerExpressions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
