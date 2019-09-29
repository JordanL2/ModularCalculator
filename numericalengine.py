#!/usr/bin/python3

from modularcalculator.engine import Engine
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *

from decimal import *
import math


class NumericalEngine(Engine):

    def __init__(self):
        super().__init__()

        self.number_size = 70
        self.number_prec = 30
        self.update_engine_prec()

        self.number_casters = []
        self.finalizers.append({'ref': NumericalEngine.finalize_number})
        self.validators['number'] = NumericalEngine.validate_number

    def number_size_set(self, size):
        self.number_size = size
        self.update_engine_prec()

    def number_size_get(self):
        return self.number_size

    def number_prec_set(self, prec):
        self.number_prec = prec
        self.update_engine_prec()

    def number_prec_get(self):
        return self.number_prec

    def update_engine_prec(self):
        getcontext().prec = (self.number_prec + self.number_size + 1)
    
    def number_to_string(self, num):
        if isinstance(num, Decimal):
            num = format(num, 'f')
            if num.find('.') > -1:
                num = num.rstrip('0')
        return num

    def clean_number(self, num):
        return Decimal(self.number_to_string(num))

    def round_number(self, num):
        if not isinstance(num, Decimal):
            return val
        try:
            num = Decimal(round(num, self.number_prec))
        except InvalidOperation as err:
            raise CalculatorException('Number entered is too large')
        return self.clean_number(num)

    def floor_number(self, num):
        return Decimal(math.floor(num))

    def is_whole_number(self, num):
        return self.round_number(num) == self.floor_number(num)

    def number(self, val):
        for caster in self.number_casters:
            num, num_type = caster['ref'](self, val)
            if num is not None:
                num = self.clean_number(num)
                return num, num_type
        raise CalculatorException("Can't cast to number: {0}".format(str(val)))

    def restore_number_type(self, num, num_type):
        if num_type is None or num_type == False:
            return num
        if not isinstance(num, Decimal):
            num = self.number(num)[0]
        return num_type.restore(self, num)

    def finalize_number(self, val):
        if isinstance(val.value, Decimal):
            val.value = self.number(val.value)[0]
            val.value = self.round_number(val.value)
        return val

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
