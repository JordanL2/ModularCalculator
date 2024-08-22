#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalBasicArithmetic(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': '123 + 456', 'expected': Number(579) },
        { 'test': '123.2 + 456.7', 'expected': Number("579.9") },
        { 'test': '123 + -456', 'expected': Number(-333) },
        { 'test': '123.2 + -456.7', 'expected': Number("-333.5") },
        { 'test': '123 - 1', 'expected': Number(122) },
        { 'test': '123.2 - 1.1', 'expected': Number("122.1") },
        { 'test': '123 - -1', 'expected': Number(124) },
        { 'test': '2 + 3 * 4', 'expected': Number(14) },
        { 'test': '2 + 3 * 4.5', 'expected': Number("15.5") },
        { 'test': '2 + -3 / 4', 'expected': Number('1.25') },
        { 'test': '1 + 2 * 3 -4', 'expected': Number(3) },
        { 'test': '10 / 5 * 2', 'expected': Number(4) },
        { 'test': r"10 / 3", 'expected': Number(10, 3) },
        { 'test': r"9 / 4.5", 'expected': Number(2) },
        { 'test': r"9 / -4.5", 'expected': Number(-2) },
        { 'test': r"-13.5 / 4.5", 'expected': Number(-3) },
        { 'test': '2 + 3^3', 'expected': Number(29) },
        { 'test': '2 ^ 8', 'expected': Number(256) },
        { 'test': '4 ^ 0.5', 'expected': Number(2) },
        { 'test': '4 ^ 0', 'expected': Number(1) },
        { 'test': '4 ^ -1', 'expected': Number("0.25") },
        { 'test': '-4 ^ -1', 'expected': Number("-0.25") },
        { 'test': '43535.4346 ^ 0', 'expected': Number(1) },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalBasicArithmetic.prepare_tests()

if __name__ == '__main__':
    execute_tests()
