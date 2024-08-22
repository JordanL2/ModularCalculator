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
        { 'test': "x = 1\n x", 'expected': Number('1') },
        { 'test': "x = 5.5 metres\n x", 'expected': (Number('5.5'), 'meters') },
        { 'test': "x = 5.5 metres\n x * -1", 'expected': (Number('-5.5'), 'meters') },
        { 'test': "x = 1\n x * 2", 'expected': Number('2') },
        { 'test': "x = 1 + 1", 'expected': Number('2') },
        { 'test': "3 + (c = 4 * 5)", 'expected': Number('23') },
        { 'test': "3 + (c = 4 * 5)\n c", 'expected': Number('20') },
        { 'test': "day_usage = 1\n day_usage", 'expected': Number('1') },
        { 'test': "day_usage_2 = 1\n day_usage_2", 'expected': Number('1') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStateAssignment.prepare_tests()

if __name__ == '__main__':
    execute_tests()
