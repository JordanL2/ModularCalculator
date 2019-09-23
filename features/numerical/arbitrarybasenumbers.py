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
        return 'Enables numbers in arbitrary bases (up to 36), eg: 012z89 is 89 in base 12'

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
        calculator.add_number_caster('arbitrarybase', ArbitraryBaseFeature.number_arbbase)

    arbbase_regex = re.compile(r'(\-?0\d{1,2}z[0-9A-Z]+(\.[0-9A-Z]+)?)', re.IGNORECASE)

    def parse_arbbase(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items, len(items))
        if prev is None or prev.isop():
            arbbase_match = ArbitraryBaseFeature.arbbase_regex.match(next)
            if arbbase_match:
                arbbasenum = arbbase_match.group(1)
                try:
                    decnum = self.number(arbbasenum)
                    return [LiteralItem(arbbasenum, decnum)], len(arbbasenum), None
                except CalculatorException as err:
                    raise ParsingException(err.message, [], next)
        return None, None, None

    def func_base(self, vals, units, refs, flags):
        return OperationResult(BasesFeature.number_add_prefix(self, BasesFeature.dec_to_base(self, vals[0], vals[1]), "0{0}z".format(vals[1])))

    def number_arbbase(self, val):
        if isinstance(val, str) and ArbitraryBaseFeature.arbbase_regex.fullmatch(val):
            base = val[1:3]
            if base[1].lower() == 'z':
                base = base[0]
            base = int(base)
            return BasesFeature.base_to_dec(self, BasesFeature.number_remove_prefix(self, val, "0{0}z".format(base)), base)
        return None
