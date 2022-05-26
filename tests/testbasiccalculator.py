#!/usr/bin/python3

from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestBasicCalculator(CalculatorTestCase):

    c = ModularCalculator('Basic')
    tests = [
        { 'test': '123', 'expected': Number(123) },
        { 'test': '123+456', 'expected': Number(579) },
        { 'test': '123-1', 'expected': Number(122) },
        { 'test': '2+3*4', 'expected': Number(14) },
        { 'test': '2+-3/4', 'expected': Number('1.25') },
        { 'test': '2+3^3', 'expected': Number(29) },
        { 'test': '1+2*3-4', 'expected': Number(3) },
        { 'test': '10/5*2', 'expected': Number(4) },
        { 'test': r"10/3", 'expected': Number(10, 3) },
        { 'test': r"10/3*3", 'expected': Number(10) },
    #    { 'test': r"", 'expected': '' },
    ]

    def setUp(self):
        self.c = ModularCalculator('Basic')


TestBasicCalculator.prepare_tests()

if __name__ == '__main__':
    execute_tests()
