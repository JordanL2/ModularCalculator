#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStructureExternalFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': "f = './tests/externalfunctions/ext_func_addition'\n@f(5 - 4, 2)", 'expected': Number('3') },
        { 'test': "x=1 \nf = './tests/externalfunctions/ext_func_addition'\n@f(5 - 4, 2) \nx", 'expected': Number('1') },
        { 'test': "f = './tests/externalfunctions/mean'\n@f([1 .. 10])", 'expected': Number('5.5') },
        { 'test': "f = './tests/externalfunctions/acceleration'\n@f(20s, 5m/s^2)", 'expected': (Number('100'), 'meters/second') },
        { 'test': "f = './tests/externalfunctions/distance'\n@f([0, 0], [3, 4])", 'expected': Number('5') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStructureExternalFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
