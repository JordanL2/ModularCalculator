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


    numexp_regex = re.compile(r'(\-?\d+(\.\d+)?e\-?\d+)', re.IGNORECASE)

    def parse_numberexp(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items, len(items))
        if prev is None or prev.isop():
            numexp_match = ExpNumbersFeature.numexp_regex.match(next)
            if (numexp_match):
                numexp = numexp_match.group(1)
                num = Decimal(numexp[0:numexp.lower().find('e')])
                exp = Decimal(numexp[numexp.lower().find('e') + 1:])
                num *= (10 ** exp)
                return [LiteralItem(numexp, self.number(num))], len(numexp), None
        return None, None, None

    def func_scientific(self, vals, units, refs, flags):
        num = self.number(vals[0])
        places = ''
        if len(vals) == 2:
            places = '.' + str(self.number(vals[1]))
        scientificformat = '{0:' + places + 'E}'
        formattednumber = scientificformat.format(num)
        formattednumber = formattednumber.replace('+', '')
        res = OperationResult(formattednumber)
        res.set_unit(units[0])
        return res
