#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestNumericalStatisticalFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': 'min([1, 2, 3])', 'expected': Number('1') },
        { 'test': '1 + (( min([ 2, -1,  3 ])))', 'expected': Number('0') },
        { 'test': '( min([ min([4,5,6]), min([2,8,9]),  min([3,7,8]) ]))', 'expected': Number('2') },
        { 'test': '( min([ min([4,5,6]), min([2,8,9])+1,  min([3,7,8]) ]))', 'expected': Number('3') },
        { 'test': '( min([ min([4,5,6]), 2 * min([2,8,9]) - 3,  min([3,7,8]) ]))', 'expected': Number('1') },
        { 'test': '( min([ min([4,5,6]), 2 * min([2,8,9])-3,  min([3,7,8]) ]))', 'expected': Number('1') },
        { 'test': '(min([min([4,5,6]),((2 * min([2,8,9])-(3 + 1))),min([3,7,8]) ]))', 'expected': Number('0') },
        { 'test': r"max([3, 5, 7])", 'expected': Number('7') },
        { 'test': r"mean([2, 3, 5, 6])", 'expected': Number('4') },
        { 'test': r"median([6, 1, 9])", 'expected': Number('6') },
        { 'test': r"mode([1, 1, 2, 4])", 'expected': Number('1') },
        { 'test': r"stdev([1, 2, 3, 4])", 'expected': Number(645497224367902814196544233297066601805486950881931804431262294352247181989496505586547896143112253, 500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000) },
        { 'test': r"sum([1, 2, 3, 4])", 'expected': Number('10') },
        { 'test': r"sum(([10]))", 'expected': Number('10') },
        { 'test': r"sum([(10)])", 'expected': Number('10') },
        { 'test': r"sum([(1), 2, 3])", 'expected': Number('6') },
        { 'test': r"sum(([(1), 2, 3]))", 'expected': Number('6') },
        { 'test': r"sum([1, (2), 3])", 'expected': Number('6') },
        { 'test': r"sum([1, 2, (3)])", 'expected': Number('6') },
        { 'test': r"sum([1, 2, (3) + 2])", 'expected': Number('8') },
        { 'test': r"sum([(1), 2, 3 + 2])", 'expected': Number('8') },
        { 'test': r"sum([ (10) ])", 'expected': Number('10') },
        { 'test': r"sum( [ (10) ] )", 'expected': Number('10') },
        { 'test': r"sum([( 10 )])", 'expected': Number('10') },
        { 'test': r"sum( [( 10 )] )", 'expected': Number('10') },

        { 'test': r"mean([1, 2, 6])", 'expected': Number('3') },
        { 'test': r"mean([1 .. 100])", 'expected': Number('50.5') },
        { 'test': "a=[1 .. 100]\nmean(a)", 'expected': Number('50.5') },

        { 'test': r"min([1 metre, 40 cm])", 'expected': (Number('40'), 'centimeters') },
        { 'test': r"max([40 cm, 1 metre])", 'expected': (Number('1'), 'meter') },

        { 'test': r"min([0, 3, 6], [4, 2, 5])", 'expected': [Number('0'), Number('2'), Number('5')] },
        { 'test': r"min(3, [4, 2, 5])", 'expected': [Number('3'), Number('2'), Number('3')] },
        { 'test': r"min([0, 3, 6], 4)", 'expected': [Number('0'), Number('3'), Number('4')] },
        { 'test': r"min([0, 3, 6], [1, 2, 3], [6, 4, 1])", 'expected': [Number('0'), Number('2'), Number('1')] },
        { 'test': r"min(5, 2, 3, 1, 4)", 'expected': Number('1') },

        { 'test': r"stdev([1, 2, 3, 4])", 'expected': Number('645497224367902814196544233297066601805486950881931804431262294352247181989496505586547896143112253', '500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestNumericalStatisticalFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
