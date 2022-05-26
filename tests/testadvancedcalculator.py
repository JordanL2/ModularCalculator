#!/usr/bin/python3

from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestAdvancedCalculator(CalculatorTestCase):

    c = ModularCalculator('Advanced')
    tests = [
        { 'test': r'14 % 3', 'expected': Number('2') },
        { 'test': r'4 \ 3', 'expected': Number('1') },
        { 'test': r'(1000 \ 10) \ 10', 'expected': Number('10') },

        { 'test': '123 + 456', 'expected': Number('579') },
        { 'test': '123-1', 'expected': Number('122') },
        { 'test': '123 + (1 * 3) - 456', 'expected': Number('-330') },
        { 'test': '2 + 3 * 4', 'expected': Number('14') },
        { 'test': '2+-3/4', 'expected': Number('1.25') },
        { 'test': '2 + 3^3', 'expected': Number('29') },
        { 'test': '4 * (2 + (3)) - 3', 'expected': Number('17') },
        { 'test': r"10 / 3", 'expected': Number(10, 3) },
        { 'test': r"(10 / 3) * 3", 'expected': Number('10') },
        { 'test': r"10 / 3 (3)", 'expected': Number('10') },
        { 'test': "\n((1 + 3)\n/ 2)\n", 'expected': Number('2') },

        { 'test': r"x = 1 + 1", 'expected': Number('2') },
        { 'test': r"3 + (c = 4 * 5)", 'expected': Number('23') },

        { 'test': "1 + 2\n3 + 4", 'expected': Number('7') },
        { 'test': "1\n2", 'expected': Number('2') },
        { 'test': "1 \n2", 'expected': Number('2') },

        { 'test': "x = 0\nx++\nx", 'expected': Number('1') },
        { 'test': "x = 3\nx--\nx", 'expected': Number('2') },
        { 'test': "x = 0\nx += 2\nx", 'expected': Number('2') },
        { 'test': "x = 5\nx -= 2\nx", 'expected': Number('3') },
        { 'test': "x = 5\nx *= 2\nx", 'expected': Number('10') },
        { 'test': "x = 8\nx /= 4\nx", 'expected': Number('2') },
        { 'test': "x = 5\nx ^= 2\nx", 'expected': Number('25') },
        { 'test': "x = 15\nx %= 4\nx", 'expected': Number('3') },
        { 'test': "x = 5\nx \\= 2\nx", 'expected': Number('2') },

    #    { 'test': r"", 'expected': Number('') },
    ]

    def setUp(self):
        self.c = ModularCalculator('Advanced')


TestAdvancedCalculator.prepare_tests()

if __name__ == '__main__':
    execute_tests()
