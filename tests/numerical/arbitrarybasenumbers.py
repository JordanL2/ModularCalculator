#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalArbitraryBaseNumbers(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"base(71, 36)", 'cast': str, 'expected': '36z1Z' },
        { 'test': r"base(0, 36)", 'cast': str, 'expected': '36z0' },
        { 'test': r"base(7, 10)", 'cast': str, 'expected': '10z7' },
        { 'test': r"dec(base(71, 36))", 'expected': Number('71') },
        { 'test': r"36z1Z", 'cast': str, 'expected': '36z1Z' },
        { 'test': r"-36z1Z", 'cast': str, 'expected': '-36z1Z' },
        { 'test': r"dec(-36z1Z)", 'expected': Number('-71') },
        { 'test': r"36Z1z", 'cast': str, 'expected': '36z1Z' },
        { 'test': r"4z1.2", 'cast': str, 'expected': '4z1.2' },
        { 'test': r"dec(4z1.2)", 'expected': Number('1.5') },
        { 'test': r"2z100", 'cast': str, 'expected': '2z100' },
        { 'test': r"2Z100", 'cast': str, 'expected': '2z100' },
        { 'test': r"2Z0", 'cast': str, 'expected': '2z0' },
        { 'test': r"02Z0", 'cast': str, 'expected': '2z0' },
        { 'test': r"002Z0", 'cast': str, 'expected': '2z0' },
        { 'test': r"2Z000", 'cast': str, 'expected': '2z0' },
        { 'test': r"dec(36z1Z)", 'expected': Number('71') },
        { 'test': r"dec(36Z1z)", 'expected': Number('71') },
        { 'test': r"dec(2z100)", 'expected': Number('4') },
        { 'test': r"dec(2Z100)", 'expected': Number('4') },
        { 'test': r"round(36z1Z.12I, 2)", 'cast': str, 'expected': '36z1Z.13' },
        { 'test': r"round(36z1Z.12H, 2)", 'cast': str, 'expected': '36z1Z.12' },
        { 'test': r"floor(36z1Z.12I, 2)", 'cast': str, 'expected': '36z1Z.12' },
        { 'test': r"ceil(36z1Z.12H, 2)", 'cast': str, 'expected': '36z1Z.13' },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalArbitraryBaseNumbers.prepare_tests()

if __name__ == '__main__':
    execute_tests()
