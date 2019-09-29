#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature


class BasesFeature(Feature):

    def id():
        return 'numerical.bases'

    def category():
        return 'Numerical'

    def title():
        return 'Bases'

    def desc():
        return 'Base feature for non-decimal bases. Adds dec function to turn any number into a decimal'

    def dependencies():
        return ['numerical.decimalnumbers','structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['dec'] = FunctionDefinition(
            'Bases', 
            'dec', 
            'Convert a number from any base to base-10',
            ['number'],
            BasesFeature.func_dec, 
            1, 
            1, 
            'number')
        calculator.funcs['dec'].auto_convert_numbers = False

    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def func_dec(self, vals, units, refs, flags):
        return OperationResult(vals[0])

    def number_remove_prefix(self, val, prefix):
        return val.lower().replace(prefix, '')

    def number_add_prefix(self, val, prefix):
        if val[0] == '-':
            return val[0] + prefix + val[1:]
        else:
            return prefix + val

    def base_to_dec(self, val, base):
        if val == 0:
            return 0
        if base == 10:
            return Decimal(val)
        if base < 2 or base > 36:
            raise CalculatorException("Base must be between 2 and 36")

        negative = False
        if val[0] == '-':
            negative = True
            val = val[1:]

        power = len(val) - 1
        dot_index = val.find('.')
        if dot_index > -1:
            power = dot_index - 1

        dec = Decimal(0)
        val = val.upper()
        for c in val:
            if c == '.':
                continue
            c_val = BasesFeature.digits.find(c)
            if c_val == -1 or c_val > base - 1:
                raise CalculatorException("Illegal digit: {0}".format(c))
            dec += Decimal(c_val * (base ** power))
            power -= 1

        if negative:
            dec = -dec
        return self.clean_number(dec)

    def dec_to_base(self, val, base):
        if val == 0:
            return 0
        if base == 10:
            return self.number_to_string(val)
        if base < 2 or base > 36:
            raise CalculatorException("Base must be between 2 and 36")
        
        negative = val < 0
        val = abs(val)

        power = 0
        while (base ** (power + 1)) <= val:
            power += 1

        str = ''
        while power >= 0 or (val > 0 and len(str) < 28):
            if power == -1:
                str += '.'
            c_val = int(val / Decimal(base ** power))
            val -= Decimal(c_val * (base ** power))
            str += BasesFeature.digits[c_val]
            power -= 1

        if negative:
            str = '-' + str
        if str.find('.') > -1:
            str = str.rstrip('0')
        return str
