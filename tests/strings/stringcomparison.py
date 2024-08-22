#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStringsStringComparison(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"true ==$ 'True'", 'expected': True },
        { 'test': r"true ==$ 'TRUE'", 'expected': False },
        { 'test': r"'123' ==$ 123", 'expected': True },
        { 'test': r"'abc' ==$ 'ABC'", 'expected': False },

        { 'test': r"'abc' !=$ 'ABC'", 'expected': True },

        { 'test': r"'a' <$ 'b'", 'expected': True },
        { 'test': r"123 <$ 14", 'expected': True },
        { 'test': r"'a' <=$ 'A'", 'expected': False },
        { 'test': r"'a' >$ 'b'", 'expected': False },
        { 'test': r"'b' >=$ 'b'", 'expected': True },

        { 'test': r"true ==~ 'TRUE'", 'expected': True },
        { 'test': r"'abc' ==~ 'ABC'", 'expected': True },

        { 'test': r"'abc' !=~ 'ABC'", 'expected': False },

        { 'test': r"'a' <~ 'A'", 'expected': False },
        { 'test': r"'a' <=~ 'A'", 'expected': True },
        { 'test': r"'a' >~ 'A'", 'expected': False },
        { 'test': r"'a' >=~ 'A'", 'expected': True },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStringsStringComparison.prepare_tests()

if __name__ == '__main__':
    execute_tests()
