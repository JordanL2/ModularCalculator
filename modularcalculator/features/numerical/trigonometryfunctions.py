#!/usr/bin/python3

from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *

import math
import statistics


class TrigonometryFunctionsFeature(Feature):

    def id():
        return 'numerical.trigonometryfunctions'

    def category():
        return 'Numerical'

    def title():
        return 'Trigonometry Functions'

    def desc():
        return 'Sine, cosine etc functions'

    def dependencies():
        return ['structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['sin'] = FunctionDefinition(
            'Trigonometry',
            'sin',
            'Sine',
            ['radians'],
            TrigonometryFunctionsFeature.func_sin,
            1,
            1,
            'number')
        calculator.funcs['cos'] = FunctionDefinition(
            'Trigonometry',
            'cos',
            'Cosine',
            ['radians'],
            TrigonometryFunctionsFeature.func_cos,
            1,
            1,
            'number')
        calculator.funcs['tan'] = FunctionDefinition(
            'Trigonometry',
            'tan',
            'Tangent',
            ['radians'],
            TrigonometryFunctionsFeature.func_tan,
            1,
            1,
            'number')
        calculator.funcs['asin'] = FunctionDefinition(
            'Trigonometry',
            'asin',
            'Inverse sine',
            ['radians'],
            TrigonometryFunctionsFeature.func_asin,
            1,
            1,
            'number')
        calculator.funcs['acos'] = FunctionDefinition(
            'Trigonometry',
            'acos',
            'Inverse cosine',
            ['radians'],
            TrigonometryFunctionsFeature.func_acos,
            1,
            1,
            'number')
        calculator.funcs['atan'] = FunctionDefinition(
            'Trigonometry',
            'atan',
            'Inverse tangent',
            ['radians'],
            TrigonometryFunctionsFeature.func_atan,
            1,
            1,
            'number')
        calculator.funcs['sinh'] = FunctionDefinition(
            'Trigonometry',
            'sinh',
            'Hyperbolic sine',
            ['radians'],
            TrigonometryFunctionsFeature.func_sinh,
            1,
            1,
            'number')
        calculator.funcs['cosh'] = FunctionDefinition(
            'Trigonometry',
            'cosh',
            'Hyperbolic cosine',
            ['radians'],
            TrigonometryFunctionsFeature.func_cosh,
            1,
            1,
            'number')
        calculator.funcs['tanh'] = FunctionDefinition(
            'Trigonometry',
            'tanh',
            'Hyperbolic tangent',
            ['radians'],
            TrigonometryFunctionsFeature.func_tanh,
            1,
            1,
            'number')
        calculator.funcs['asinh'] = FunctionDefinition(
            'Trigonometry',
            'asinh',
            'Inverse hyperbolic sine',
            ['radians'],
            TrigonometryFunctionsFeature.func_asinh,
            1,
            1,
            'number')
        calculator.funcs['acosh'] = FunctionDefinition(
            'Trigonometry',
            'acosh',
            'Inverse hyperbolic cosine',
            ['radians'],
            TrigonometryFunctionsFeature.func_acosh,
            1,
            1,
            'number')
        calculator.funcs['atanh'] = FunctionDefinition(
            'Trigonometry',
            'atanh',
            'Inverse hyperbolic tangent',
            ['radians'],
            TrigonometryFunctionsFeature.func_atanh,
            1,
            1,
            'number')


    def func_sin(self, vals, units, refs, flags):
        return OperationResult(math.sin(vals[0]))

    def func_cos(self, vals, units, refs, flags):
        return OperationResult(math.cos(vals[0]))

    def func_tan(self, vals, units, refs, flags):
        return OperationResult(math.tan(vals[0]))

    def func_asin(self, vals, units, refs, flags):
        return OperationResult(math.asin(vals[0]))

    def func_acos(self, vals, units, refs, flags):
        return OperationResult(math.acos(vals[0]))

    def func_atan(self, vals, units, refs, flags):
        return OperationResult(math.atan(vals[0]))

    def func_sinh(self, vals, units, refs, flags):
        return OperationResult(math.sinh(vals[0]))

    def func_cosh(self, vals, units, refs, flags):
        return OperationResult(math.cosh(vals[0]))

    def func_tanh(self, vals, units, refs, flags):
        return OperationResult(math.tanh(vals[0]))

    def func_asinh(self, vals, units, refs, flags):
        return OperationResult(math.asinh(vals[0]))

    def func_acosh(self, vals, units, refs, flags):
        return OperationResult(math.acosh(vals[0]))

    def func_atanh(self, vals, units, refs, flags):
        return OperationResult(math.atanh(vals[0]))
