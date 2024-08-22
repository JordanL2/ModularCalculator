#!/usr/bin/python3

if __name__ == '__main__':
    from tests.testrunner import *
else:
    from testrunner import *

from modularcalculator.modularcalculator import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class TestUnitsUnitFunctions(CalculatorTestCase):

    c = ModularCalculator('Computing')
    tests = [
        { 'test': r"format(1 hour + 23 minutes + 45 seconds)", 'expected': '1 hour, 23 minutes, 45 seconds' },
        { 'test': r"format(61s)", 'expected': '1 minute, 1 second' },
        { 'test': r"format(2 weeks + 3 hour + 23 minutes + 45 seconds)", 'expected': '14 days, 3 hours, 23 minutes, 45 seconds' },
        { 'test': r"format(1 hour + 23 minutes + 0.001 seconds)", 'expected': '1 hour, 23 minutes, 1 millisecond' },
        { 'test': r"format(456765.34533646 s)", 'expected': '5 days, 6 hours, 52 minutes, 45.34533646 seconds' },
        { 'test': r"format(456765.34533646 s, si)", 'expected': '456765.34533646 seconds' },
        { 'test': r"format(456765.34533646 minutes, si)", 'expected': '27405920.7201876 seconds' },
        { 'test': r"format(456765000.34533646 ms, gregorian)", 'expected': '5 days, 6 hours, 52 minutes, 45.00034533646 seconds' },
        { 'test': r"format(0.000000046 ms)", 'expected': '46 picoseconds' },
        { 'test': r"format(1.000000001 ms)", 'expected': '1.000000001 milliseconds' },
        { 'test': r"format(0.001000000001 ms)", 'expected': '1.000000001 microseconds' },
        { 'test': r"format(1000000001 ms, si)", 'expected': '1000000.001 seconds' },
        { 'test': r"format(1000000000 ms, si)", 'expected': '1000000 seconds' },
        { 'test': r"format(1000000000 ms)", 'expected': '11 days, 13 hours, 46 minutes, 40 seconds' },
        { 'test': r"format(456765.345336 ms, si)", 'expected': '456.765345336 seconds' },
        { 'test': r"format(1.543 miles)", 'expected': '1 mile, 955 yards, 2 feet, 0.48 inches' },
        { 'test': r"format(1.543 long tons)", 'expected': '1 long ton, 86 stone, 12 pounds, 5 ounces, 52.5 grains' },
        { 'test': r"format(1.543 short tons)", 'expected': '1 short ton, 1086 pounds' },
        { 'test': r"format(1.54467 short tons)", 'expected': '1 short ton, 1089 pounds, 5 ounces, 192.5 grains' },
        { 'test': r"format(1.543 tons)", 'expected': '1 short ton, 1086 pounds' },
        { 'test': r"format(12345.6789kg)", 'expected': '12 tonnes, 345.6789 kilograms' },
        { 'test': r"format(1234 MB)", 'expected': '1.234 gigabytes' },
        { 'test': r"format(1234000000 bytes)", 'expected': '1.234 gigabytes' },
        { 'test': r"format(1234005000 bytes)", 'expected': '1.234005 gigabytes' },

        { 'test': r"compact(40 TW h / yr)", 'expected': (Number(2000000, 438291), 'gigawatts') },
    ]

    def category(self):
        return 'Computing'

    def setUp(self):
        self.c = ModularCalculator('Computing')


TestUnitsUnitFunctions.prepare_tests()

if __name__ == '__main__':
    execute_tests()
