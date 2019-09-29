#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.numerical.bases import BasesFeature
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature

import re


class BinaryNumbersFeature(Feature):

    def id():
        return 'numerical.binarynumbers'

    def category():
        return 'Numerical'

    def title():
        return 'Binary Numbers'

    def desc():
        return 'Eg: 0b10101'

    def dependencies():
        return ['numerical.bases']

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('number_bin', BinaryNumbersFeature.parse_bin)
        calculator.funcs['bin'] = FunctionDefinition(
            'Bases', 
            'bin', 
            'Convert a number into binary',
            ['number'],
            BinaryNumbersFeature.func_bin, 
            1, 
            1, 
            'number')
        calculator.add_number_caster('binary', BinaryNumbersFeature.number_bin)

    bin_prefix = '0b'
    bin_regex = re.compile(r'(\-?' + bin_prefix + r'[01]+(\.[01]+)?)', re.IGNORECASE)

    def parse_bin(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items, len(items))
        if prev is None or prev.isop():
            bin_match = BinaryNumbersFeature.bin_regex.match(next)
            if bin_match:
                binnum = bin_match.group(1)
                return [LiteralItem(binnum, binnum)], len(binnum), None
        return None, None, None

    def func_bin(self, vals, units, refs, flags):
        return OperationResult(BasesFeature.number_add_prefix(self, BasesFeature.dec_to_base(self, vals[0], 2), BinaryNumbersFeature.bin_prefix))

    def number_bin(self, val):
        if isinstance(val, str) and BinaryNumbersFeature.bin_regex.fullmatch(val):
            return (BasesFeature.base_to_dec(self, BasesFeature.number_remove_prefix(self, val, BinaryNumbersFeature.bin_prefix), 2))
        return None
