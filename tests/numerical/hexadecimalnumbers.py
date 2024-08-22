#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalHexadecimalNumbers(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"0xff", 'expected': Number("255") },
        { 'test': r"0xFF", 'expected': Number("255") },
        { 'test': r"0xFF.2", 'expected': Number("255.125") },
        { 'test': r"-0xFF.2", 'expected': Number("-255.125") },
        { 'test': r"hex(255)", 'cast': str, 'expected': '0xFF' },
        { 'test': r"dec(hex(255))", 'expected': Number('255') },
        { 'test': r"0xff", 'cast': str, 'expected': '0xFF' },
        { 'test': r"0xf.88", 'cast': str, 'expected': '0xF.88' },
        { 'test': r"0x0", 'cast': str, 'expected': '0x0' },
        { 'test': r"0x000", 'cast': str, 'expected': '0x0' },
        { 'test': r"dec(0xff)", 'expected': Number('255') },
        { 'test': r"dec(0xf.88)", 'expected': Number('15.53125') },
        { 'test': r"0xff + 0XFF", 'cast': str, 'expected': '0x1FE' },
        { 'test': r"hex(15.125)", 'cast': str, 'expected': '0xF.2' },
        { 'test': r"hex(0b10101)", 'cast': str, 'expected': '0x15' },
        { 'test': r"hex(-15.125)", 'cast': str, 'expected': '-0xF.2' },
        { 'test': r"hex(0)", 'cast': str, 'expected': '0x0' },
        { 'test': r"0xF + 4", 'cast': str, 'expected': '0x13' },
        { 'test': r"4 + 0xF", 'expected': Number('19') },
        { 'test': r"0x1 / 0x2", 'cast': str, 'expected': '0x0.8' },
        { 'test': r"0x2 / 0x3", 'cast': str, 'expected': '0x0.AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' },
        { 'test': r"round(0x10F.348, 2)", 'cast': str, 'expected': '0x10F.35' },
        { 'test': r"round(0x10F.347, 2)", 'cast': str, 'expected': '0x10F.34' },
        { 'test': r"floor(0x10F.348, 2)", 'cast': str, 'expected': '0x10F.34' },
        { 'test': r"ceil(0x10F.347, 2)", 'cast': str, 'expected': '0x10F.35' },

        { 'test': r"mean([5, 0xF])", 'expected': Number('10') },
        { 'test': r"mean([0xF, 5])", 'cast': str, 'expected': '0xA' },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalHexadecimalNumbers.prepare_tests()

if __name__ == '__main__':
    execute_tests()
