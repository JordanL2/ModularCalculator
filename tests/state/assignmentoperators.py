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
        { 'test': "x = 0\n x++\n x", 'expected': Number('1') },
        { 'test': "x = -1.5\n x++\n x", 'expected': Number('-0.5') },

        { 'test': "x = 3\n x--\n x", 'expected': Number('2') },
        { 'test': "x = 0.5\n x--\n x", 'expected': Number('-0.5') },

        { 'test': "x = 0\n x += 2\n x", 'expected': Number('2') },
        { 'test': "x = 1\n x += 2.5\n x", 'expected': Number('3.5') },

        { 'test': "x = 5\n x -= 2\n x", 'expected': Number('3') },
        { 'test': "x = 1.5\n x -= 2.7\n x", 'expected': Number('-1.2') },

        { 'test': "x = 5\n x *= 2\n x", 'expected': Number('10') },
        { 'test': "x = 5\n x *= -2.5\n x", 'expected': Number('-12.5') },
        { 'test': "x = 5\n x *= 2", 'expected': Number('10') },
        { 'test': "x = 8\n x /= 4\n x", 'expected': Number('2') },

        { 'test': "x = 5\n x ^= 2\n x", 'expected': Number('25') },
        { 'test': "x = 25\n x ^= 0.5\n x", 'expected': Number('5') },
        { 'test': "x = 5\n x ^= -1\n x", 'expected': Number('0.2') },

        { 'test': "x = 15\n x %= 4\n x", 'expected': Number('3') },

        { 'test': "x = 5\n x \\= 2\n x", 'expected': Number('2') },
    ]



    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStateAssignmentOperators.prepare_tests()

if __name__ == '__main__':
    execute_tests()
