#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.numerical.bases import BasesFeature
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature

import re


class HexadecimalNumbersFeature(Feature):

    def id():
        return 'numerical.hexadecimalnumbers'

    def category():
        return 'Numerical'

    def title():
        return 'Hexadecimal Numbers'

    def desc():
        return 'Eg: 0x1F'

    def dependencies():
        return ['numerical.bases']

    def after():
        return ['numerical.numericalrepresentation']

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('number_hex', HexadecimalNumbersFeature.parse_hex)
        calculator.funcs['hex'] = FunctionDefinition(
            'Bases',
            'hex',
            'Convert a number into hexadecimal',
            ['number'],
            HexadecimalNumbersFeature.func_hex,
            1,
            1,
            'number')
        calculator.funcs['hex'].auto_convert_numerical_result = False
        calculator.add_number_type(HexadecimalNumericalRepresentation)

    hex_prefix = '0x'
    hex_regex = re.compile(r'(\-?' + hex_prefix + r'[0-9A-F]+(\.[0-9A-F]+)?)', re.IGNORECASE)

    def parse_hex(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            hex_match = HexadecimalNumbersFeature.hex_regex.match(next)
            if hex_match:
                hexnum = hex_match.group(1)
                decnum = HexadecimalNumericalRepresentation.convert_from(self, hexnum)
                return [LiteralItem(hexnum, decnum)], len(hexnum), None
        return None, None, None

    def func_hex(self, vals, units, refs, flags):
        return OperationResult(HexadecimalNumericalRepresentation.convert_to(self, vals[0]))


class HexadecimalNumericalRepresentation:

    @staticmethod
    def name():
        return 'hexadecimal'

    @staticmethod
    def desc():
        return 'Hexadecimal'

    @staticmethod
    def convert_to(calculator, val):
        return BasesFeature.number_add_prefix(calculator, BasesFeature.dec_to_base(calculator, val, 16), HexadecimalNumbersFeature.hex_prefix)

    @staticmethod
    def convert_from(calculator, val):
        if isinstance(val, str) and HexadecimalNumbersFeature.hex_regex.fullmatch(val):
            dec_num = BasesFeature.base_to_dec(calculator, BasesFeature.number_remove_prefix(calculator, val, HexadecimalNumbersFeature.hex_prefix), 16)
            dec_num.number_cast = {'ref': HexadecimalNumericalRepresentation.convert_to, 'args': [], 'base': 16}
            return dec_num
        return None
