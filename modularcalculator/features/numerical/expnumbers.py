#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *
from modularcalculator.features.feature import Feature
from modularcalculator.features.structure.functions import *
from modularcalculator.numericalengine import NumberType

import re


class ExpNumbersFeature(Feature):

    def id():
        return 'numerical.expnumbers'

    def category():
        return 'Numerical'

    def title():
        return 'Scientific E Notation'

    def desc():
        return 'Eg: 1e6, 2.34E12'

    def dependencies():
        return ['numerical.decimalnumbers','structure.functions']

    def default_options():
        return {
            'Symbol': 'E',
        }

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('numberexp', ExpNumbersFeature.parse_numberexp)

        calculator.funcs['scientific'] = FunctionDefinition(
            'Numerical',
            'scientific',
            'Format number in scientific E notation',
            ['number', '[places]'],
            ExpNumbersFeature.func_scientific,
            1,
            2,
            'number')
        calculator.funcs['scientific'].units_normalise = False

        calculator.add_number_caster('exp', 'Scientific E Notation', ExpNumbersFeature.number_exp, ExpNumbersFeature.restore_exp)

        calculator.feature_options['numerical.expnumbers'] = cls.default_options()

    def parse_numberexp(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            numexp_regex = ExpNumbersFeature.compile_regex(self)
            numexp_match = numexp_regex.match(next)
            if (numexp_match):
                numexp = numexp_match.group(1)
                decnum = ExpNumbersFeature.number_exp(self, numexp)
                return [LiteralItem(numexp, decnum)], len(numexp), None
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
        symbol = self.feature_options['numerical.expnumbers']['Symbol']

        if num == Number(0):
            return "0{}0".format(symbol)
        if places is None:
            places = '.' + str(self.number_prec)
        else:
            places = '.' + str(places)
        scientificformat = '{0:' + places + 'E}'

        formattednumber = scientificformat.format(num)
        formattednumber = formattednumber.replace('+', '')
        parts = formattednumber.split('E')
        if '.' in parts[0]:
            parts[0] = parts[0].rstrip('0')
        if parts[0][-1] == '.':
            parts[0] = parts[0][0 : -1]
        if parts[0] != '0':
            parts[0] = parts[0].rstrip('0')
        formattednumber = "{}{}{}".format(parts[0], symbol, parts[1])

        return formattednumber

    def number_exp(self, val):
        numexp_regex = ExpNumbersFeature.compile_regex(self)
        if isinstance(val, str) and numexp_regex.fullmatch(val):
            numexp_match = numexp_regex.match(val)
            numexp = numexp_match.group(1)
            symbol = self.feature_options['numerical.expnumbers']['Symbol'].lower()
            num = Number(numexp[0:numexp.lower().find(symbol)])
            exp = Number(numexp[numexp.lower().find(symbol) + len(symbol):])
            num *= (Number(10) ** exp)
            num.number_cast = {'ref': ExpNumbersFeature.restore_exp, 'args': [self]}
            return num

        return None

    def restore_exp(self, val, opts=None):
        return ExpNumbersFeature.dec_to_exp(self, val)

    def compile_regex(self):
        return re.compile(r'(\-?\d+(\.\d+)?' + self.feature_options['numerical.expnumbers']['Symbol'] + '\-?\d+)', re.IGNORECASE)
