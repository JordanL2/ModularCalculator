#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStateAssignment(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"x = 1 + 1", 'expected': Number('2') },
        { 'test': r"3 + (c = 4 * 5)", 'expected': Number('23') },
        { 'test': r"day_usage = 1", 'expected': Number('1') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStateAssignment.prepare_tests()

if __name__ == '__main__':
    execute_tests()
