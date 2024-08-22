#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStringsRegex(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"'ABC' =~ '\\w'", 'expected': True },
        { 'test': r"'ABC' =~ '\\d'", 'expected': False },
        { 'test': r"'ABC123abc' =~ '\\d{3}'", 'expected': True },
        { 'test': r"'ABC123abc' =~ '\\d{4}'", 'expected': False },
        { 'test': r"'ABC123abc' =~ '^\\w{3}\\d{3}\\w{3}$'", 'expected': True },
        { 'test': r"'ABC123abc' =~ '^\\w{3}\\d{3}\\w{2}$'", 'expected': False },

        { 'test': r"'ABC' !~ '\\w'", 'expected': False },
        { 'test': r"'ABC' !~ '\\d'", 'expected': True },

        { 'test': r"regexget('123ABC123DEF123GHI123', '[A-Z]+')", 'expected': ['ABC', 'DEF', 'GHI'] },
        { 'test': r"regexget('123456', '[A-Z]+')", 'expected': [] },
        { 'test': r"regexget('123ABC456', '\\d+', 2)", 'expected': '456' },

        { 'test': r"regexsplit('123ABC456XYZ789', '[A-Z]+')", 'expected': ['123', '456', '789'] },
        { 'test': r"regexsplit('123456', '[A-Z]+')", 'expected': ['123456'] },
        { 'test': r"regexsplit('123A456XY789', '[A-Z]')", 'expected': ['123', '456', '', '789'] },
        { 'test': r"regexsplit('123A456XY789Z', '[A-Z]')", 'expected': ['123', '456', '', '789', ''] },
        { 'test': r"regexsplit('Z123A456XY789Z', '[A-Z]')", 'expected': ['', '123', '456', '', '789', ''] },
        { 'test': r"regexsplit('Z123A456XY789Z', '[A-Z]+')", 'expected': ['', '123', '456', '789', ''] },

        { 'test': r"regexsub('123ABC123', '[A-Z]+', 'defg')", 'expected': '123defg123' },
        { 'test': r"regexsub('123456', '[A-Z]+', 'defg')", 'expected': '123456' },
        { 'test': r"regexsub('123ABC456XYZ789', '[A-Z]+', 'defg')", 'expected': '123defg456defg789' },
        { 'test': r"regexsub('123ABC456XYZ789', '[A-Z]+', 'defg', 1)", 'expected': '123defg456XYZ789' },
        { 'test': r"regexsub('123456789', '[A-Z]+', 'defg')", 'expected': '123456789' },

        { 'test': r"regexcount('1abc2def3ghi4', '[a-z]{3}')", 'expected': Number(3) },
        { 'test': r"regexcount('12345', '[a-z]{3}')", 'expected': Number(0) },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStringsRegex.prepare_tests()

if __name__ == '__main__':
    execute_tests()
