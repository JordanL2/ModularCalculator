#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestBooleanBooleans(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"true", 'expected': True },
        { 'test': r"false", 'expected': False },
        { 'test': r"TRUE ", 'expected': True },
        { 'test': r"false and false", 'expected': False },
        { 'test': r"false and true", 'expected': False },
        { 'test': r"true and false", 'expected': False },
        { 'test': r"true and true", 'expected': True },
        { 'test': r"false or false", 'expected': False },
        { 'test': r"false or true", 'expected': True },
        { 'test': r"true or false", 'expected': True },
        { 'test': r"true or true", 'expected': True },

        { 'test': r"true xor true", 'expected': False },
        { 'test': r"true xor false", 'expected': True },
        { 'test': r"false xor true", 'expected': True },
        { 'test': r"false xor false", 'expected': False },

        { 'test': r"true == true", 'expected': True },
        { 'test': r"false == false", 'expected': True },
        { 'test': r"true == false", 'expected': False },
        { 'test': r"true == 1", 'expected': True },
        { 'test': r"true == 0", 'expected': False },
        { 'test': r"false == 0", 'expected': True },
        { 'test': r"123.00 == 123", 'expected': True },
        { 'test': r"'123' == 123", 'expected': True },
        { 'test': r"'123.00' == 123", 'expected': True },
        { 'test': r"('123' + 0) == 123", 'expected': True },
        { 'test': r"'123' == (123 +$ '')", 'expected': True },

        { 'test': r"123 < 14", 'expected': False },

        { 'test': r"true * true", 'expected': Number(1) },
        { 'test': r"true * false", 'expected': Number(0) },

        { 'test': r"not true", 'expected': False },
        { 'test': r"not false", 'expected': True },
        { 'test': r"not(not true)", 'expected': True },
        { 'test': r"not not true", 'expected': True },
        { 'test': r"not(true == false)", 'expected': True },

        { 'test': r"True then 1 else 2", 'expected': Number(1) },
        { 'test': r"False then 1 else 2", 'expected': Number(2) },
        { 'test': r"True then (False then 3 else 4) else 2", 'expected': Number(4) },
        { 'test': r"(3 > 2) then ((2 > 3) then 3 else 4) else 2", 'expected': Number(4) },
        { 'test': r"3 > 2 then (2 > 3 then 3 else 4) else 2", 'expected': Number(4) },
        { 'test': r"true then not(true or false) else true", 'expected': False },
        { 'test': r"true then 1 + 2 else true", 'expected': Number(3) },
        { 'test': "a = 1\nb = 2\ntrue then a else b = 3\na - b", 'expected': Number(1) },
        { 'test': "a = 1\nb = 2\nfalse then a else b = 3\na - b", 'expected': Number(-2) },
        { 'test': r"false then (1/0) else 2", 'expected': Number(2) },
        { 'test': r"false then 1/0 else 2", 'expected': Number('2') },
        { 'test': r"false and (1/0)", 'expected': False },
        { 'test': r"true or (1/0)", 'expected': True },

        { 'test': r"1 minute == 1 minute", 'expected': True },
        { 'test': r"2 minute < 1 minute", 'expected': False },
        { 'test': r"2 minute <= 1 minute", 'expected': False },
        { 'test': r"2 minute > 1 minute", 'expected': True },
        { 'test': r"2 minute >= 1 minute", 'expected': True },
        { 'test': r"2 minute != 1 minute", 'expected': True },

        { 'test': r"false then 1m else 2cm", 'expected': (Number('2'), 'centimeters') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestBooleanBooleans.prepare_tests()

if __name__ == '__main__':
    execute_tests()
