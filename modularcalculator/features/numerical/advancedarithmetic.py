#!/usr/bin/python3

from modularcalculator.objects.operators import OperationResult, OperatorDefinition
from modularcalculator.features.feature import Feature
from modularcalculator.objects.items import OperandResult
from modularcalculator.objects.number import *
from modularcalculator.features.numerical.basicarithmetic import BasicArithmeticFeature

import math


class AdvancedArithmeticFeature(Feature):

    def id():
        return 'numerical.advancedarithmetic'

    def category():
        return 'Numerical'

    def title():
        return 'Advanced Arithmetic'

    def desc():
        return 'Adds some advanced arithmetic operators: % (modulus), \\ (integer divide)'

    def dependencies():
        return ['structure.operators']

    @classmethod
    def install(cls, calculator):
        calculator.add_op(OperatorDefinition(
            'Numerical',
            '%',
            'Modulus',
            AdvancedArithmeticFeature.op_number_modulus,
            1,
            1,
            'number'))
        calculator.add_op(OperatorDefinition(
            'Numerical',
            '\\',
            'Integer divide - Truncates non-integer component',
            AdvancedArithmeticFeature.op_number_integer_divide,
            1,
            1,
            'number'))

    def op_number_modulus(self, vals, units, refs, flags):
        return OperationResult(vals[0] % vals[1])

    def op_number_integer_divide(self, vals, units, refs, flags):
        op = self.ops_list['/']
        division_result = op.call(self, [OperandResult(vals[0], units[0], None), OperandResult(vals[1], units[1], None)], flags)
        res = OperationResult(math.floor(division_result.value))
        res.set_unit(division_result.unit)
        return res
