#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *

from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestUnitsUnitConstants(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': "G", 'expected': (Number('0.0000000000667408'), 'meters^3/(kilogram second^2)') },
        { 'test': "earthgravity", 'expected': (Number('9.80665'), 'meters/second^2') },
        { 'test': "speedoflight", 'expected': (Number('299792458'), 'meters/second') },
        { 'test': "Planck", 'expected': (Number('0.000000000000000000000000000000000662607015'), 'joule seconds') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestUnitsUnitConstants.prepare_tests()

if __name__ == '__main__':
    execute_tests()
