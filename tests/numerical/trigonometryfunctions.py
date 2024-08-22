#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalTrigonometryFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"sin(1)", 'expected': Number(3789648413623927, 4503599627370496) },
        { 'test': r"cos(1)", 'expected': Number(1216652631687587, 2251799813685248) },
        { 'test': r"tan(1)", 'expected': Number(3506970424209875, 2251799813685248) },
        { 'test': r"sinh(1)", 'expected': Number(2646317828889793, 2251799813685248) },
        { 'test': r"cosh(1)", 'expected': Number(434338585747285, 281474976710656) },
        { 'test': r"tanh(1)", 'expected': Number(1714957578484965, 2251799813685248) },
        { 'test': r"asin(1)", 'expected': Number(884279719003555, 562949953421312) },
        { 'test': r"acos(1)", 'expected': Number(0) },
        { 'test': r"atan(1)", 'expected': Number(884279719003555, 1125899906842624) },
        { 'test': r"asinh(1)", 'expected': Number(7938707516150823, 9007199254740992) },
        { 'test': r"acosh(1)", 'expected': Number(0) },
        { 'test': r"atanh(0)", 'expected': Number(0) },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalTrigonometryFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
