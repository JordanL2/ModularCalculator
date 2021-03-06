#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature

from decimal import *
import math
import statistics


class NumericalFunctionsFeature(Feature):

    def id():
        return 'numerical.numericalfunctions'

    def category():
        return 'Numerical'

    def title():
        return 'Numerical Functions'

    def desc():
        return 'Standard numerical functions'

    def dependencies():
        return ['structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['abs'] = FunctionDefinition(
            'Numerical', 
            'abs', 
            'Absolute',
            ['number'],
            NumericalFunctionsFeature.func_abs, 
            1, 
            1, 
            'number')

        calculator.funcs['floor'] = FunctionDefinition(
            'Numerical', 
            'floor', 
            'Round downwards to nearest integer',
            ['number'],
            NumericalFunctionsFeature.func_floor, 
            1, 
            1, 
            'number')

        calculator.funcs['ceil'] = FunctionDefinition(
            'Numerical', 
            'ceil', 
            'Round upwards to nearest integer',
            ['number'],
            NumericalFunctionsFeature.func_ceil, 
            1, 
            1, 
            'number')

        calculator.funcs['round'] = FunctionDefinition(
            'Numerical', 
            'round', 
            'Round to nearest integer or number of decimal places',
            ['number', '[places]'],
            NumericalFunctionsFeature.func_round, 
            1, 
            2, 
            'number')
        calculator.funcs['round'].units_normalise = False

        calculator.funcs['fact'] = FunctionDefinition(
            'Numerical', 
            'fact', 
            'Factorial',
            ['number'],
            NumericalFunctionsFeature.func_fact, 
            1, 
            1, 
            'number')

        calculator.funcs['exp'] = FunctionDefinition(
            'Numerical', 
            'exp', 
            'Return e to the power of given number',
            ['number'],
            NumericalFunctionsFeature.func_exp, 
            1, 
            1, 
            'number')

        calculator.funcs['log'] = FunctionDefinition(
            'Numerical', 
            'log', 
            'Natural logarithm, or logarithm to given base',
            ['number', '[base]'],
            NumericalFunctionsFeature.func_log, 
            1, 
            2, 
            'number')


    def func_abs(self, vals, units, refs, flags):
        res =  OperationResult(Decimal(abs(vals[0])))
        res.set_unit(units[0])
        return res

    def func_floor(self, vals, units, refs, flags):
        res =  OperationResult(Decimal(math.floor(vals[0])))
        res.set_unit(units[0])
        return res

    def func_ceil(self, vals, units, refs, flags):
        res =  OperationResult(Decimal(math.ceil(vals[0])))
        res.set_unit(units[0])
        return res

    def func_round(self, vals, units, refs, flags):
        if len(vals) == 1:
            res = OperationResult(Decimal(round(vals[0])))
        else:
            res = OperationResult(Decimal(round(vals[0], int(vals[1]))))
        res.set_unit(units[0])
        return res

    def func_fact(self, vals, units, refs, flags):
        res =  OperationResult(Decimal(math.factorial(int(vals[0]))))
        res.set_unit(units[0])
        return res

    def func_exp(self, vals, units, refs, flags):
        res =  OperationResult(Decimal(math.exp(vals[0])))
        res.set_unit(units[0])
        return res

    def func_log(self, vals, units, refs, flags):
        num = vals[0]
        if len(vals) == 1:
            res = OperationResult(Decimal(math.log(num)))
        else:
            base = int(vals[1])
            result = Decimal(math.log(num, base))
            res = OperationResult(result)
        res.set_unit(units[0])
        return res
