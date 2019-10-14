#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.exceptions import *
from modularcalculator.features.feature import Feature
from modularcalculator.features.structure.functions import *

import re
from decimal import *


class ExpNumbersFeature(Feature):

    def id():
        return 'numerical.expnumbers'

    def category():
        return 'Numerical'

    def title():
        return 'Exponent Numbers'

    def desc():
        return 'Eg: 10e6'

    def dependencies():
        return ['numerical.decimalnumbers','structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('numberexp', ExpNumbersFeature.parse_numberexp)

        calculator.funcs['scientific'] = FunctionDefinition(
            'Numerical', 
            'scientific', 
            'Format number in scientific notation',
            ['number', '[places]'],
            ExpNumbersFeature.func_scientific, 
            1, 
            2, 
            'number')
        calculator.funcs['scientific'].units_normalise = False

        calculator.add_number_caster('exp', ExpNumbersFeature.number_exp)

    numexp_regex = re.compile(r'(\-?\d+(\.\d+)?e\-?\d+)', re.IGNORECASE)

    def parse_numberexp(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            numexp_match = ExpNumbersFeature.numexp_regex.match(next)
            if (numexp_match):
                numexp = numexp_match.group(1)
                return [LiteralItem(numexp, numexp)], len(numexp), None
        return None, None, None

    def func_scientific(self, vals, units, refs, flags):
        places = None
        if len(vals) == 2:
            places = vals[1]

        formattednumber = ExpNumbersFeature.dec_to_exp(self, vals[0], places)

        res = OperationResult(formattednumber)
        res.set_unit(units[0])
        return res

    def dec_to_exp(self, num, places=None):
        if places is None:
            places = ''
        else:
            places = '.' + str(places)
        scientificformat = '{0:' + places + 'E}'

        formattednumber = scientificformat.format(num)
        formattednumber = formattednumber.replace('+', '')
        parts = formattednumber.split('E')
        if '.' in parts[0]:
            parts[0] = parts[0].rstrip('0')
        formattednumber = "{}E{}".format(parts[0].rstrip('0'), parts[1])

        return formattednumber

    def number_exp(self, val):
        if isinstance(val, str) and ExpNumbersFeature.numexp_regex.fullmatch(val):
            numexp_match = ExpNumbersFeature.numexp_regex.match(val)
            numexp = numexp_match.group(1)
            num = Decimal(numexp[0:numexp.lower().find('e')])
            exp = Decimal(numexp[numexp.lower().find('e') + 1:])
            num *= (10 ** exp)
            return num, False#NumberType(ExpNumbersFeature.restore_exp)
        
        return None, None

    def restore_exp(self, val, opts=None):
        return ExpNumbersFeature.dec_to_exp(self, val)
