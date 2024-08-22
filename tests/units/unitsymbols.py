#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *

from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestUnitsUnitSymbols(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"-200 °C to K", 'expected': (Number('73.15'), 'kelvin') },
        { 'test': r"20 °C to °F", 'expected': (Number('68'), 'Fahrenheit') },
        { 'test': r"20000 °C to °F", 'expected': (Number('36032'), 'Fahrenheit') },
        { 'test': r"68 °F to °C", 'expected': (Number('20'), 'Celsius') },
        { 'test': r"1 meter + 23 cm", 'expected': (Number('1.23'), 'meters') },
        { 'test': r"1 meter + 23 µm", 'expected': (Number('1.000023'), 'meters') },
        { 'test': r"1 meter + 23 nm", 'expected': (Number('1.000000023'), 'meters') },
        { 'test': r"1K + 1K", 'expected': (Number('2'), 'kelvin') },
        { 'test': r"1°C + 1°C", 'expected': (Number('2'), 'Celsius') },
        { 'test': r"1K + 1°C", 'expected': (Number('2'), 'kelvin') },
        { 'test': r"1°C + 1K", 'expected': (Number('2'), 'Celsius') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestUnitsUnitSymbols.prepare_tests()

if __name__ == '__main__':
    execute_tests()
