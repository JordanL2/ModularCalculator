#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.numerical.bases import BasesFeature
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature

import re


class ArbitraryBaseFeature(Feature):

    def id():
        return 'numerical.arbitrarybasenumbers'

    def category():
        return 'Numerical'

    def title():
        return 'Arbitrary-Base Numbers'

    def desc():
        return 'Enables numbers in arbitrary bases (up to 36), eg: 12z89 is 89 in base 12'

    def dependencies():
        return ['numerical.bases']

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('number_arbbase', ArbitraryBaseFeature.parse_arbbase)
        calculator.funcs['base'] = FunctionDefinition(
            'Bases',
            'base',
            'Convert a base-10 number into any base',
            ['number', 'base'],
            ArbitraryBaseFeature.func_base,
            2,
            2,
            'number')
        calculator.funcs['base'].auto_convert_numerical_result = False
        calculator.add_number_type(ArbitraryBaseNumericalRepresentation)

    arbbase_regex = re.compile(r'(\-?\d+z[0-9A-Z]+(\.[0-9A-Z]+)?)', re.IGNORECASE)

    def parse_arbbase(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            arbbase_match = ArbitraryBaseFeature.arbbase_regex.match(next)
            if arbbase_match:
                arbbasenum = arbbase_match.group(1)
                decnum = ArbitraryBaseNumericalRepresentation.convert_from(self, arbbasenum)
                if decnum is not None:
                    return [LiteralItem(arbbasenum, decnum)], len(arbbasenum), None
        return None, None, None

    def func_base(self, vals, units, refs, flags):
        return OperationResult(ArbitraryBaseFeature.restore_arbbase(self, vals[0], {'base': int(vals[1])}))

    def restore_arbbase(self, val, opts):
        base = opts['base']
        return BasesFeature.number_add_prefix(self, BasesFeature.dec_to_base(self, val, base), "{0}z".format(base))


class ArbitraryBaseNumericalRepresentation:

    @staticmethod
    def name():
        return 'arbitrarybase'

    @staticmethod
    def desc():
        return 'Arbitrary Base'

    @staticmethod
    def convert_from(calculator, val):
        if isinstance(val, str) and ArbitraryBaseFeature.arbbase_regex.fullmatch(val):
            try:
                split_point = val.lower().index('z')
                base = val[0:split_point]
                if base[0] == '-':
                    base = base[1:]
                base = int(base)
                dec_num = BasesFeature.base_to_dec(calculator, BasesFeature.number_remove_prefix(calculator, val, "{0}z".format(base)), base)
                dec_num.number_cast = {'ref': ArbitraryBaseFeature.restore_arbbase, 'args': [{'base': base}], 'base': base}
                return dec_num
            except CalculatorException:
                pass

        return None
