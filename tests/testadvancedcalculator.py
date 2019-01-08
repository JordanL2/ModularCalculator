#!/usr/bin/python3

from testing.testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *


print("AdvancedCalculator tests:")
c = ModularCalculator('Advanced')
hl = SyntaxHighlighter()

tests = [
    { 'test': r'14 % 3', 'expected': Decimal('2') },
    { 'test': r'4 \ 3', 'expected': Decimal('1') },

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
    { 'test': "\n(1 + 3)\n/ 2\n", 'expected': Decimal('2') },

    { 'test': r"x = 1 + 1", 'expected': Decimal('2') },
    { 'test': r"x", 'expected': Decimal('2') },
    { 'test': r"3 + (c = 4 * 5)", 'expected': Decimal('23') },
    { 'test': r"c", 'expected': Decimal('20') },

    { 'test': r"1 + 2;3 + 4", 'expected': Decimal('7') },
    
    { 'test': r"x = 0; x++; x", 'expected': Decimal('1') },
    { 'test': r"x = 3; x--; x", 'expected': Decimal('2') },
    { 'test': r"x = 0; x += 2; x", 'expected': Decimal('2') },
    { 'test': r"x = 5; x -= 2; x", 'expected': Decimal('3') },
    { 'test': r"x = 5; x *= 2; x", 'expected': Decimal('10') },
    { 'test': r"x = 8; x /= 4; x", 'expected': Decimal('2') },
    { 'test': r"x = 5; x ^= 2; x", 'expected': Decimal('25') },
    { 'test': r"x = 15; x %= 4; x", 'expected': Decimal('3') },
    { 'test': r"x = 5; x \= 2; x", 'expected': Decimal('2') },

#    { 'test': r"", 'expected': Decimal('') },
]

tester = TestRunner(CalculatorException)
tester.test(c.calculate, tests)
