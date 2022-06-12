#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *
from modularcalculator.objects.operators import OperationResult, OperatorDefinition
from modularcalculator.features.feature import Feature

import math


class BitwiseOperatorsFeature(Feature):

    def id():
        return 'numerical.bitwiseoperators'

    def category():
        return 'Numerical'

    def title():
        return 'Bitwise Operators'

    def desc():
        return 'Adds bitwise operators'

    def dependencies():
        return ['structure.operators']

    @classmethod
    def install(cls, calculator):
        calculator.add_op(OperatorDefinition(
            'Bitwise',
            '&',
            'Bitwise AND',
            BitwiseOperatorsFeature.op_bitwise_and,
            1,
            1,
            'number'))

        calculator.add_op(OperatorDefinition(
            'Bitwise',
            '|',
            'Bitwise OR',
            BitwiseOperatorsFeature.op_bitwise_or,
            1,
            1,
            'number'))

        calculator.add_op(OperatorDefinition(
            'Bitwise',
            '^^',
            'Bitwise XOR',
            BitwiseOperatorsFeature.op_bitwise_xor,
            1,
            1,
            'number'))

        bitwise_not = OperatorDefinition(
            'Bitwise',
            '~',
            'Bitwise Negation (1\'s Complement)',
            BitwiseOperatorsFeature.op_bitwise_not,
            0,
            1,
            'number')
        bitwise_not.auto_convert_numerical_inputs = False
        calculator.add_op(bitwise_not, {'rtl': True})

        calculator.add_op(OperatorDefinition(
            'Bitwise',
            '<<',
            'Bitwise Left Shift',
            BitwiseOperatorsFeature.op_bitwise_lshift,
            1,
            1,
            'number'))

        calculator.add_op(OperatorDefinition(
            'Bitwise',
            '>>',
            'Bitwise Right Shift',
            BitwiseOperatorsFeature.op_bitwise_rshift,
            1,
            1,
            'number'))

    def op_bitwise_and(self, vals, units, refs, flags):
        return OperationResult(Number(int(vals[0]) & int(vals[1])))

    def op_bitwise_or(self, vals, units, refs, flags):
        return OperationResult(Number(int(vals[0]) | int(vals[1])))

    def op_bitwise_xor(self, vals, units, refs, flags):
        return OperationResult(Number(int(vals[0]) ^ int(vals[1])))

    def op_bitwise_not(self, vals, units, refs, flags):
        dec_num = self.number(vals[0])

        if dec_num < Number(0) or dec_num % Number(1) != Number(0):
            raise CalculatorException('Operator requires positive integers')

        int_val = int(dec_num)
        opts = None
        if dec_num.number_cast is not None and len(dec_num.number_cast['args']) > 1:
            opts = dec_num.number_cast['args'][1]
        if opts and 'width' in opts:
            mask_val = 2**opts['width'] - 1
        else:
            mask_val = 2**math.ceil(math.log(int_val, 2)) - 1
        flipped_val = ~int_val
        masked_flipped_val = Number(flipped_val & mask_val, number_cast=vals[0].number_cast)

        return OperationResult(masked_flipped_val)

    def op_bitwise_lshift(self, vals, units, refs, flags):
        return OperationResult(Number(int(vals[0]) << int(vals[1])))

    def op_bitwise_rshift(self, vals, units, refs, flags):
        return OperationResult(Number(int(vals[0]) >> int(vals[1])))
