#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.operators import OperationResult, OperatorDefinition
from modularcalculator.objects.units import *
from modularcalculator.features.feature import Feature


class BasicArithmeticFeature(Feature):

    def id():
        return 'numerical.basicarithmetic'

    def category():
        return 'Numerical'

    def title():
        return 'Basic Arithmetic'

    def desc():
        return '+, -, /, *, ^'

    def dependencies():
        return ['structure.operators']

    @classmethod
    def install(cls, calculator):
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            '^', 
            '', #TODO
            BasicArithmeticFeature.op_number_power, 
            1, 
            1, 
            [['number', 'unit'], 'number']),
        {'units_normalise': False})
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            '*', 
            '', #TODO
            BasicArithmeticFeature.op_number_multiply, 
            1, 
            1, 
            [['number', 'unit'], ['number', 'unit']]), 
        {'units_relative': True, 'units_multi': True})
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            '/', 
            '', #TODO
            BasicArithmeticFeature.op_number_divide, 
            1, 
            1, 
            [['number', 'unit'], ['number', 'unit']]), 
        {'units_relative': True, 'units_multi': True})
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            '+', 
            '', #TODO
            BasicArithmeticFeature.op_number_add, 
            1, 
            1, 
            'number'), 
        {'units_relative': True})
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            '-', 
            '', #TODO
            BasicArithmeticFeature.op_number_subtract, 
            1, 
            1, 
            'number'), 
        {'units_relative': True})
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            'IMPLICIT_MULTIPLY', 
            '', #TODO
            BasicArithmeticFeature.op_number_multiply, 
            1, 
            1, 
            'number'), 
        {'units_relative': True, 'units_multi': True, 'hidden': True})
        calculator.implicit_multiply_op = 'IMPLICIT_MULTIPLY'
        calculator.multiply_op = '*'
        calculator.divide_op = '/'

    def op_number_power(self, vals, units, refs, flags):
        power = self.number(vals[1])
        if isinstance(vals[0], UnitPowerList):
            unit = vals[0].power(power)
            return OperationResult(unit)
        res = OperationResult(self.number(vals[0]) ** power)
        if units[1] is not None:
            raise CalculatorException("Power operand must be simple number")
        if units[0] is not None:
            res.set_unit(units[0].power(power))
        return res

    def op_number_multiply(self, vals, units, refs, flags):
        if isinstance(vals[0], UnitPowerList) and isinstance(vals[1], UnitPowerList):
            unit = UnitPowerList.new([vals[0], 1, vals[1], 1])
            unit.no_simplify = True
            return OperationResult(unit)
        for i in range(0, len(vals)):
            if isinstance(vals[i], UnitPowerList):
                units[i] = vals[i]
                vals[i] = Decimal('1')
        res = OperationResult(self.number(vals[0]) * self.number(vals[1]))
        if units[0] is not None and units[1] is not None:
            unit = UnitPowerList.new([units[0], 1, units[1], 1])
            res.set_unit(unit)
        elif units[0] is not None:
            res.set_unit(units[0])
        elif units[1] is not None:
            res.set_unit(units[1])
        return res

    def op_number_divide(self, vals, units, refs, flags):
        if isinstance(vals[0], UnitPowerList) and isinstance(vals[1], UnitPowerList):
            unit = UnitPowerList.new([vals[0], 1, vals[1], -1])
            unit.no_simplify = True
            return OperationResult(unit)
        for i in range(0, len(vals)):
            if isinstance(vals[i], UnitPowerList):
                units[i] = vals[i]
                vals[i] = Decimal('1')
        res = OperationResult(self.number(vals[0]) / self.number(vals[1]))
        if units[0] is not None and units[1] is not None:
            unit = UnitPowerList.new([units[0], 1, units[1], -1])
            res.set_unit(unit)
        elif units[0] is not None and units[1] is None:
            res.set_unit(units[0])
        elif units[0] is None and units[1] is not None:
            unit = units[1].power(-1)
            unit.no_simplify = units[1].no_simplify
            res.set_unit(unit)
        return res

    def op_number_add(self, vals, units, refs, flags):
        return OperationResult(self.number(vals[0]) + self.number(vals[1]))

    def op_number_subtract(self, vals, units, refs, flags):
        return OperationResult(self.number(vals[0]) - self.number(vals[1]))
