#!/usr/bin/python3

from decimal import Decimal, getcontext, InvalidOperation
from importlib import import_module
import math


NUMBER = {
    'decimal_places': 10
}


class Number:

    def __init__(self, num, den=None, skip_checks=False):
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

            try:
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
            except InvalidOperation:
                # Run out of precision, need to collapse num/den unfortunately
                num /= den
                den = Decimal(1)

            self.num = num.to_integral_exact()
            self.den = den.to_integral_exact()


    def __str__(self):
        val = "{0:f}".format(round(self.to_decimal(), NUMBER['decimal_places']))
        if val.find('.') > -1:
            val = val.rstrip('0')
            if val[-1] == '.':
                val = val[0:-1]
        return val

    def __format__(self, format_spec):
        return self.to_decimal().__format__(format_spec)

    def __repr__(self):
        if self.den != Decimal('1'):
            return "Number({0:f}, {1:f})".format(self.num, self.den)
        return "Number({0:f})".format(self.num)

    def as_fraction(self):
        (whole, num) = divmod(self.num, self.den)
        return (whole, num, self.den)

    def is_integer(self):
        return Number.is_integer(self.to_decimal())


    def __add__(self, other):
        (lcm, a_num, b_num) = Number.normalise(self, other)
        return Number(a_num + b_num, lcm)

    def __sub__(self, other):
        (lcm, a_num, b_num) = Number.normalise(self, other)
        return Number(a_num - b_num, lcm)

    def __mul__(self, other):
        return Number(self.num * other.num, self.den * other.den)

    def __truediv__(self, other):
        return Number(self.num * other.den, self.den * other.num)

    def __floordiv__(self, other):
        res = self.__truediv__(other)
        return res.__floor__()

    def __mod__(self, other):
        (lcm, a_num, b_num) = Number.normalise(self, other)
        return Number(a_num % b_num, lcm)

    def __divmod__(self, other):
        div = self // other
        mod = self % other
        return (div, mod)

    def __pow__(self, other, modulo=None):
        res = Number(pow(self.num, other.to_decimal()), pow(self.den, other.to_decimal()))
        if modulo is None:
            return res
        return res % modulo


    def __neg__(self):
        return Number(-self.num, self.den, skip_checks=True)

    def __pos__(self):
        return self

    def __abs__(self):
        return Number(abs(self.num), self.den, skip_checks=True)

    def log(self, base=None):
        if base is None:
            return Number(self.to_decimal().ln())
        return Number(self.to_decimal().ln() / Decimal(base).ln())


    def to_decimal(self):
        return self.num / self.den

    def __complex__(self):
        return complex(self.to_decimal())

    def __int__(self):
        return int(self.to_decimal())

    def __float__(self):
        return float(self.to_decimal())


    def __round__(self, ndigits=0):
        return Number(round(self.to_decimal(), ndigits))

    def __trunc__(self):
        return Number(Decimal(math.trunc(self.to_decimal())), Decimal(1), skip_checks=True)

    def __floor__(self):
        return Number(Decimal(math.floor(self.to_decimal())), Decimal(1), skip_checks=True)

    def __ceil__(self):
        return Number(Decimal(math.ceil(self.to_decimal())), Decimal(1), skip_checks=True)


    def __lt__(self, other):
        return self.to_decimal() < other.to_decimal()

    def __le__(self, other):
        return self.to_decimal() <= other.to_decimal()

    def __eq__(self, other):
        return self.to_decimal() == other.to_decimal()

    def __ne__(self, other):
        return self.to_decimal() != other.to_decimal()

    def __gt__(self, other):
        return self.to_decimal() > other.to_decimal()

    def __ge__(self, other):
        return self.to_decimal() >= other.to_decimal()


    def __hash__(self):
        return hash((self.num, self.den))


    def set_precision(total, decimal_places):
        getcontext().prec = total
        NUMBER['decimal_places'] = decimal_places

    def set_rounding(rounding):
        getcontext().rounding = getattr(import_module('decimal'), rounding)

    def normalise(*vals):
        lcm = math.lcm(*[int(v.den) for v in vals])
        return (lcm, *[v.num * (lcm / v.den) for v in vals])

    def is_integer(n):
        return math.floor(n) == n
