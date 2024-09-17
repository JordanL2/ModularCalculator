#!/usr/bin/python3

from modularcalculator.services.typechecking import *

from decimal import Decimal, getcontext, InvalidOperation
from importlib import import_module
import math


NUMBER = {
    'decimal_places': 10
}


class Number:

    def __init__(self, num, den=None, skip_checks=False, number_cast=None):
        assert_class(Number, self)
        self.number_cast = number_cast
        if skip_checks:
            self.num = num
            self.den = den
        else:
            if den is None:
                den = Decimal(1)
            if not isinstance(num, Decimal):
                if type(num) not in (str, int):
                    raise Exception("Cannot create Number with arguments: {}, {}".format(type(num), type(den)))
                num = Decimal(num)
            if not isinstance(den, Decimal):
                if type(den) not in (str, int):
                    raise Exception("Cannot create Number with arguments: {}, {}".format(type(num), type(den)))
                den = Decimal(den)
            if den == 0:
                raise Exception("Cannot create Number with denominator of 0")

            # Make numerator an integer if it isn't already
            if not Number.is_integer(num):
                (a, b) = num.as_integer_ratio()
                num = Decimal(a)
                den *= b
            # Make denominator an integer if it isn't already
            if not Number.is_integer(den):
                (a, b) = den.as_integer_ratio()
                den = Decimal(a)
                num *= b
            # Make sure denominator is positive
            if den < 0:
                den = -den
                num = -num
            # Reduce num/den by dividing by greatest common divisor
            gcd = math.gcd(int(num), int(den))
            if gcd > 1:
                num /= gcd
                den /= gcd

            self.num = num.to_integral_exact()
            self.den = den.to_integral_exact()


    def __str__(self):
        assert_class(Number, self)
        raise Exception("Use to_string(calculator)")

    def to_string(self, calculator=None):
        assert_class(Number, self)
        assert_optional_classname("ModularCalculator", calculator)
        if hasattr(self, 'number_cast') and self.number_cast is not None and 'to_string' in self.number_cast:
            return self.number_cast['to_string'](
                calculator,
                self,
                *(self.number_cast['args'] if 'args' in self.number_cast else []))
        dec_num = self.to_decimal()
        if dec_num == 0:
            # This is to avoid getting '-0'
            dec_num = 0
        val = "{0:f}".format(round(dec_num, NUMBER['decimal_places']))
        if val.find('.') > -1:
            val = val.rstrip('0')
            if val[-1] == '.':
                val = val[0:-1]
        return val

    def __format__(self, format_spec: str):
        assert_class(Number, self)
        return self.to_decimal().__format__(format_spec)

    def __repr__(self):
        assert_class(Number, self)
        if self.den != Decimal('1'):
            return "Number('{0:f}', '{1:f}')".format(self.num, self.den)
        return "Number('{0:f}')".format(self.num)

    def as_fraction(self):
        assert_class(Number, self)
        (whole, num) = divmod(self.num, self.den)
        return (whole, num, self.den)

    def is_integer(self):
        assert_class(Number, self)
        return self.den == Decimal(1)

    def copy(self):
        assert_class(Number, self)
        return Number(self.num, self.den, number_cast=self.number_cast, skip_checks=True)


    def __add__(self, other):
        assert_class(Number, self, other)
        (lcm, a_num, b_num) = Number.normalise(self, other)
        return Number(a_num + b_num, lcm, number_cast=self.number_cast)

    def __sub__(self, other):
        assert_class(Number, self, other)
        (lcm, a_num, b_num) = Number.normalise(self, other)
        return Number(a_num - b_num, lcm, number_cast=self.number_cast)

    def __mul__(self, other):
        assert_class(Number, self, other)
        return Number(self.num * other.num, self.den * other.den, number_cast=self.number_cast)

    def __truediv__(self, other):
        assert_class(Number, self, other)
        return Number(self.num * other.den, self.den * other.num, number_cast=self.number_cast)

    def __floordiv__(self, other):
        assert_class(Number, self, other)
        res = self.__truediv__(other)
        return res.__floor__()

    def __mod__(self, other):
        assert_class(Number, self, other)
        (lcm, a_num, b_num) = Number.normalise(self, other)
        return Number(a_num % b_num, lcm, number_cast=self.number_cast)

    def __divmod__(self, other):
        assert_class(Number, self, other)
        div = self // other
        mod = self % other
        return (div, mod)

    def __pow__(self, other, modulo=None):
        assert_class(Number, self, other)
        if other.to_decimal() < 0:
            res = Number(pow(self.den, -other.to_decimal()), pow(self.num, -other.to_decimal()), number_cast=self.number_cast)
        else:
            res = Number(pow(self.num, other.to_decimal()), pow(self.den, other.to_decimal()), number_cast=self.number_cast)
        if modulo is None:
            return res
        return res % modulo


    def __neg__(self):
        assert_class(Number, self)
        return Number(-self.num, self.den, skip_checks=True, number_cast=self.number_cast)

    def __pos__(self):
        assert_class(Number, self)
        return self

    def __abs__(self):
        assert_class(Number, self)
        return Number(abs(self.num), self.den, skip_checks=True, number_cast=self.number_cast)

    def log(self, base=None):
        assert_class(Number, self)
        assert_optional_class((float, int), base)
        log = self.num.ln() - self.den.ln()
        if base is None:
            return Number(log, number_cast=self.number_cast)
        if base <= 0:
            raise ExecutionException("Cannot use base <= 0 for log function")
        return Number(log / Decimal(base).ln(), number_cast=self.number_cast)


    def to_decimal(self):
        assert_class(Number, self)
        return self.num / self.den

    def __complex__(self):
        assert_class(Number, self)
        return complex(self.to_decimal())

    def __int__(self):
        assert_class(Number, self)
        return int(self.to_decimal())

    def __float__(self):
        assert_class(Number, self)
        return float(self.to_decimal())


    def __round__(self, ndigits=0):
        assert_class(Number, self)
        assert_optional_class(int, ndigits)
        return Number(round(self.to_decimal(), ndigits), number_cast=self.number_cast)

    def __trunc__(self):
        assert_class(Number, self)
        return Number(Decimal(math.trunc(self.to_decimal())), Decimal(1), skip_checks=True, number_cast=self.number_cast)

    def __floor__(self):
        assert_class(Number, self)
        return Number(Decimal(math.floor(self.to_decimal())), Decimal(1), skip_checks=True, number_cast=self.number_cast)

    def __ceil__(self):
        assert_class(Number, self)
        return Number(Decimal(math.ceil(self.to_decimal())), Decimal(1), skip_checks=True, number_cast=self.number_cast)


    def __lt__(self, other):
        assert_class(Number, self, other)
        return self.to_decimal() < other.to_decimal()

    def __le__(self, other):
        assert_class(Number, self, other)
        return self.to_decimal() <= other.to_decimal()

    def __eq__(self, other):
        assert_class(Number, self, other)
        return self.to_decimal() == other.to_decimal()

    def __ne__(self, other):
        assert_class(Number, self, other)
        return self.to_decimal() != other.to_decimal()

    def __gt__(self, other):
        assert_class(Number, self, other)
        return self.to_decimal() > other.to_decimal()

    def __ge__(self, other):
        assert_class(Number, self, other)
        return self.to_decimal() >= other.to_decimal()


    def __hash__(self):
        assert_class(Number, self)
        return hash((self.num, self.den))


    def set_precision(total, decimal_places):
        getcontext().prec = total
        NUMBER['decimal_places'] = decimal_places

    def set_rounding(rounding):
        getcontext().rounding = getattr(import_module('decimal'), rounding)

    def normalise(a, b):
        lcm = math.lcm(int(a.den), int(b.den))
        return (lcm, a.num * lcm / a.den, b.num * lcm / b.den)

    def is_integer(n):
        return math.floor(n) == n
