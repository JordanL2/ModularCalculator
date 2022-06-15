#!/usr/bin/python3

from modularcalculator.engine import Engine
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.number import *


class NumericalEngine(Engine):

    def __init__(self):
        super().__init__()

        self.number_size = 100
        self.number_prec = 30
        self.update_engine_prec()
        self.number_set_rounding('ROUND_HALF_UP')

        self.number_casters = []
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
        Number.set_precision(self.number_size, self.number_prec)

    def number_set_rounding(self, rounding):
        Number.set_rounding(rounding)

    def number(self, val):
        if isinstance(val, Number):
            return val
        for caster in self.number_casters:
            num = caster['ref'](self, val)
            if num is not None:
                return num
        raise CalculatorException("Can't cast to number: {0}".format(str(val)))

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
