#!/usr/bin/python3

from modularcalculator.tests.testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *

import pprint


pp = pprint.PrettyPrinter(indent=4)

print("BasicCalculator tests:")
c = ModularCalculator('Basic')
hl = SyntaxHighlighter()

#print("Presets:", c.list_presets(), "\n")
#print("Features:")
#pp.pprint(c.list_features())
#print("\n")

tests = [
    { 'test': '123', 'expected': Decimal('123') },
    { 'test': '123+456', 'expected': Decimal('579') },
    { 'test': '123-1', 'expected': Decimal('122') },
    { 'test': '2+3*4', 'expected': Decimal('14') },
    { 'test': '2+-3/4', 'expected': Decimal('1.25') },
    { 'test': '2+3^3', 'expected': Decimal('29') },
    { 'test': '1+2*3-4', 'expected': Decimal('3') },
    { 'test': '10/5*2', 'expected': Decimal('4') },
    { 'test': r"10/3", 'expected': Decimal('3.333333333333333333333333333333') },
    { 'test': r"10/3*3", 'expected': Decimal('10') },
#    { 'test': r"", 'expected': '' },
]

tester = TestRunner(CalculatorException)
tester.test(c.calculate, tests)
