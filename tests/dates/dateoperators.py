#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestDatesDateOperators(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': "'2012-01-02T11:45:56' +% 5 seconds", 'expected': '2012-01-02T11:46:01' },
        { 'test': "'2012-01-02T11:45:56' -% 5 seconds", 'expected': '2012-01-02T11:45:51' },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestDatesDateOperators.prepare_tests()

if __name__ == '__main__':
    execute_tests()
