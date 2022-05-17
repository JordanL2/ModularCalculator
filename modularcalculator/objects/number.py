#!/usr/bin/python3

from decimal import Decimal, getcontext, InvalidOperation
from importlib import import_module
import math


NUMBER = {
    'decimal_places': 10
}


class Number:

    def __init__(self, num, den=None):
        if num is None:
            raise Exception("Cannot create Number with arguments: {}, {}".format(type(num), type(den)))
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

        # Try to simplify num/den if possible
        if num % 1 == 0 and den % 1 == 0:
            # Greatest common divisor
            gcd = math.gcd(int(num), int(den))
            if gcd > 1:
                num /= gcd
                den /= gcd
        elif (num / den) % 1 == 0:
            # Can be simplified to an integer
            num = num / den
            den = Decimal(1)

        self.num = num
        self.den = den


    def copy(self):
        return Number(self.num, self.den)

    def __str__(self):
        val = str(round(self.to_decimal(), NUMBER['decimal_places']))
        if val.find('.') > -1:
            val = val.rstrip('0')
            if val[-1] == '.':
                val = val[0:-1]
        return val

    def __repr__(self):
        if self.den != Decimal('1'):
            return "Number({}, {})".format(self.num, self.den)
        return "Number({})".format(self.num)

    def fraction(self):
        (whole, num) = divmod(self.num, self.den)
        return (Number(whole), Number(num), Number(self.den))

    def will_truncate(self):
        return str(self.to_decimal()) != self.__str__()


    def __add__(self, other):
        (lcm, a_num, b_num) = Number.normalise(self, other)
        return Number(a_num + b_num, lcm)

    def __sub__(self, other):
        (lcm, a_num, b_num) = Number.normalise(self, other)
        return Number(a_num - b_num, lcm)

    def __mul__(self, other):
        try:
            return Number(self.num * other.num, self.den * other.den)
        except InvalidOperation:
            # Run out of precision, need to collapse num/den unfortunately
            return Number(self.num / self.den * other.num / other.den)

    def __truediv__(self, other):
        other = Number(other.den, other.num)
        return self.__mul__(other)

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
        return Number(pow(self.to_decimal(), other.to_decimal(), modulo))


    def __neg__(self):
        res = self.copy()
        res.num = -res.num
        return res

    def __pos__(self):
        return self

    def __abs__(self):
        res = self.copy()
        res.num = abs(res.num)
        return res


    def to_decimal(self):
        res = self.num / self.den
        return Decimal(res)

    def __complex__(self):
        return complex(self.to_decimal())

    def __int__(self):
        return int(self.to_decimal())

    def __float__(self):
        return float(self.to_decimal())


    def __round__(self, ndigits=0):
        return Number(round(self.to_decimal(), ndigits))

    def __trunc__(self):
        return Number(math.trunc(self.to_decimal()))

    def __floor__(self):
        return Number(math.floor(self.to_decimal()))

    def __ceil__(self):
        return Number(math.ceil(self.to_decimal()))


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
        if self.will_truncate():
            return hash((self.num, self.den))
        return hash(self.to_decimal())


    def set_precision(total, decimal_places):
        getcontext().prec = total
        NUMBER['decimal_places'] = decimal_places

    def set_rounding(rounding):
        getcontext().rounding = getattr(import_module('decimal'), rounding)

    def normalise(*vals):
        lcm = math.lcm(*[int(v.den) for v in vals])
        return (lcm, *[v.num * (lcm / v.den) for v in vals])
