#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *
from modularcalculator.features.feature import Feature
from modularcalculator.features.structure.functions import *

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

    def after():
        return ['numerical.numericalrepresentation']

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
        calculator.funcs['scientific'].auto_convert_numerical_result = False

        calculator.add_number_type(ExpNumericalRepresentation)

        calculator.feature_options['numerical.expnumbers'] = cls.default_options()

    def parse_numberexp(self, expr, i, items, flags):
        next = expr[i:]
        prev = previous_functional_item(items)
        if prev is None or prev.isop():
            numexp_regex = ExpNumbersFeature.compile_regex(self)
            numexp_match = numexp_regex.match(next)
            if (numexp_match):
                numexp = numexp_match.group(1)
                decnum = ExpNumericalRepresentation.parse(self, numexp)
                return [LiteralItem(numexp, decnum)], len(numexp), None
        return None, None, None

    def func_scientific(self, vals, units, refs, flags):
        places = None
        if len(vals) == 2:
            places = vals[1]

        if places is None:
            number = ExpNumericalRepresentation.convert_to(self, vals[0])
        else:
            formattednumber = ExpNumbersFeature.dec_to_exp(self, vals[0], places)
            number = self.number(formattednumber)

        res = OperationResult(number)
        res.set_unit(units[0])
        return res

    def dec_to_exp(self, num, places=None):
        symbol = self.feature_options['numerical.expnumbers']['Symbol']

        if num.to_decimal() == 0:
            return "0{}0".format(symbol)
        if places is None:
            places = '.' + str(self.number_size_after_decimal_point_get())
        else:
            places = '.' + str(places.to_string())
        scientificformat = '{0:' + places + 'E}'

        formattednumber = scientificformat.format(num.to_decimal())
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

    def compile_regex(self):
        if not hasattr(self, 'ExpNumbersFeature_numexp_regex') or not hasattr(self, 'ExpNumbersFeature_numexp_regex_symbol') or self.ExpNumbersFeature_numexp_regex_symbol != self.feature_options['numerical.expnumbers']['Symbol']:
            self.ExpNumbersFeature_numexp_regex = re.compile(r'(\-?\d+(\.\d+)?' + self.feature_options['numerical.expnumbers']['Symbol'] + r'\-?\d+)', re.IGNORECASE)
            self.ExpNumbersFeature_numexp_regex_symbol = self.feature_options['numerical.expnumbers']['Symbol']
        return self.ExpNumbersFeature_numexp_regex


class ExpNumericalRepresentation:

    @staticmethod
    def name():
        return 'scientific'

    @staticmethod
    def desc():
        return 'Scientific E Notation'

    @staticmethod
    def parse(calculator, val):
        numexp_regex = ExpNumbersFeature.compile_regex(calculator)
        if isinstance(val, str) and numexp_regex.fullmatch(val):
            numexp_match = numexp_regex.match(val)
            numexp = numexp_match.group(1)
            symbol = calculator.feature_options['numerical.expnumbers']['Symbol'].lower()
            num = Number(numexp[0:numexp.lower().find(symbol)])
            exp = Number(numexp[numexp.lower().find(symbol) + len(symbol):])
            num *= (Number(10) ** exp)
            num = ExpNumericalRepresentation.convert_to(calculator, num)
            return num

        return None

    @staticmethod
    def to_string(calculator, val):
        return ExpNumbersFeature.dec_to_exp(calculator, val)

    @staticmethod
    def convert_to(calculator, val):
        if isinstance(val, Number):
            val = val.copy()
            val.number_cast = {'to_string': ExpNumericalRepresentation.to_string}
            return val
        return None
