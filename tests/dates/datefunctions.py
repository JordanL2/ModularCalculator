#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *
from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestDatesDateFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': "dateformat('2012-01-02')", 'expected': 'Monday, 02-Jan-2012' },
        { 'test': "dateformat('2012-01-02T11:45:56')", 'expected': 'Monday, 02-Jan-2012 at 11:45:56' },
        { 'test': "dateformat('2012-01-02T11:45:56.123456')", 'expected': 'Monday, 02-Jan-2012 at 11:45:56.123456' },
        { 'test': "dateformat('2012-01-02+0100')", 'expected': 'Monday, 02-Jan-2012 (+0100)' },
        { 'test': "dateformat('2012-01-02T11:45:56-0430')", 'expected': 'Monday, 02-Jan-2012 at 11:45:56 (-0430)' },
        { 'test': "dateformat('2012-01-02T11:45:56.123456+1256')", 'expected': 'Monday, 02-Jan-2012 at 11:45:56.123456 (+1256)' },

        { 'test': "dateadd('2012-01-02T11:45:56', 5 seconds)", 'expected': '2012-01-02T11:46:01' },
        { 'test': "dateadd('2012-01-02T11:45:56', 0.123456 seconds)", 'expected': '2012-01-02T11:45:56.123456' },
        { 'test': "dateadd('2012-01-02T11:45:56', 5 hours)", 'expected': '2012-01-02T16:45:56' },
        { 'test': "dateadd('2012-01-02T11:45:56', 5 weeks)", 'expected': '2012-02-06T11:45:56' },
        { 'test': "dateadd(dateadd('0900-01-01', 1 year), 1 year)", 'expected': '0902-01-01T11:38:24' },

        { 'test': "datesubtract('2012-01-02T11:45:56', 5 seconds)", 'expected': '2012-01-02T11:45:51' },

        { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-04T11:45:56', days)", 'expected': (Number('2'), 'days') },
        { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-01T11:45:56', hours)", 'expected': (Number('24'), 'hours') },
        { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-02T11:45:56.123456', seconds)", 'expected': (Number('0.123456'), 'seconds') },
        { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-02T11:45:56.123456')", 'expected': (Number('0.123456'), 'seconds') },
        { 'test': "datedifference('2012-01-02T11:45:56', '2012-01-02T11:45:56.123456', microseconds)", 'expected': (Number('123456'), 'microseconds') },
        { 'test': "datedifference('2012-01-02-0200', '2012-01-02T04:00:00+0100', hours)", 'expected': (Number('1'), 'hour') },
        { 'test': "datedifference('2012-01-02T11:45:56-0200', '2012-01-02T11:45:56+0100', hours)", 'expected': (Number('3'), 'hours') },
        { 'test': "datedifference('2012-01-02-0200', '2012-01-02T11:45:56.123456+0100', microseconds)", 'expected': (Number('31556123456'), 'microseconds') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestDatesDateFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
