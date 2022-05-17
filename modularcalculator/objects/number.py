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

        self.num = num
        self.den = den

        # Check if we can cast to string
        self.__str__()


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

    def is_rational(self):
        return Number.is_rational(self.to_decimal())


    def __add__(self, other):
        (lcm, a_num, b_num) = Number.normalise(self, other)
        return Number(a_num + b_num, lcm)

    def __sub__(self, other):
        (lcm, a_num, b_num) = Number.normalise(self, other)
        return Number(a_num - b_num, lcm)

    def __mul__(self, other):
        return Number(self.num * other.num, self.den * other.den)

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
        if self.is_rational():
            return hash(self.to_decimal())
        return hash((self.num, self.den))


    def set_precision(total, decimal_places):
        getcontext().prec = total
        NUMBER['decimal_places'] = decimal_places

    def set_rounding(rounding):
        getcontext().rounding = getattr(import_module('decimal'), rounding)

    def normalise(*vals):
        lcm = math.lcm(*[int(v.den) for v in vals])
        return (lcm, *[v.num * (lcm / v.den) for v in vals])

    def is_rational(n):
        return n == round(n, NUMBER['decimal_places'])

    def is_integer(n):
        return math.floor(n) == n
