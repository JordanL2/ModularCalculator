#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestArraysArrays(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"[1, 2, 3]", 'expected': [Number('1'), Number('2'), Number('3')] },
        { 'test': r"[1 .. 3]", 'expected': [Number('1'), Number('2'), Number('3')] },
        { 'test': r"[-3 .. -1]", 'expected': [Number('-3'), Number('-2'), Number('-1')] },
        { 'test': r"[-1 .. -3 step -1]", 'expected': [Number('-1'), Number('-2'), Number('-3')] },
        { 'test': r"[3 .. 1]", 'expected': [Number('3'), Number('2'), Number('1')] },
        { 'test': r"[3 .. 1 step -1]", 'expected': [Number('3'), Number('2'), Number('1')] },
        { 'test': r"[-1 .. -3]", 'expected': [Number('-1'), Number('-2'), Number('-3')] },
        { 'test': r"[1.5 .. 3.5]", 'expected': [Number('1.5'), Number('2.5'), Number('3.5')] },
        { 'test': r"[1.5 .. 3.5 step 0.5]", 'expected': [Number('1.5'), Number('2'), Number('2.5'), Number('3'), Number('3.5')] },
        { 'test': r"[1 .. 4, 9, 14 .. 20 step 2]", 'expected': [Number('1'), Number('2'), Number('3'), Number('4'), Number('9'), Number('14'), Number('16'), Number('18'), Number('20')] },
        { 'test': r"[1 cm, 2 seconds, 3]", 'expected': [(Number('1') , 'centimeter'), (Number('2'), 'seconds'), Number('3')] },
        { 'test': "a = [1] / 0\nelement(a, 1)", 'expected_exception': {
                                                'exception': ExecutionException,
                                                'message': r"Could not execute operator / with parameters: 1, 0" } },

        { 'test': "a = [1, 2, 3]\na", 'expected': [Number('1'), Number('2'), Number('3')] },
        { 'test': "a = [1, 2, 3]\na = [1, 2, 3]\na", 'expected': [Number('1'), Number('2'), Number('3')] },
        { 'test': r"[1, 2, 3] + 4", 'expected': [Number('5'), Number('6'), Number('7')] },
        { 'test': r"abs([-5, 2 * 3, -3 - 4])", 'expected': [Number('5'), Number('6'), Number('7')] },

        { 'test': "a=[1cm, 3 feet]", 'expected': [(Number('1'), 'centimeter'), (Number('3'), 'feet')] },
        { 'test': "a=[1cm, 3 feet]\nmean(a)\na", 'expected': [(Number('1'), 'centimeter'), (Number('3'), 'feet')] },
        { 'test': r"[20 cm .. 1 meter step 20 cm]", 'expected': [(Number('20') , 'centimeters'), (Number('40') , 'centimeters'), (Number('60') , 'centimeters'), (Number('80') , 'centimeters'), (Number('100') , 'centimeters')] },

        { 'test': r"[[1, 2, 3], [4, 5, 6], [7, 8, 9]]", 'expected': [[Number('1'), Number('2'), Number('3')], [Number('4'), Number('5'), Number('6')], [Number('7'), Number('8'), Number('9')]] },
        { 'test': r"[[1, 2, 3], [4, 5, 6], [7, 8, 9]] + 10", 'expected': [[Number('11'), Number('12'), Number('13')], [Number('14'), Number('15'), Number('16')], [Number('17'), Number('18'), Number('19')]] },
        { 'test': "a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nb = a + 1\nb - a", 'expected': [[Number('1'), Number('1'), Number('1')], [Number('1'), Number('1'), Number('1')], [Number('1'), Number('1'), Number('1')]] },
        { 'test': "[[1, 2, 3], [4, 5, 6], [7, 8, 9]] * [10, 100, 1000]", 'expected': [[Number('10'), Number('20'), Number('30')], [Number('400'), Number('500'), Number('600')], [Number('7000'), Number('8000'), Number('9000')]] },
        { 'test': "a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nelement(a, 1)", 'expected': [Number('1'), Number('2'), Number('3')] },
        { 'test': "a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nelement(element(a, 1), 3)", 'expected': Number('3') },
        { 'test': "a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nelement(a, [1, 3])", 'expected': [[Number('1'), Number('2'), Number('3')], [Number('7'), Number('8'), Number('9')]] },
        { 'test': r"[[1, 2],[4, 5]] meters", 'expected': [[(Number('1'), 'meter'), (Number('2'), 'meters')], [(Number('4'), 'meters'), (Number('5'), 'meters')]] },
        { 'test': r"[[1 meter, 2 seconds],[4 joules, 5 N]]", 'expected': [[(Number('1'), 'meter'), (Number('2'), 'seconds')], [(Number('4'), 'joules'), (Number('5'), 'newtons')]] },
        { 'test': r"[[1..2] meters, [2..4] s]", 'expected': [[(Number('1'), 'meter'), (Number('2'), 'meters')], [(Number('2'), 'seconds'), (Number('3'), 'seconds'), (Number('4'), 'seconds')]] },
        { 'test': r"[[1..2] meters, [2, 4] s] + [[4..5] meters, [3, 4] s]", 'expected': [[(Number('5'), 'meters'), (Number('7'), 'meters')], [(Number('5'), 'seconds'), (Number('8'), 'seconds')]] },

        { 'test': r"[1, 4, 9] < 5", 'expected': [True, True, False] },
        { 'test': "a = [1, 4, 9]\n a < 5", 'expected': [True, True, False] },
        { 'test': "a = [1, 4, 9]\n a < 5 then a else 25", 'expected': [Number('1'), Number('4'), Number('25')] },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestArraysArrays.prepare_tests()

if __name__ == '__main__':
    execute_tests()
