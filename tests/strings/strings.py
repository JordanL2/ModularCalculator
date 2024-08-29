#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStringsStrings(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"'abc'", 'expected': 'abc' },
        { 'test': "'abc def'", 'expected': 'abc def' },
        { 'test': "'abc\ndef'", 'expected': "abc\ndef" },
        { 'test': r"'123.45'", 'expected': '123.45' },
        { 'test': r"'123.45' * 2", 'expected': Number('246.9') },

        { 'test': "'hello' +$ 'goodbye'", 'expected': 'hellogoodbye' },
        { 'test': r"'hello' +$ 'good\'bye\\'", 'expected': "hellogood'bye\\" },
        { 'test': r"123 +$ 'abc'", 'expected': '123abc' },
        { 'test': r"'123' +$ '456'", 'expected': '123456' },
        { 'test': r"'0b10' +$ '101'", 'expected': '0b10101' },
        { 'test': r"0b10 +$ 101", 'expected': '0b10101' },
        { 'test': r"('12' +$ '3') - 100", 'expected': Number(23) },
        { 'test': r"10 / 3 +$ ''", 'expected': '3.333333333333333333333333333333' },
        { 'test': r"((10 / 3 +$ '') *$ 1) * 3", 'expected': Number('9.999999999999999999999999999999') },

        { 'test': r"'abc' *$ 3", 'expected': 'abcabcabc' },
        { 'test': r"'123' *$ 2", 'expected': '123123' },
        { 'test': r"'123' *$ 0b10", 'expected': '123123' },
        { 'test': r"'abc' *$ '3'", 'expected': 'abcabcabc' },
        { 'test': r"'abc' *$ -1", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute operator *$ with parameters: 'abc', -1 - operator *$ parameter 2 must be of type(s) positive integer" } },
        { 'test': r"'abc' *$ 0.5", 'expected_exception': {
                                'exception': ExecutionException,
                                'message': r"Could not execute operator *$ with parameters: 'abc', 0.5 - operator *$ parameter 2 must be of type(s) positive integer" } },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStringsStrings.prepare_tests()

if __name__ == '__main__':
    execute_tests()
