#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.numerical.bases import BasesFeature
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature
from modularcalculator.numericalengine import NumberType

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
        calculator.funcs['bin'].auto_convert_numerical_result = False
        calculator.add_number_caster('binary', 'Binary', BinaryNumbersFeature.number_bin, BinaryNumbersFeature.restore_bin)

    bin_prefix = '0b'
    bin_regex = re.compile(r'(\-?' + bin_prefix + r'[01]+(\.[01]+)?)', re.IGNORECASE)

    def parse_bin(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            bin_match = BinaryNumbersFeature.bin_regex.match(next)
            if bin_match:
                binnum = bin_match.group(1)
                decnum = BinaryNumbersFeature.number_bin(self, binnum)
                return [LiteralItem(binnum, decnum)], len(binnum), None
        return None, None, None

    def func_bin(self, vals, units, refs, flags):
        return OperationResult(BinaryNumbersFeature.force_bin(self, vals[0]))

    def number_bin(self, val):
        if isinstance(val, str) and BinaryNumbersFeature.bin_regex.fullmatch(val):
            dec_num = BinaryNumbersFeature.bin_to_dec(self, val)
            dec_num.number_cast = {'ref': BinaryNumbersFeature.restore_bin, 'args': [], 'base': 2}
            width = BasesFeature.get_number_width(self, val, BinaryNumbersFeature.bin_prefix)
            dec_num.binary_number_width = width
            return dec_num
        return None

    def restore_bin(self, val, opts=None):
        binnum = BasesFeature.dec_to_base(self, val, 2)
        if hasattr(val, 'binary_number_width'):
            binnum = BasesFeature.force_number_width(self, binnum, val.binary_number_width)
        return BasesFeature.number_add_prefix(self, binnum, BinaryNumbersFeature.bin_prefix)

    def bin_to_dec(self, val):
        return BasesFeature.base_to_dec(self, BasesFeature.number_remove_prefix(self, val, BinaryNumbersFeature.bin_prefix), 2)

    def force_bin(self, val):
        if isinstance(val, Number):
            val = val.copy()
            val.number_cast = {'ref': BinaryNumbersFeature.restore_bin, 'args': [], 'base': 2}
            return val
        return None
