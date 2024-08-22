#!/usr/bin/python3

from modularcalculator.features.numerical.numericalconstants import *
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *

from decimal import Decimal
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
            'Round downwards to nearest integer or number of places',
            ['number', '[places]'],
            NumericalFunctionsFeature.func_floor,
            1,
            2,
            'number')
        calculator.funcs['floor'].units_normalise = False

        calculator.funcs['ceil'] = FunctionDefinition(
            'Numerical',
            'ceil',
            'Round upwards to nearest integer or number of places',
            ['number', '[places]'],
            NumericalFunctionsFeature.func_ceil,
            1,
            2,
            'number')
        calculator.funcs['ceil'].units_normalise = False

        calculator.funcs['round'] = FunctionDefinition(
            'Numerical',
            'round',
            'Round to nearest integer or number of places',
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

        calculator.funcs['lcm'] = FunctionDefinition(
            'Numerical',
            'lcm',
            'Lowest common multiple',
            ['number', 'number'],
            NumericalFunctionsFeature.func_lcm,
            2,
            2,
            'number')

        calculator.funcs['gcd'] = FunctionDefinition(
            'Numerical',
            'gcd',
            'Greatest common divisor, or highest common factor',
            ['number', 'number'],
            NumericalFunctionsFeature.func_gcd,
            2,
            2,
            'number')


    def func_abs(self, vals, units, refs, flags):
        res = OperationResult(abs(vals[0]))
        res.set_unit(units[0])
        return res

    def apply_rounding_function(self, vals, units, f):
        places = 0
        if len(vals) > 1:
            places = int(vals[1])
        base = 10
        if vals[0].number_cast is not None and 'base' in vals[0].number_cast:
            base = vals[0].number_cast['base']
        if vals[0].number_cast is not None and 'places_offset' in vals[0].number_cast:
            places += vals[0].number_cast['places_offset']
        p = Number(base ** places)
        val = vals[0]
        val *= p
        val = f(val)
        val /= p
        res = OperationResult(val)
        res.set_unit(units[0])
        return res

    def func_floor(self, vals, units, refs, flags):
        return NumericalFunctionsFeature.apply_rounding_function(self, vals, units, math.floor)

    def func_ceil(self, vals, units, refs, flags):
        return NumericalFunctionsFeature.apply_rounding_function(self, vals, units, math.ceil)

    def func_round(self, vals, units, refs, flags):
        return NumericalFunctionsFeature.apply_rounding_function(self, vals, units, round)

    def func_fact(self, vals, units, refs, flags):
        if vals[0].to_decimal() < 0 or (vals[0] % Number(1)).to_decimal() != 0:
            raise CalculatorException('Operator requires positive integers')
        res = OperationResult(Number(math.factorial(int(vals[0]))))
        res.set_unit(units[0])
        return res

    def func_exp(self, vals, units, refs, flags):
        res = OperationResult(Number(NumericalConstantsFeature.e) ** vals[0])
        res.set_unit(units[0])
        return res

    def func_log(self, vals, units, refs, flags):
        num = vals[0]
        if len(vals) == 1:
            res = OperationResult(num.log())
        else:
            res = OperationResult(num.log(float(vals[1])))
        res.set_unit(units[0])
        return res

    def func_lcm(self, vals, units, refs, flags):
        if (vals[0] % Number(1)).to_decimal() != 0 or (vals[1] % Number(1)).to_decimal() != 0:
            raise CalculatorException('Operator requires integers')
        res = OperationResult(Number(math.lcm(int(vals[0]), int(vals[1]))))
        res.set_unit(units[0])
        return res

    def func_gcd(self, vals, units, refs, flags):
        if (vals[0] % Number(1)).to_decimal() != 0 or (vals[1] % Number(1)).to_decimal() != 0:
            raise CalculatorException('Operator requires integers')
        res = OperationResult(Number(math.gcd(int(vals[0]), int(vals[1]))))
        res.set_unit(units[0])
        return res
