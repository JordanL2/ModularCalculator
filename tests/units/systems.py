#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *

from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *
from modularcalculator.features.units.systems import *


class TestUnitsSystems(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': "si", 'expected': UnitSystemValue('si') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestUnitsSystems.prepare_tests()

if __name__ == '__main__':
    execute_tests()
