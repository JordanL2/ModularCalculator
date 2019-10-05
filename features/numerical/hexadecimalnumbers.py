#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.numerical.bases import BasesFeature
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature
from modularcalculator.numericalengine import NumberType

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
        calculator.add_number_caster('hexadecimal', HexadecimalNumbersFeature.number_hex)

    hex_prefix = '0x'
    hex_regex = re.compile(r'(\-?' + hex_prefix + r'[0-9A-F]+(\.[0-9A-F]+)?)', re.IGNORECASE)

    def parse_hex(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            hex_match = HexadecimalNumbersFeature.hex_regex.match(next)
            if hex_match:
                hexnum = hex_match.group(1)
                clean_hexnum = HexadecimalNumbersFeature.restore_hex(self, HexadecimalNumbersFeature.hex_to_dec(self, hexnum))
                return [LiteralItem(hexnum, clean_hexnum)], len(hexnum), None
        return None, None, None

    def func_hex(self, vals, units, refs, flags):
        return OperationResult(HexadecimalNumbersFeature.restore_hex(self, vals[0]))

    def number_hex(self, val):
        if isinstance(val, str) and HexadecimalNumbersFeature.hex_regex.fullmatch(val):
            dec_num = HexadecimalNumbersFeature.hex_to_dec(self, val)
            return dec_num, NumberType(HexadecimalNumbersFeature.restore_hex)
        return None, None

    def restore_hex(self, val, opts=None):
        return BasesFeature.number_add_prefix(self, BasesFeature.dec_to_base(self, val, 16), HexadecimalNumbersFeature.hex_prefix)

    def hex_to_dec(self, val):
        return BasesFeature.base_to_dec(self, BasesFeature.number_remove_prefix(self, val, HexadecimalNumbersFeature.hex_prefix), 16)
