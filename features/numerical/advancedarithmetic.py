#!/usr/bin/python3

from modularcalculator.objects.operators import OperationResult, OperatorDefinition
from modularcalculator.features.feature import Feature

import math
from decimal import *


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
        calculator.add_op(OperatorDefinition('Numerical', '%', AdvancedArithmeticFeature.op_number_modulus, 1, 1, 'number'))
        calculator.add_op(OperatorDefinition('Numerical', '\\', AdvancedArithmeticFeature.op_number_integer_divide, 1, 1, 'number'))

    def op_number_modulus(self, vals, units, refs, flags):
        return OperationResult(self.number(vals[0]) % self.number(vals[1]))

    def op_number_integer_divide(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.floor(self.number(vals[0]) / self.number(vals[1]))))
