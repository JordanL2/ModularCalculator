#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalExpNumbers(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"1.234e1", 'expected': Number('12.34') },
        { 'test': r"-1.234e1", 'expected': Number('-12.34') },
        { 'test': r"dec(1.234e1)", 'expected': Number('12.34') },
        { 'test': r"dec(1.234e10)", 'expected': Number('12340000000') },
        { 'test': r"dec(1.234e2)", 'expected': Number('123.4') },
        { 'test': r"dec(1.234e0)", 'expected': Number('1.234') },
        { 'test': r"dec(1.234e-1)", 'expected': Number('0.1234') },
        { 'test': r"dec(1.234e-2)", 'expected': Number('0.01234') },
        { 'test': r"dec(5.97237e24 kg)", 'expected': (Number('5972370000000000000000000'), 'kilograms') },
        { 'test': r"1.23e2 + 1.2e1", 'cast': str, 'expected': '1.35E2' },
        { 'test': r"1.23e2kg + 1.2e1kg", 'cast': str, 'expected': ('1.35E2', 'kilograms') },
        { 'test': r"dec(1.23e2 + 1.2e1)", 'expected': Number('135') },
        { 'test': r"10E0 * 1", 'cast': str, 'expected': '1E1' },
        { 'test': r"0E0", 'cast': str, 'expected': '0E0' },
        { 'test': r"0E0 * 1", 'cast': str, 'expected': '0E0' },
        { 'test': r"1E9 * 1", 'cast': str, 'expected': '1E9' },
        { 'test': r"1 * 1E9", 'expected': Number('1000000000') },
        { 'test': r"dec(1E9)", 'expected': Number('1000000000') },
        { 'test': r"dec(1E9)", 'cast': str, 'expected': '1000000000' },
        { 'test': r"1E9 m", 'cast': str, 'expected': ('1E9', 'meters') },
        { 'test': r"dec(1E9 m)", 'expected': (Number('1000000000'), 'meters') },
        { 'test': r"dec(1E9) m", 'expected': (Number('1000000000'), 'meters') },
        { 'test': r"2e0 / 3", 'cast': str, 'expected': '6.666666666666666666666666666667E-1' },
        { 'test': r"scientific(123.456789)", 'cast': str,  'expected': '1.23456789E2' },
        { 'test': r"scientific(123.45678900000)", 'cast': str,  'expected': '1.23456789E2' },
        { 'test': r"scientific(12345678900000)", 'cast': str,  'expected': '1.23456789E13' },
        { 'test': r"scientific(123.456789, 3)", 'cast': str,  'expected': '1.235E2' },
        { 'test': r"scientific(123.456789, 5)", 'cast': str,  'expected': '1.23457E2' },
        { 'test': r"scientific(0.000123456789, 5)", 'cast': str,  'expected': '1.23457E-4' },
        { 'test': r"scientific(123.456789 miles)", 'cast': str,  'expected': ('1.23456789E2', 'miles') },
        { 'test': r"scientific(123.4) * 2", 'cast': str,  'expected': '2.468E2' },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalExpNumbers.prepare_tests()

if __name__ == '__main__':
    execute_tests()
