#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestArraysArrayFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"concat([1, 2, 3], [4, 5])", 'expected': [Number('1'), Number('2'), Number('3'), Number('4'), Number('5')] },

        { 'test': r"count([2 .. 6 step 2])", 'expected': Number('3') },

        { 'test': r"element([1, 2, 3], 2)", 'expected': Number('2') },
        { 'test': r"element([1, 2, 3, 4, 5], [2 .. 4])", 'expected': [Number('2'), Number('3'), Number('4')] },
        { 'test': r"element([1 cm, 2 seconds, 3 metres], 2)", 'expected': (Number('2'), 'seconds') },
        { 'test': "a = [1] / 0\nelement(a, 1)", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with parameters: 1, 0" } },
        { 'test': "a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nelement(a, 1)", 'expected': [Number('1'), Number('2'), Number('3')] },
        { 'test': "a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nelement(element(a, 1), 3)", 'expected': Number('3') },
        { 'test': "a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nelement(a, [1, 3])", 'expected': [[Number('1'), Number('2'), Number('3')], [Number('7'), Number('8'), Number('9')]] },

        { 'test': "a = [1 .. 7]\nfilter(a, a % 2 == 0)", 'expected': [Number('2'), Number('4'), Number('6')] },

        { 'test': r"reverse([4, 2, 3, 1])", 'expected': [Number('1'), Number('3'), Number('2'), Number('4')] },

        { 'test': r"sort([4, 2, 3, 1])", 'expected': [Number('1'), Number('2'), Number('3'), Number('4')] },
        { 'test': r"sort([4 cm, 2 meters, 3 feet])", 'expected': [(Number('4'), 'centimeters'), (Number('3'), 'feet'), (Number('2'), 'meters')] },
        { 'test': r"sort(5, 2, 3, 1, 4)", 'expected': [Number('1'), Number('2'), Number('3'), Number('4'), Number('5')] },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestArraysArrayFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
