#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *

from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestStructureTerminator(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': "\n((1 + 3)\n/ 2)\n", 'expected': Number('2') },
        { 'test': "1 + 2\n3 + 4", 'expected': Number('7') },
        { 'test': "1\n2", 'expected': Number('2') },
        { 'test': "1 \n2", 'expected': Number('2') },
        { 'test': "\n((1 + 3)\n/ 2)\n", 'expected': Number(2) },
        { 'test': "1 +\n2", 'expected': Number('3') },
        { 'test': "1 + 2\n3 + 4", 'expected': Number('7') },
        { 'test': "1 + 2 + \n3 + 4", 'expected': Number('10') },
        { 'test': "true then\n1\nelse\n2", 'expected': Number('1') },
        { 'test': "true then\n1 + 3\nelse\n2", 'expected': Number('4') },
        { 'test': "true then\n1\nelse\n2\n456", 'expected': Number('456') },
        { 'test': "a = [0, 1]\n(a > 0) then 1 / a else 0", 'expected': [Number('0'), Number('1')] },
        { 'test': "a = [0, 1]\nb = 1 / a\nfilter(b, a > 0)", 'expected': [Number('1')] },

        { 'test': "orbitheight = 36000km\nearthmass = 5.97237e24kg\nearthradius = 6378.1km\ngm = G earthmass\norbitradius = earthradius + orbitheight\ntime = 2 pi (orbitradius^\n\n\n3 /\n\n\n\n gm\n\n\n\n\n\n\n\n)^\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n0.5\ntime to hours",
            'cast': str,
            'expected': ('24.116847271747239529834702110187', 'hours') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestStructureTerminator.prepare_tests()

if __name__ == '__main__':
    execute_tests()
