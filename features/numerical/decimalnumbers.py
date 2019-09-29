#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.features.feature import Feature

import re
from decimal import *


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
        calculator.add_number_caster('decimal', DecimalNumbersFeature.number_decimal)

    num_pattern = r'(\-?\d+(\.\d+)?)'
    num_regex = re.compile(num_pattern)
    num_is_regex = re.compile('^' + num_pattern + '$')

    def parse_number(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items, len(items))
        if prev is None or prev.isop():
            num_match = DecimalNumbersFeature.num_regex.match(next)
            if (num_match):
                num = num_match.group(1)
                return [LiteralItem(num, self.number(Decimal(num))[0])], len(num), None
        return None, None, None

    def number_decimal(self, val):
        if isinstance(val, Decimal):
            return val, False
        if isinstance(val, str) and DecimalNumbersFeature.num_is_regex.match(val):
            return Decimal(val), False
        return None, None
