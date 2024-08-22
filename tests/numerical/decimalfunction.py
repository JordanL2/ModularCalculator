#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalDecimalFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"dec(36z1Z)", 'expected': Number('71') },
        { 'test': r"dec(0b10)", 'expected': Number('2') },
        { 'test': r"dec(0xff)", 'expected': Number('255') },
        { 'test': r"dec(0o77)", 'expected': Number('63') },
        { 'test': r"dec(1.234e1)", 'expected': Number('12.34') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalDecimalFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
