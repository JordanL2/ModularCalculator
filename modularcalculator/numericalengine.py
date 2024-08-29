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

        self.number_types = {}
        self.numerical_validators = []
        self.add_validator('number', 'number', NumericalEngine.validate_number, True)
        self.add_validator('number_int', 'integer', NumericalEngine.validate_number_int, True)
        self.add_validator('number_int_positive', 'positive integer', NumericalEngine.validate_number_int_positive, True)

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

    def add_validator(self, name, desc, ref, is_number=False):
        if name in self.validators:
            raise Exception("Duplicate validator {}".format(name))
        self.validators[name] = {
            'desc': desc,
            'ref': ref,
        }
        if is_number:
            self.numerical_validators.append(name)

    def number(self, val):
        if isinstance(val, Number):
            return val
        for number_type in self.number_types.values():
            num = number_type.parse(self, val)
            if num is not None:
                return num
        raise CalculatorException("Can't cast to number: {0}".format(str(val)))

    def validate_number(self, value, unit=None, ref=None):
        try:
            self.number(value)
            return True
        except Exception:
            return False

    def validate_number_int(self, value, unit=None, ref=None):
        try:
            num = self.number(value)
            return (num % Number(1)).to_decimal() == 0
        except Exception:
            return False

    def validate_number_int_positive(self, value, unit=None, ref=None):
        try:
            num = self.number(value)
            return (num % Number(1)).to_decimal() == 0 and num.to_decimal() >= 0
        except Exception:
            return False
