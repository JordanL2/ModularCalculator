#!/usr/bin/python3

from decimal import Decimal
import math


class Number:

    def __init__(self, num, den=None):
        if num is None:
            raise Exception("Cannot create Number with arguments: {}, {}".format(repr(num), repr(den)))
        if isinstance(num, Number):
            if den is not None:
                val = num / den
                num = val.num
                den = val.den
            else:
                den = num.den
                num = num.num
        if den is None:
            den = Decimal('1')
        if not isinstance(num, Decimal):
            num = Decimal(num)
        if not isinstance(den, Decimal):
            den = Decimal(den)
        self.num = num
        self.den = den

    def copy(self):
        return Number(self)

    def to_decimal(self):
        res = self.num / self.den
        return Decimal(res)

    def __str__(self):
        val = str(self.to_decimal)
#        val = format(val, 'f')
#        if val.find('.') > -1:
#            val = val.rstrip('0')
        return val

    def __repr__(self):
        if self.den != Decimal('1'):
            return "Number({}, {})".format(self.num, self.den)
        return "Number({})".format(self.num)

    def numden(self):
        return {
            num: self.num,
            den: self.den
        }

    def fraction(self):
        whole = self.num % self.den
        num =  self.num // self.den
        return {
            whole: whole,
            num: num,
            den: self.den
        }


    def __add__(self, other):
        return Number(self.num + Number(other).num)

    def __sub__(self, other):
        return Number(self.num - Number(other).num)

    def __mul__(self, other):
        return Number(self.num * Number(other).num)

    def __truediv__(self, other):
        return Number(self.num / Number(other).num)

    def __floordiv__(self, other):
        return Number(self.num // Number(other).num)

    def __mod__(self, other):
        return Number(self.num % Number(other).num)

    def __divmod__(self, other):
        res = divmod(self.num, Number(other).num)
        return (Number(res[0]), Number(res[1]))

    def __pow__(self, other, modulo=None):
        return Number(pow(self.num, Number(other).num, modulo))


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


    def __complex__(self):
        return complex(self.to_decimal())

    def __int__(self):
        return int(self.to_decimal())

    def __float__(self):
        return float(self.to_decimal())


    def __index__(self):
        return self.__int__()


    def __round__(self, ndigits=0):
        res = self.copy()
        res.num = round(res.num)
        return res

    def __trunc__(self):
        res = self.copy()
        res.num = math.trunc(res.num)
        return res

    def __floor__(self):
        res = self.copy()
        res.num = math.floor(res.num)
        return res

    def __ceil__(self):
        res = self.copy()
        res.num = math.ceil(res.num)
        return res


    def __lt__(self, other):
        return self.to_decimal() < Number(other).to_decimal()

    def __le__(self, other):
        return self.to_decimal() <= Number(other).to_decimal()

    def __eq__(self, other):
        return self.to_decimal() == Number(other).to_decimal()

    def __ne__(self, other):
        return self.to_decimal() != Number(other).to_decimal()

    def __gt__(self, other):
        return self.to_decimal() > Number(other).to_decimal()

    def __ge__(self, other):
        return self.to_decimal() >= Number(other).to_decimal()


    def __hash__(self):
        return hash(self.numden())


    def update_precision(prec):
        getcontext().prec = prec
