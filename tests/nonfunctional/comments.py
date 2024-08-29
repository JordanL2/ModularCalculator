#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNonFunctionalComments(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': "123 + (#comment\n456)", 'expected': Number(579) },
        { 'test': "123 + 456#comment", 'expected': Number(579) },
        { 'test': "#comment\n123 + 456", 'expected': Number(579) },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNonFunctionalComments.prepare_tests()

if __name__ == '__main__':
    execute_tests()