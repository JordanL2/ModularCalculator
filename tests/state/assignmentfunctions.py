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
        { 'test': "x = 1\n y=2\n reset()\n x", 'expected': None },
        { 'test': "x = 1\n y=2\n reset()\n y", 'expected': None },
        { 'test': "x = 1\nreset()\n x", 'expected': None },
        { 'test': "x = 1\nreset()\n x = 2\n x", 'expected': Number('2') },
        { 'test': "x = 1\n y=2\n delete(x)\n x", 'expected': None },
        { 'test': "x = 1\n y=2\n delete(x)\n y", 'expected': Number('2') },
        { 'test': "x = 1\n y=2\n delete(y)\n x", 'expected': Number('1') },
        { 'test': "x = 1\n y=2\n delete(y)\n y", 'expected': None },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStateAssignmentFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
