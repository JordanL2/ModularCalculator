#!/usr/bin/python3

from modularcalculator.services.typechecking import *

from decimal import Decimal
import unittest


class TestTypeChecking(unittest.TestCase):

    def category(self):
        return None

    def setUp(self):
        enable_type_checking()

    def tearDown(self):
        enable_type_checking()


    def test_assert_class_1class_1val_pos(self):
        assert_class(Decimal, Decimal(1))

    def test_assert_class_1class_1val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_class(Decimal, 5.0)
        self.assertEqual(str(cm.exception), "'float' != 'Decimal'")

    def test_assert_class_2class_1val_pos(self):
        assert_class((Decimal, float), Decimal(1))
        assert_class((Decimal, float), 2.0)

    def test_assert_class_2class_1val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_class((Decimal, float), 1)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")

    def test_assert_class_2class_2val_pos(self):
        assert_class((Decimal, float), Decimal(1), Decimal(2))
        assert_class((Decimal, float), 2.0, 3.0)
        assert_class((Decimal, float), Decimal(1), 2.0)

    def test_assert_class_2class_2val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_class((Decimal, float), 1, 1.0)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")
        with self.assertRaises(AssertionError) as cm:
            assert_class((Decimal, float), 1.0, 1)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")


    def test_assert_optional_class_1class_1val_pos(self):
        assert_optional_class(Decimal, Decimal(1))
        assert_optional_class(Decimal, None)

    def test_assert_optional_class_1class_1val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_optional_class(Decimal, 5.0)
        self.assertEqual(str(cm.exception), "'float' != 'Decimal'")

    def test_assert_optional_class_2class_1val_pos(self):
        assert_optional_class((Decimal, float), Decimal(1))
        assert_optional_class((Decimal, float), 2.0)
        assert_optional_class((Decimal, float), None)

    def test_assert_optional_class_2class_1val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_optional_class((Decimal, float), 1)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")

    def test_assert_optional_class_2class_2val_pos(self):
        assert_optional_class((Decimal, float), Decimal(1), Decimal(2))
        assert_optional_class((Decimal, float), 2.0, 3.0)
        assert_optional_class((Decimal, float), None, Decimal(2))
        assert_optional_class((Decimal, float), 2.0, None)

    def test_assert_optional_class_2class_2val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_optional_class((Decimal, float), 1, 1.0)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")
        with self.assertRaises(AssertionError) as cm:
            assert_optional_class((Decimal, float), 1.0, 1)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")
        with self.assertRaises(AssertionError) as cm:
            assert_optional_class((Decimal, float), 1, None)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")
        with self.assertRaises(AssertionError) as cm:
            assert_optional_class((Decimal, float), None, 1)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")


    def test_assert_classname_1class_1val_pos(self):
        assert_classname('Decimal', Decimal(1))

    def test_assert_classname_1class_1val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_classname('Decimal', 5.0)
        self.assertEqual(str(cm.exception), "'float' != 'Decimal'")

    def test_assert_classname_2class_1val_pos(self):
        assert_classname(('Decimal', 'float'), Decimal(1))
        assert_classname(('Decimal', 'float'), 2.0)

    def test_assert_classname_2class_1val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_classname(('Decimal', 'float'), 1)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")

    def test_assert_classname_2class_2val_pos(self):
        assert_classname(('Decimal', 'float'), Decimal(1), Decimal(2))
        assert_classname(('Decimal', 'float'), 2.0, 3.0)
        assert_classname(('Decimal', 'float'), Decimal(1), 2.0)

    def test_assert_classname_2class_2val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_classname(('Decimal', 'float'), 1, 1.0)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")
        with self.assertRaises(AssertionError) as cm:
            assert_classname(('Decimal', 'float'), 1.0, 1)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")


    def test_assert_optional_classname_1class_1val_pos(self):
        assert_optional_classname('Decimal', Decimal(1))
        assert_optional_classname('Decimal', None)

    def test_assert_optional_classname_1class_1val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_optional_classname('Decimal', 5.0)
        self.assertEqual(str(cm.exception), "'float' != 'Decimal'")

    def test_assert_optional_classname_2class_1val_pos(self):
        assert_optional_classname(('Decimal', 'float'), Decimal(1))
        assert_optional_classname(('Decimal', 'float'), 2.0)
        assert_optional_classname(('Decimal', 'float'), None)

    def test_assert_optional_classname_2class_1val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_optional_classname(('Decimal', 'float'), 1)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")

    def test_assert_optional_classname_2class_2val_pos(self):
        assert_optional_classname(('Decimal', 'float'), Decimal(1), Decimal(2))
        assert_optional_classname(('Decimal', 'float'), 2.0, 3.0)
        assert_optional_classname(('Decimal', 'float'), None, Decimal(2))
        assert_optional_classname(('Decimal', 'float'), 2.0, None)

    def test_assert_optional_classname_2class_2val_neg(self):
        with self.assertRaises(AssertionError) as cm:
            assert_optional_classname(('Decimal', 'float'), 1, 1.0)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")
        with self.assertRaises(AssertionError) as cm:
            assert_optional_classname(('Decimal', 'float'), 1.0, 1)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")
        with self.assertRaises(AssertionError) as cm:
            assert_optional_classname(('Decimal', 'float'), 1, None)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")
        with self.assertRaises(AssertionError) as cm:
            assert_optional_classname(('Decimal', 'float'), None, 1)
        self.assertEqual(str(cm.exception), "'int' not in 'Decimal', 'float'")


    def test_disable_type_checking(self):
        disable_type_checking()
        assert_class(Decimal, 1)
        assert_optional_class(Decimal, 1)
        assert_classname(Decimal, 1)
        assert_optional_classname(Decimal, 1)

    def test_enable_type_checking(self):
        disable_type_checking()
        enable_type_checking()
        with self.assertRaises(AssertionError) as cm:
            assert_class(Decimal, 5.0)
        self.assertEqual(str(cm.exception), "'float' != 'Decimal'")
        with self.assertRaises(AssertionError) as cm:
            assert_optional_class(Decimal, 5.0)
        self.assertEqual(str(cm.exception), "'float' != 'Decimal'")
        with self.assertRaises(AssertionError) as cm:
            assert_classname('Decimal', 5.0)
        self.assertEqual(str(cm.exception), "'float' != 'Decimal'")
        with self.assertRaises(AssertionError) as cm:
            assert_optional_classname('Decimal', 5.0)
        self.assertEqual(str(cm.exception), "'float' != 'Decimal'")


if __name__ == '__main__':
    unittest.main()
