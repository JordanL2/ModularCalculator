#!/usr/bin/python3

from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *

import argparse


print("AdvancedCalculator tests:")
c = ModularCalculator('Advanced')
hl = SyntaxHighlighter()

parser = argparse.ArgumentParser()
parser.add_argument('-n', dest='times', nargs='?', type=int, default=1, help='number of times to run the tests')
parser.add_argument('-t', dest='test',  nargs='?', type=int, default=0, help='test to run')
args = parser.parse_args()
times = args.times
test = args.test

tests = [
    { 'test': r'14 % 3', 'expected': Decimal('2') },
    { 'test': r'4 \ 3', 'expected': Decimal('1') },
    { 'test': r'(1000 \ 10) \ 10', 'expected': Decimal('10') },

    { 'test': '123 + 456', 'expected': Decimal('579') },
    { 'test': '123-1', 'expected': Decimal('122') },
    { 'test': '123 + (1 * 3) - 456', 'expected': Decimal('-330') },
    { 'test': '2 + 3 * 4', 'expected': Decimal('14') },
    { 'test': '2+-3/4', 'expected': Decimal('1.25') },
    { 'test': '2 + 3^3', 'expected': Decimal('29') },
    { 'test': '4 * (2 + (3)) - 3', 'expected': Decimal('17') },
    { 'test': r"10 / 3", 'expected': Decimal('3.333333333333333333333333333333') },
    { 'test': r"(10 / 3) * 3", 'expected': Decimal('10') },
    { 'test': r"10 / 3 (3)", 'expected': Decimal('10') },
    { 'test': "\n((1 + 3)\n/ 2)\n", 'expected': Decimal('2') },

    { 'test': r"x = 1 + 1", 'expected': Decimal('2') },
    { 'test': r"x", 'expected': Decimal('2') },
    { 'test': r"3 + (c = 4 * 5)", 'expected': Decimal('23') },
    { 'test': r"c", 'expected': Decimal('20') },

    { 'test': "1 + 2\n3 + 4", 'expected': Decimal('7') },
    { 'test': "1\n2", 'expected': Decimal('2') },
    { 'test': "1 \n2", 'expected': Decimal('2') },
    
    { 'test': "x = 0\nx++\nx", 'expected': Decimal('1') },
    { 'test': "x = 3\nx--\nx", 'expected': Decimal('2') },
    { 'test': "x = 0\nx += 2\nx", 'expected': Decimal('2') },
    { 'test': "x = 5\nx -= 2\nx", 'expected': Decimal('3') },
    { 'test': "x = 5\nx *= 2\nx", 'expected': Decimal('10') },
    { 'test': "x = 8\nx /= 4\nx", 'expected': Decimal('2') },
    { 'test': "x = 5\nx ^= 2\nx", 'expected': Decimal('25') },
    { 'test': "x = 15\nx %= 4\nx", 'expected': Decimal('3') },
    { 'test': "x = 5\nx \\= 2\nx", 'expected': Decimal('2') },

#    { 'test': r"", 'expected': Decimal('') },
]

if test != 0:
    tests = [tests[test - 1]]
tester = TestRunner(CalculatorException)
tester.test(c.calculate, tests)
