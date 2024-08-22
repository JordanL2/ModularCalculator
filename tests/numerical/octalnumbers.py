#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalOctalNumbers(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"0o77", 'expected': Number('63') },
        { 'test': r"0o77.4", 'expected': Number('63.5') },
        { 'test': r"-0o77.4", 'expected': Number('-63.5') },
        { 'test': r"oct(63)", 'cast': str, 'expected': '0o77' },
        { 'test': r"dec(oct(63))", 'expected': Number('63') },
        { 'test': r"0o77", 'cast': str, 'expected': '0o77' },
        { 'test': r"0o77.4", 'cast': str, 'expected': '0o77.4' },
        { 'test': r"0o0", 'cast': str, 'expected': '0o0' },
        { 'test': r"0o000", 'cast': str, 'expected': '0o0' },
        { 'test': r"dec(0o77)", 'expected': Number('63') },
        { 'test': r"dec(0o77.4)", 'expected': Number('63.5') },
        { 'test': r"oct(63.5)", 'cast': str, 'expected': '0o77.4' },
        { 'test': r"oct(-63.5)", 'cast': str, 'expected': '-0o77.4' },
        { 'test': r"oct(0)", 'cast': str, 'expected': '0o0' },
        { 'test': r"oct(0b10101)", 'cast': str, 'expected': '0o25' },
        { 'test': r"round(0o12.334, 2)", 'cast': str, 'expected': '0o12.34' },
        { 'test': r"round(0o12.334, 1)", 'cast': str, 'expected': '0o12.3' },
        { 'test': r"floor(0o12.337, 2)", 'cast': str, 'expected': '0o12.33' },
        { 'test': r"ceil(0o12.301, 1)", 'cast': str, 'expected': '0o12.4' },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalOctalNumbers.prepare_tests()

if __name__ == '__main__':
    execute_tests()
