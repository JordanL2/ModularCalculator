#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.numerical.bases import BasesFeature
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature

import re


class OctalNumbersFeature(Feature):

    def id():
        return 'numerical.octalnumbers'

    def category():
        return 'Numerical'

    def title():
        return 'Octal Numbers'

    def desc():
        return 'Eg: 0o77'

    def dependencies():
        return ['numerical.bases']

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('number_oct', OctalNumbersFeature.parse_oct)
        calculator.funcs['oct'] = FunctionDefinition('Bases', 'oct', OctalNumbersFeature.func_oct, 1, 1, 'number')
        calculator.add_number_caster('octal', OctalNumbersFeature.number_oct)

    oct_prefix = '0o'
    oct_regex = re.compile(r'(\-?' + oct_prefix + r'[0-7]+(\.[0-7]+)?)', re.IGNORECASE)

    def parse_oct(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items, len(items))
        if prev is None or prev.isop():
            oct_match = OctalNumbersFeature.oct_regex.match(next)
            if oct_match:
                octnum = oct_match.group(1)
                try:
                    decnum = self.number(octnum)
                    return [LiteralItem(octnum, decnum)], len(octnum), None
                except CalculatorException as err:
                    raise ParsingException(err.message, [], next)
        return None, None, None

    def func_oct(self, vals, units, refs, flags):
        return OperationResult(BasesFeature.number_add_prefix(self, BasesFeature.dec_to_base(self, vals[0], 8), OctalNumbersFeature.oct_prefix))

    def number_oct(self, val):
        if isinstance(val, str) and OctalNumbersFeature.oct_regex.fullmatch(val):
            return BasesFeature.base_to_dec(self, BasesFeature.number_remove_prefix(self, val, OctalNumbersFeature.oct_prefix), 8)
        return None
