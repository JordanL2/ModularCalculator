#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStringsStringArrayFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"join(['ab', 'b', 'c'], '||')", 'expected': 'ab||b||c' },
        { 'test': r"join(['ab', 'b', 2], '||')", 'expected': 'ab||b||2' },
        { 'test': r"join(['ab', 'b', 2])", 'expected': 'abb2' },

        { 'test': r"split('ab||b||2', '||')", 'expected': ['ab', 'b', '2'] },
        { 'test': r"split(12345367, 3)", 'expected': ['12', '45', '67'] },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStringsStringArrayFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
