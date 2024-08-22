#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *

from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStructureInlineFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': "f = { 10 * PARAM1 }\n@f(2)", 'expected': Number('20') },
        { 'test': "f = { \n 10 * PARAM1 \n }\n@f(2)", 'expected': Number('20') },
        { 'test': "f = { 1 + 2 \n 10 * PARAM1 }\n@f(2)", 'expected': Number('20') },
        { 'test': "a = 2\nf = { b = 4 * a \n b * PARAM1 }\n@f(2)", 'expected': Number('16') },
        { 'test': "f = [ {PARAM1*2}, {PARAM1*4} ]\n@f(3)", 'expected': [Number('6'), Number('12')] },
        { 'test': "f = [ {PARAM1*2}, {PARAM1*4} ]\n@f([3, 9])", 'expected': [[Number('6'), Number('18')], [Number('12'), Number('36')]] },

        { 'test': """f = {
    str = PARAM1
    dec = find(str, '.')
    decfound = dec > -1 then true else false

    str = decfound then
        replace(str, '.', '')
        else str
    leadingspaces = (str =~ '^(0+)') then
        length(regexget(str, '^(0+)', 1))
        else 0
    dec = leadingspaces > 1 then
        (dec - (leadingspaces - 1))
        else dec
    str = decfound then
        substr(str, 0, 0) +$ '.' +$ substr(str, 1)
        else str
    dec = decfound then
        dec - 1
        else length(str) - 2

    str +$ '*10^' +$ dec
}
@f(4)""", 'expected': '4*10^-1' },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStructureInlineFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
