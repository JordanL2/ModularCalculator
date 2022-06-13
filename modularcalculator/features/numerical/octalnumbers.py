#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.numerical.bases import BasesFeature
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature
from modularcalculator.numericalengine import NumberType

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
        calculator.funcs['oct'] = FunctionDefinition(
            'Bases',
            'oct',
            'Convert a number into octal',
            ['number'],
            OctalNumbersFeature.func_oct,
            1,
            1,
            'number')
        calculator.funcs['oct'].auto_convert_numerical_result = False
        calculator.add_number_caster('octal', 'Octal', OctalNumbersFeature.number_oct, OctalNumbersFeature.restore_oct)

    oct_prefix = '0o'
    oct_regex = re.compile(r'(\-?' + oct_prefix + r'[0-7]+(\.[0-7]+)?)', re.IGNORECASE)

    def parse_oct(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            oct_match = OctalNumbersFeature.oct_regex.match(next)
            if oct_match:
                octnum = oct_match.group(1)
                decnum = OctalNumbersFeature.number_oct(self, octnum)
                return [LiteralItem(octnum, decnum)], len(octnum), None
        return None, None, None

    def func_oct(self, vals, units, refs, flags):
        return OperationResult(OctalNumbersFeature.force_oct(self, vals[0]))

    def number_oct(self, val):
        if isinstance(val, str) and OctalNumbersFeature.oct_regex.fullmatch(val):
            dec_num = OctalNumbersFeature.oct_to_dec(self, val)
            dec_num = OctalNumbersFeature.force_oct(self, dec_num)
            return dec_num
        return None

    def restore_oct(self, val, opts=None):
        return BasesFeature.number_add_prefix(self, BasesFeature.dec_to_base(self, val, 8), OctalNumbersFeature.oct_prefix)

    def oct_to_dec(self, val):
        return BasesFeature.base_to_dec(self, BasesFeature.number_remove_prefix(self, val, OctalNumbersFeature.oct_prefix), 8)

    def force_oct(self, val):
        if isinstance(val, Number):
            val = val.copy()
            val.number_cast = {'ref': OctalNumbersFeature.restore_oct, 'args': []}
            return val
        return None
