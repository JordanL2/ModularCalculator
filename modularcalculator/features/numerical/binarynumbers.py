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

    def after():
        return ['numerical.numericalrepresentation']

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
        calculator.add_number_type(BinaryNumericalRepresentation)

    bin_prefix = '0b'
    bin_regex = re.compile(r'(\-?' + bin_prefix + r'[01]+(\.[01]+)?)', re.IGNORECASE)

    def parse_bin(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            bin_match = BinaryNumbersFeature.bin_regex.match(next)
            if bin_match:
                binnum = bin_match.group(1)
                decnum = BinaryNumericalRepresentation.convert_from(self, binnum)
                return [LiteralItem(binnum, decnum)], len(binnum), None
        return None, None, None

    def func_bin(self, vals, units, refs, flags):
        return OperationResult(BinaryNumericalRepresentation.convert_to(self, vals[0]))


class BinaryNumericalRepresentation:

    @staticmethod
    def name():
        return 'binary'

    @staticmethod
    def desc():
        return 'Binary'

    @staticmethod
    def convert_to(calculator, val):
        binnum = BasesFeature.dec_to_base(calculator, val, 2)
        if hasattr(val, 'binary_number_width'):
            binnum = BasesFeature.force_number_width(calculator, binnum, val.binary_number_width)
        return BasesFeature.number_add_prefix(calculator, binnum, BinaryNumbersFeature.bin_prefix)

    @staticmethod
    def convert_from(calculator, val):
        if isinstance(val, str) and BinaryNumbersFeature.bin_regex.fullmatch(val):
            dec_num = BasesFeature.base_to_dec(calculator, BasesFeature.number_remove_prefix(calculator, val, BinaryNumbersFeature.bin_prefix), 2)
            dec_num.number_cast = {'ref': BinaryNumericalRepresentation.convert_to, 'args': [], 'base': 2}
            width = BasesFeature.get_number_width(calculator, val, BinaryNumbersFeature.bin_prefix)
            dec_num.binary_number_width = width
            return dec_num
        return None
