#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.features.feature import Feature
from modularcalculator.objects.number import *

import re


class DecimalNumbersFeature(Feature):

    def id():
        return 'numerical.decimalnumbers'

    def category():
        return 'Numerical'

    def title():
        return 'Decimal Numbers'

    def desc():
        return 'Standard decimal numbers'

    def dependencies():
        return []

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('number', DecimalNumbersFeature.parse_number)
        calculator.add_number_caster('decimal', 'Decimal', DecimalNumbersFeature.number_decimal, None)

    num_pattern = r'(\-?\d+(\.\d+)?)'
    num_regex = re.compile(num_pattern)
    num_is_regex = re.compile('^' + num_pattern + '$')

    def parse_number(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            num_match = DecimalNumbersFeature.num_regex.match(next)
            if (num_match):
                num = num_match.group(1)
                return [LiteralItem(num, self.number(Number(num)))], len(num), None
        return None, None, None

    def number_decimal(self, val):
        if isinstance(val, Number):
            return val
        if isinstance(val, str) and DecimalNumbersFeature.num_is_regex.match(val):
            return Number(val)
        return None
