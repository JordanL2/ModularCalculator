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
        return 'Standard numerical, statistical, trigonometry functions'

    def dependencies():
        return ['structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['abs'] = FunctionDefinition('Numerical', 'abs', NumericalFunctionsFeature.func_abs, 1, 1, 'number')
        calculator.funcs['floor'] = FunctionDefinition('Numerical', 'floor', NumericalFunctionsFeature.func_floor, 1, 1, 'number')
        calculator.funcs['ceil'] = FunctionDefinition('Numerical', 'ceil', NumericalFunctionsFeature.func_ceil, 1, 1, 'number')
        calculator.funcs['round'] = FunctionDefinition('Numerical', 'round', NumericalFunctionsFeature.func_round, 1, 2, 'number')
        calculator.funcs['round'].units_normalise = False
        calculator.funcs['fact'] = FunctionDefinition('Numerical', 'fact', NumericalFunctionsFeature.func_fact, 1, 1, 'number')
        calculator.funcs['exp'] = FunctionDefinition('Numerical', 'exp', NumericalFunctionsFeature.func_exp, 1, 1, 'number')
        calculator.funcs['log'] = FunctionDefinition('Numerical', 'log', NumericalFunctionsFeature.func_log, 1, 1, 'number')
        
        calculator.funcs['sin'] = FunctionDefinition('Trigonometry', 'sin', NumericalFunctionsFeature.func_sin, 1, 1, 'number')
        calculator.funcs['cos'] = FunctionDefinition('Trigonometry', 'cos', NumericalFunctionsFeature.func_cos, 1, 1, 'number')
        calculator.funcs['tan'] = FunctionDefinition('Trigonometry', 'tan', NumericalFunctionsFeature.func_tan, 1, 1, 'number')
        calculator.funcs['asin'] = FunctionDefinition('Trigonometry', 'asin', NumericalFunctionsFeature.func_asin, 1, 1, 'number')
        calculator.funcs['acos'] = FunctionDefinition('Trigonometry', 'acos', NumericalFunctionsFeature.func_acos, 1, 1, 'number')
        calculator.funcs['atan'] = FunctionDefinition('Trigonometry', 'atan', NumericalFunctionsFeature.func_atan, 1, 1, 'number')
        calculator.funcs['sinh'] = FunctionDefinition('Trigonometry', 'sinh', NumericalFunctionsFeature.func_sinh, 1, 1, 'number')
        calculator.funcs['cosh'] = FunctionDefinition('Trigonometry', 'cosh', NumericalFunctionsFeature.func_cosh, 1, 1, 'number')
        calculator.funcs['tanh'] = FunctionDefinition('Trigonometry', 'tanh', NumericalFunctionsFeature.func_tanh, 1, 1, 'number')
        calculator.funcs['asinh'] = FunctionDefinition('Trigonometry', 'asinh', NumericalFunctionsFeature.func_asinh, 1, 1, 'number')
        calculator.funcs['acosh'] = FunctionDefinition('Trigonometry', 'acosh', NumericalFunctionsFeature.func_acosh, 1, 1, 'number')
        calculator.funcs['atanh'] = FunctionDefinition('Trigonometry', 'atanh', NumericalFunctionsFeature.func_atanh, 1, 1, 'number')

        calculator.funcs['sum'] = FunctionDefinition('Statistics', 'sum', NumericalFunctionsFeature.func_sum, 1, None, 'number')
        calculator.funcs['min'] = FunctionDefinition('Statistics', 'min', NumericalFunctionsFeature.func_min, 1, None, 'number')
        calculator.funcs['max'] = FunctionDefinition('Statistics', 'max', NumericalFunctionsFeature.func_max, 1, None, 'number')
        calculator.funcs['mean'] = FunctionDefinition('Statistics', 'mean', NumericalFunctionsFeature.func_mean, 1, None, 'number')
        calculator.funcs['median'] = FunctionDefinition('Statistics', 'median', NumericalFunctionsFeature.func_median, 1, None, 'number')
        calculator.funcs['mode'] = FunctionDefinition('Statistics', 'mode', NumericalFunctionsFeature.func_mode, 1, None, 'number')
        calculator.funcs['stdev'] = FunctionDefinition('Statistics', 'stdev', NumericalFunctionsFeature.func_stdev, 1, None, 'number')

    def func_abs(self, vals, units, refs, flags):
        return OperationResult(Decimal(abs(self.number(vals[0]))))

    def func_floor(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.floor(self.number(vals[0]))))

    def func_ceil(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.ceil(self.number(vals[0]))))

    def func_round(self, vals, units, refs, flags):
        if len(vals) == 1:
            res = OperationResult(Decimal(round(self.number(vals[0]))))
        else:
            res = OperationResult(Decimal(round(self.number(vals[0]), int(vals[1]))))
        res.set_unit(units[0])
        return res

    def func_fact(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.factorial(self.number(vals[0]))))

    def func_exp(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.exp(self.number(vals[0]))))

    def func_log(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.log(self.number(vals[0]))))


    def func_sin(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.sin(self.number(vals[0]))))

    def func_cos(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.cos(self.number(vals[0]))))

    def func_tan(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.tan(self.number(vals[0]))))

    def func_asin(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.asin(self.number(vals[0]))))

    def func_acos(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.acos(self.number(vals[0]))))

    def func_atan(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.atan(self.number(vals[0]))))

    def func_sinh(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.sinh(self.number(vals[0]))))

    def func_cosh(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.cosh(self.number(vals[0]))))

    def func_tanh(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.tanh(self.number(vals[0]))))

    def func_asinh(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.asinh(self.number(vals[0]))))

    def func_acosh(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.acosh(self.number(vals[0]))))

    def func_atanh(self, vals, units, refs, flags):
        return OperationResult(Decimal(math.atanh(self.number(vals[0]))))


    def func_sum(self, vals, units, refs, flags):
        return OperationResult(Decimal(sum(self.numbers(vals))))

    def func_min(self, vals, units, refs, flags):
        return OperationResult(Decimal(min(self.numbers(vals))))

    def func_max(self, vals, units, refs, flags):
        return OperationResult(Decimal(max(self.numbers(vals))))

    def func_mean(self, vals, units, refs, flags):
        return OperationResult(Decimal(statistics.mean(self.numbers(vals))))

    def func_median(self, vals, units, refs, flags):
        return OperationResult(Decimal(statistics.median(self.numbers(vals))))

    def func_mode(self, vals, units, refs, flags):
        return OperationResult(Decimal(statistics.mode(self.numbers(vals))))

    def func_stdev(self, vals, units, refs, flags):
        return OperationResult(Decimal(statistics.stdev(self.numbers(vals))))
