#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.exceptions import *
from modularcalculator.features.feature import Feature

import re
from decimal import *


class ExpNumbersFeature(Feature):

    def id():
        return 'numerical.expnumbers'

    def category():
        return 'Numerical'

    def title():
        return 'Exponent Numbers'

    def desc():
        return 'Eg: 10e6'

    def dependencies():
        return []

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('numberexp', ExpNumbersFeature.parse_numberexp)

    numexp_regex = re.compile(r'(\-?\d+(\.\d+)?e\-?\d+)', re.IGNORECASE)

    def parse_numberexp(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items, len(items))
        if prev is None or prev.isop():
            numexp_match = ExpNumbersFeature.numexp_regex.match(next)
            if (numexp_match):
                numexp = numexp_match.group(1)
                num = Decimal(numexp[0:numexp.lower().find('e')])
                exp = Decimal(numexp[numexp.lower().find('e') + 1:])
                num *= (10 ** exp)
                return [LiteralItem(numexp, self.number(num))], len(numexp), None
        return None, None, None
