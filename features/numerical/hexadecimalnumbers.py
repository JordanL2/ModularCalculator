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

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('number_hex', HexadecimalNumbersFeature.parse_hex)
        calculator.funcs['hex'] = FunctionDefinition(
            'Bases', 
            'hex', 
            'Convert a number into hexadecimal',
            'hex(number)',
            HexadecimalNumbersFeature.func_hex, 
            1, 
            1, 
            'number')
        calculator.add_number_caster('hexadecimal', HexadecimalNumbersFeature.number_hex)

    hex_prefix = '0x'
    hex_regex = re.compile(r'(\-?' + hex_prefix + r'[0-9A-F]+(\.[0-9A-F]+)?)', re.IGNORECASE)

    def parse_hex(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items, len(items))
        if prev is None or prev.isop():
            hex_match = HexadecimalNumbersFeature.hex_regex.match(next)
            if hex_match:
                hexnum = hex_match.group(1)
                try:
                    decnum = self.number(hexnum)
                    return [LiteralItem(hexnum, decnum)], len(hexnum), None
                except CalculatorException as err:
                    raise ParsingException(err.message, [], next)
        return None, None, None

    def func_hex(self, vals, units, refs, flags):
        return OperationResult(BasesFeature.number_add_prefix(self, BasesFeature.dec_to_base(self, vals[0], 16), HexadecimalNumbersFeature.hex_prefix))

    def number_hex(self, val):
        if isinstance(val, str) and HexadecimalNumbersFeature.hex_regex.fullmatch(val):
            return BasesFeature.base_to_dec(self, BasesFeature.number_remove_prefix(self, val, HexadecimalNumbersFeature.hex_prefix), 16)
        return None
