#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalNumericalRepresentation(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"255 as hexadecimal", 'cast': str, 'expected': '0xFF' },
        { 'test': r"0xFF as decimal", 'cast': str, 'expected': '255' },
        { 'test': r"255 as binary", 'cast': str, 'expected': '0b11111111' },
        { 'test': r"0b11111111 as decimal", 'cast': str, 'expected': '255' },
        { 'test': r"255 as octal", 'cast': str, 'expected': '0o377' },
        { 'test': r"0o377 as decimal", 'cast': str, 'expected': '255' },
        { 'test': r"255 as scientific", 'cast': str, 'expected': '2.55E2' },
        { 'test': r"2.55E2 as decimal", 'cast': str, 'expected': '255' },
        { 'test': r"2.5 as percentage", 'cast': str, 'expected': '250%' },
        { 'test': r"250% as decimal", 'cast': str, 'expected': '2.5' },
        { 'test': "b = 255\nb as binary", 'cast': str, 'expected': '0b11111111' },
        { 'test': "b = 255 as hexadecimal\nb as binary", 'cast': str, 'expected': '0b11111111' },
        { 'test': r"(255 as hexadecimal) as binary", 'cast': str, 'expected': '0b11111111' },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalNumericalRepresentation.prepare_tests()

if __name__ == '__main__':
    execute_tests()
