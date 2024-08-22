#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalBitwiseOperators(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"0b10101 & 0b110", 'cast': str, 'expected': '0b00100' },
        { 'test': r"0b10101 | 0b110", 'cast': str, 'expected': '0b10111' },
        { 'test': r"0b10101 ^^ 0b110", 'cast': str, 'expected': '0b10011' },
        { 'test': r"~0b1011101", 'cast': str, 'expected': '0b0100010' },
        { 'test': r"~0b00111100", 'cast': str, 'expected': '0b11000011' },
        { 'test': r"~60", 'expected': Number('3') },
        { 'test': r"0b10101 << 1", 'cast': str, 'expected': '0b101010' },
        { 'test': r"0b10101 << 2", 'cast': str, 'expected': '0b1010100' },
        { 'test': r"0b10101 << 8", 'cast': str, 'expected': '0b1010100000000' },
        { 'test': r"0b10010 >> 1", 'cast': str, 'expected': '0b01001' },
        { 'test': r"0b10010 >> 3", 'cast': str, 'expected': '0b00010' },
        { 'test': r"0b10010 >> 4", 'cast': str, 'expected': '0b00001' },
        { 'test': r"0b10010 >> 5", 'cast': str, 'expected': '0b00000' },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalBitwiseOperators.prepare_tests()

if __name__ == '__main__':
    execute_tests()
