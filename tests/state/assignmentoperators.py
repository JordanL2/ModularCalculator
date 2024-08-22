#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStateAssignmentOperators(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': "x = 0\nx++\nx", 'expected': Number('1') },
        { 'test': "x = 3\nx--\nx", 'expected': Number('2') },
        { 'test': "x = 0\nx += 2\nx", 'expected': Number('2') },
        { 'test': "x = 5\nx -= 2\nx", 'expected': Number('3') },
        { 'test': "x = 5\nx *= 2\nx", 'expected': Number('10') },
        { 'test': "x = 8\nx /= 4\nx", 'expected': Number('2') },
        { 'test': "x = 5\nx ^= 2\nx", 'expected': Number('25') },
        { 'test': "x = 15\nx %= 4\nx", 'expected': Number('3') },
        { 'test': "x = 5\nx \\= 2\nx", 'expected': Number('2') },

        { 'test': "x = 5\nx *= 2", 'expected': Number('10') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStateAssignmentOperators.prepare_tests()

if __name__ == '__main__':
    execute_tests()
