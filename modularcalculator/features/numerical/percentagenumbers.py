#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.number import *
from modularcalculator.features.feature import Feature

import re


class PercentageNumberFeature(Feature):

    perc_regex = re.compile(r'(\-?\d+(\.\d+)?%)')

    def id():
        return 'numerical.percentagenumbers'

    def category():
        return 'Numerical'

    def title():
        return 'Percentage Numbers'

    def desc():
        return 'Eg: 67%'

    def dependencies():
        return ['numerical.decimalnumbers']

    def after():
        return ['numerical.numericalrepresentation']

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('percentagenumber', PercentageNumberFeature.parse_percentagenumber)
        calculator.add_number_type(PercentageNumericalRepresentation)

    def parse_percentagenumber(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            perc_match = PercentageNumberFeature.perc_regex.match(next)
            if (perc_match):
                numperc = perc_match.group(1)
                decnum = PercentageNumericalRepresentation.parse(self, numperc)
                return [LiteralItem(numperc, decnum)], len(numperc), None
        return None, None, None


class PercentageNumericalRepresentation:

    @staticmethod
    def name():
        return 'percentage'

    @staticmethod
    def desc():
        return 'Percentage'

    @staticmethod
    def parse(calculator, val):
        numperc_regex = PercentageNumberFeature.perc_regex
        if isinstance(val, str) and numperc_regex.fullmatch(val):
            numperc_match = numperc_regex.match(val)
            numperc = numperc_match.group(1)
            symbol = '%'
            num = Number(numperc[0:numperc.lower().find(symbol)])
            num /= Number(100)
            num = PercentageNumericalRepresentation.convert_to(calculator, num)
            return num

        return None

    @staticmethod
    def to_string(calculator, val):
        val *= Number(100)
        val.number_cast = None
        return val.to_string(calculator) + '%'

    @staticmethod
    def convert_to(calculator, val):
        if isinstance(val, Number):
            val = val.copy()
            val.number_cast = {'to_string': PercentageNumericalRepresentation.to_string, 'places_offset': 2}
            return val
        return None
