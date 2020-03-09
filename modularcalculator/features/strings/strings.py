#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.operators import OperationResult, OperatorDefinition
from modularcalculator.features.feature import Feature


class StringsFeature(Feature):

    def id():
        return 'strings.strings'

    def category():
        return 'String'

    def title():
        return 'Strings'

    def desc():
        return 'String type'

    def dependencies():
        return []

    def default_options():
        return {
            'Symbol': '\'',
            'Escape Char': '\\'
        }

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('string', StringsFeature.parse_string)

        calculator.add_op(OperatorDefinition(
            'String', 
            '+$', 
            'Concatenate two strings',
            StringsFeature.op_string_add, 
            1, 
            1, 
            'string'))
        string_mult = OperatorDefinition(
            'String', 
            '*$', 
            'Multiply a string a number of times',
            StringsFeature.op_string_multiply, 
            1, 
            1, 
            ['string', 'number'])
        calculator.add_op(string_mult)
        
        calculator.validators['string'] = StringsFeature.validate_string

        calculator.feature_options['strings.strings'] = cls.default_options()

    def parse_string(self, expr, i, items, flags):
        symbol = self.feature_options['strings.strings']['Symbol']
        escape_char = self.feature_options['strings.strings']['Escape Char']
        next = expr[i:]
        if (next[0] == symbol):
            i = 1
            if i >= len(next):
                raise ParseException("Missing end {0}".format(symbol), [], next)
            string = ''
            escape = False
            while next[i] != symbol or escape:
                if next[i] == escape_char:
                    escape = not escape
                else:
                    escape = False
                if not escape:
                    string += next[i]
                i += 1
                if i >= len(next):
                    raise ParseException("Missing end {0}".format(symbol), [], next)
            return [LiteralItem(next[0:i + 1], string)], i + 1, None
        return None, None, None

    def op_string_add(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]) + StringsFeature.string(self, vals[1]))

    def op_string_multiply(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]) * int(vals[1]))
        
    def string(self, val):
        if isinstance(val, Decimal):
            return self.number_to_string(self.round_number(val))
        return str(val)

    def validate_string(self, value, unit, ref):
        try:
            str(value)
            return True
        except Exception:
            return False
