#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStateAssignmentFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': "x = 1\nreset()\nx", 'expected': None },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStateAssignmentFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
