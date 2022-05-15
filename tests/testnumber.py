#!/usr/bin/python3

from modularcalculator.objects.number import Number

from decimal import Decimal
import unittest


class TestNumber(unittest.TestCase):

    def __init__(self, n):
        super().__init__(n)
        Number.update_precision(100)

    def test_create(self):
        a = Number(123)
        self.assertEqual(a.num, Decimal('123'))
        self.assertEqual(a.den, 1)
        self.assertIsInstance(a.num, Decimal)
        self.assertIsInstance(a.den, Decimal)

        b = Number('123')
        self.assertEqual(b.num, Decimal('123'))
        self.assertEqual(b.den, 1)
        self.assertIsInstance(b.num, Decimal)
        self.assertIsInstance(b.den, Decimal)

        c = Number(int(123))
        self.assertEqual(c.num, Decimal('123'))
        self.assertEqual(c.den, 1)
        self.assertIsInstance(c.num, Decimal)
        self.assertIsInstance(c.den, Decimal)

        d = Number(float(1.23))
        self.assertEqual(round(d.num, 10), Decimal('1.23'))
        self.assertEqual(d.den, 1)
        self.assertIsInstance(d.num, Decimal)
        self.assertIsInstance(d.den, Decimal)

        e = Number(Decimal('123'))
        self.assertEqual(e.num, Decimal('123'))
        self.assertEqual(e.den, 1)
        self.assertIsInstance(e.num, Decimal)
        self.assertIsInstance(e.den, Decimal)

        f = Number(e)
        self.assertEqual(f.num, Decimal('123'))
        self.assertIsNot(e, f)
        self.assertEqual(f.den, 1)
        self.assertIsInstance(f.num, Decimal)
        self.assertIsInstance(f.den, Decimal)


    def test_add_1(self):
        res = Number(12) + Number(34)
        self.assertEqual(res, Number(46))
        self.assertIsInstance(res, Number)

    def test_add_2(self):
        res = Number(11, 6) + Number(3, 10)
        self.assertEqual(res, Number(32, 15))
        self.assertIsInstance(res, Number)

    def test_sub_1(self):
        res = Number(12) - Number(34)
        self.assertEqual(res, Number(-22))
        self.assertIsInstance(res, Number)

    def test_sub_2(self):
        res = Number(11, 6) - Number(3, 10)
        self.assertEqual(res, Number(23, 15))
        self.assertIsInstance(res, Number)

    def test_mul_1(self):
        res = Number(12) * Number(3)
        self.assertEqual(res, Number(36))
        self.assertIsInstance(res, Number)

    def test_mul_2(self):
        res = Number(1, 2) * Number(1, 4)
        self.assertEqual(res, Number(1, 8))
        self.assertIsInstance(res, Number)

    def test_mul_3(self):
        res = Number(1, 2) * Number(32)
        self.assertEqual(res, Number(16))
        self.assertIsInstance(res, Number)

    def test_truediv_1(self):
        res = Number(12) / Number(5)
        self.assertEqual(res, Number('2.4'))
        self.assertEqual(res, Number(12, 5))
        self.assertIsInstance(res, Number)

    def test_truediv_2(self):
        res = Number(16) / Number(6)
        self.assertEqual(res, Number(8, 3))
        self.assertIsInstance(res, Number)

    def test_div_mul(self):
        res = Number(10) / Number(3)
        res *= 3
        self.assertEqual(res, Number(10))
        self.assertIsInstance(res, Number)

    def test_floordiv(self):
        res = Number(12) // Number(5)
        self.assertEqual(res, Number(2))
        self.assertIsInstance(res, Number)

    def test_mod_1(self):
        res = Number(13) % Number(5)
        self.assertEqual(res, Number(3))
        self.assertIsInstance(res, Number)

    def test_mod_2(self):
        res = Number(5, 2) % Number(2)
        self.assertEqual(res, Number(1, 2))
        self.assertIsInstance(res, Number)

    def test_divmod_1(self):
        res = divmod(Number(13), Number(5))
        self.assertEqual(res, (Number(2), Number(3)))
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0], Number)
        self.assertIsInstance(res[1], Number)

    def test_divmod_2(self):
        res = divmod(Number(5, 2), Number(2))
        self.assertEqual(res, (Number(1), Number(1, 2)))

    def test_pow_1(self):
        res = Number(6) ** Number(2)
        self.assertEqual(res, Number(36))
        self.assertIsInstance(res, Number)

    def test_pow_2(self):
        res = pow(Number(6), Number(2))
        self.assertEqual(res, Number(36))
        self.assertIsInstance(res, Number)

    def test_pow_3(self):
        res = pow(Number(6), Number(2), 10)
        self.assertEqual(res, Number(6))
        self.assertIsInstance(res, Number)

    def test_pow_4(self):
        res = Number(4) ** Number(1, 2)
        self.assertEqual(res, Number(2))
        self.assertIsInstance(res, Number)

    def test_pow_5(self):
        res = Number(1 / 2) ** Number(2)
        self.assertEqual(res, Number(1 / 4))
        self.assertIsInstance(res, Number)


    def test_iadd(self):
        res = Number(12)
        res += Number(34)
        self.assertEqual(res, Number(46))
        self.assertIsInstance(res, Number)

    def test_isub(self):
        res = Number(12)
        res -= Number(34)
        self.assertEqual(res, Number(-22))
        self.assertIsInstance(res, Number)

    def test_imul(self):
        res = Number(12)
        res *= Number(3)
        self.assertEqual(res, Number(36))
        self.assertIsInstance(res, Number)

    def test_itruediv(self):
        res = Number(12)
        res /= Number(5)
        self.assertEqual(res, Number('2.4'))
        self.assertIsInstance(res, Number)

    def test_ifloordiv(self):
        res = Number(12)
        res //= Number(5)
        self.assertEqual(res, Number(2))
        self.assertIsInstance(res, Number)

    def test_imod(self):
        res = Number(13)
        res %= Number(5)
        self.assertEqual(res, Number(3))
        self.assertIsInstance(res, Number)

    def test_ipow(self):
        res = Number(6)
        res **= Number(2)
        self.assertEqual(res, Number(36))
        self.assertIsInstance(res, Number)


    def test_neg(self):
        a = Number(123)
        b = -a
        self.assertEqual(b, Number(-123))
        self.assertIsInstance(b, Number)

    def test_pos(self):
        a = Number(123)
        b = +a
        self.assertEqual(b, Number(123))
        self.assertIsInstance(b, Number)

    def test_abs(self):
        a = Number(-123)
        b = abs(a)
        self.assertEqual(b, Number(123))
        self.assertIsInstance(b, Number)


if __name__ == '__main__':
    unittest.main()
