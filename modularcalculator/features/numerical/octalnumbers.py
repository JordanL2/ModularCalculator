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

    def after():
        return ['numerical.numericalrepresentation']

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
        calculator.add_number_type(OctalNumericalRepresentation)

    oct_prefix = '0o'
    oct_regex = re.compile(r'(\-?' + oct_prefix + r'[0-7]+(\.[0-7]+)?)', re.IGNORECASE)

    def parse_oct(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            oct_match = OctalNumbersFeature.oct_regex.match(next)
            if oct_match:
                octnum = oct_match.group(1)
                decnum = OctalNumericalRepresentation.parse(self, octnum)
                return [LiteralItem(octnum, decnum)], len(octnum), None
        return None, None, None

    def func_oct(self, vals, units, refs, flags):
        return OperationResult(OctalNumericalRepresentation.convert_to(self, vals[0]))


class OctalNumericalRepresentation:

    @staticmethod
    def name():
        return 'octal'

    @staticmethod
    def desc():
        return 'Octal'

    @staticmethod
    def parse(calculator, val):
        if isinstance(val, str) and OctalNumbersFeature.oct_regex.fullmatch(val):
            dec_num = BasesFeature.base_to_dec(calculator, BasesFeature.number_remove_prefix(calculator, val, OctalNumbersFeature.oct_prefix), 8)
            dec_num = OctalNumericalRepresentation.convert_to(calculator, dec_num)
            return dec_num
        return None

    @staticmethod
    def to_string(calculator, val):
        return BasesFeature.number_add_prefix(calculator, BasesFeature.dec_to_base(calculator, val, 8), OctalNumbersFeature.oct_prefix)

    @staticmethod
    def convert_to(calculator, val):
        if isinstance(val, Number):
            val = val.copy()
            val.number_cast = {'ref': OctalNumericalRepresentation.to_string, 'args': [], 'base': 8}
            return val
        return None
