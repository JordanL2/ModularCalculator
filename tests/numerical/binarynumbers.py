#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalBinaryNumbers(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"0b10", 'cast': str, 'expected': '0b10' },
        { 'test': r"0B10", 'cast': str, 'expected': '0b10' },
        { 'test': r"-0b11", 'cast': str, 'expected': '-0b11' },
        { 'test': r"-0b0011", 'cast': str, 'expected': '-0b0011' },
        { 'test': r"-0b11 | 0b0000", 'cast': str, 'expected': '-0b0011' },
        { 'test': r"0b11 | 0b0100", 'cast': str, 'expected': '0b0111' },
        { 'test': r"0b10.1", 'cast': str, 'expected': '0b10.1' },
        { 'test': r"0b0", 'cast': str, 'expected': '0b0' },
        { 'test': r"0b000", 'cast': str, 'expected': '0b000' },
        { 'test': r"dec(0b10)", 'expected': Number('2') },
        { 'test': r"dec(0B10)", 'expected': Number('2') },
        { 'test': r"dec(-0b11)", 'expected': Number('-3') },
        { 'test': r"dec(0b10.1)", 'expected': Number('2.5') },
        { 'test': r"0b10 + 0b1", 'cast': str, 'expected': '0b11' },
        { 'test': r"bin(0b10 + 0b1)", 'cast': str, 'expected': '0b11' },
        { 'test': r"0b10 * 0b10", 'cast': str, 'expected': '0b100' },
        { 'test': r"0b1000 / 0b10", 'cast': str, 'expected': '0b100' },
        { 'test': r"bin(0b10 * 0b10)", 'cast': str, 'expected': '0b100' },
        { 'test': r"bin(0b10 * -0B10)", 'cast': str, 'expected': '-0b100' },
        { 'test': r"dec(bin(0b10 * -0B10))", 'expected': Number('-4') },
        { 'test': r"bin(0.5)", 'cast': str, 'expected': '0b0.1' },
        { 'test': r"bin(3.5)", 'cast': str, 'expected': '0b11.1' },
        { 'test': r"bin(-3.5)", 'cast': str, 'expected': '-0b11.1' },
        { 'test': r"bin(0)", 'cast': str, 'expected': '0b0' },
        { 'test': r"bin(0x1A)", 'cast': str, 'expected': '0b11010' },
        { 'test': r"0b10 / 0b11", 'cast': str, 'expected': '0b0.10101010101010101010101010101' },
        { 'test': r"0b1 / 0b10", 'cast': str, 'expected': '0b0.1' },
        { 'test': "a = (0b10 / 0b11)\na * 0b11", 'cast': str, 'expected': '0b10' },
        { 'test': r"((0b10 / 0b11) * 0b11)", 'cast': str, 'expected': '0b10' },
        { 'test': r"fact(0b101)", 'cast': str, 'expected': '0b1111000' },
        { 'test': r"round(0b101.10101)", 'cast': str, 'expected': '0b110' },
        { 'test': r"round(0b101.10101, 2)", 'cast': str, 'expected': '0b101.11' },
        { 'test': r"round(0b101.10101, 3)", 'cast': str, 'expected': '0b101.101' },
        { 'test': r"floor(0b101.10111, 2)", 'cast': str, 'expected': '0b101.1' },
        { 'test': r"ceil(0b101.10001, 3)", 'cast': str, 'expected': '0b101.101' },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalBinaryNumbers.prepare_tests()

if __name__ == '__main__':
    execute_tests()
