#!/usr/bin/python3

from modularcalculator.engine import Engine
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.number import *

#import math


class NumericalEngine(Engine):

    def __init__(self):
        super().__init__()

        self.number_size = 70
        self.number_prec = 30
        self.update_engine_prec()

        self.number_casters = []
        #self.finalizers.append({'ref': NumericalEngine.finalize_number})
        self.validators['number'] = NumericalEngine.validate_number

    def number_prec_set(self, prec):
        self.number_prec = prec
        self.update_engine_prec()

    def number_prec_get(self):
        return self.number_prec

    def update_engine_prec(self):
        Number.set_precision(self.number_size + self.number_prec, self.number_prec)

#    def number_to_string(self, num):
#        if isinstance(num, Number):
#            return str(num)
#        raise Exception("Not Number!")
            #num = format(num, 'f')
            #if num.find('.') > -1:
            #    num = num.rstrip('0')
        #return num

#    def clean_number(self, num):
#        return Decimal(self.number_to_string(num))

#    def round_number(self, num):
#        if not isinstance(num, Decimal):
#            return val
#        try:
#            num = Decimal(round(num, self.number_prec))
#        except InvalidOperation as err:
#            raise CalculatorException('Number entered is too large')
#        return self.clean_number(num)

#    def floor_number(self, num):
#        return Number(math.floor(num))

    def number(self, val):
        for caster in self.number_casters:
            num, num_type = caster['ref'](self, val)
            if num is not None:
                if isinstance(num, Number):
                    return num, num_type
                #num = self.clean_number(num)
                return Number(num), num_type
        raise CalculatorException("Can't cast to number: {0}".format(str(val)))

    def restore_number_type(self, num, num_type):
        if not num_type:
            return num
        return num_type.restore(self, num)

#    def finalize_number(self, val):
#        if isinstance(val.value, Decimal):
#            val.value = self.clean_number(val.value)
#            val.value = self.round_number(val.value)
#        return val

    def validate_number(self, value, unit=None, ref=None):
        try:
            self.number(value)
            return True
        except Exception:
            return False


class NumberType():

    def __init__(self, func, opts=None):
        self.func = func
        self.opts = opts

    def restore(self, calculator, num):
        return self.func(calculator, num, self.opts)
