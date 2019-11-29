#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature

from decimal import *
import math
import statistics


class StatisticalFunctionsFeature(Feature):

    def id():
        return 'numerical.statisticalfunctions'

    def category():
        return 'Numerical'

    def title():
        return 'Statistical Functions'

    def desc():
        return 'Sum, mean, median, standard deviation etc'

    def dependencies():
        return ['structure.functions', 'arrays.arrays']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['sum'] = FunctionDefinition(
            'Statistics', 
            'sum', 
            'Sum all values',
            ['array[number]'],
            StatisticalFunctionsFeature.func_sum, 
            1, 
            1, 
            'array[number]')

        calculator.funcs['min'] = FunctionDefinition(
            'Statistics', 
            'min', 
            'Minimum of all values',
            ['array[number]'],
            StatisticalFunctionsFeature.func_min, 
            1, 
            1, 
            'array[number]')

        calculator.funcs['max'] = FunctionDefinition(
            'Statistics', 
            'max', 
            'Maximum of all values',
            ['array[number]'],
            StatisticalFunctionsFeature.func_max, 
            1, 
            1, 
            'array[number]')

        calculator.funcs['mean'] = FunctionDefinition(
            'Statistics', 
            'mean', 
            'Average of all values',
            ['array[number]'],
            StatisticalFunctionsFeature.func_mean, 
            1, 
            1, 
            'array[number]')

        calculator.funcs['median'] = FunctionDefinition(
            'Statistics', 
            'median', 
            'Median of all values',
            ['array[number]'],
            StatisticalFunctionsFeature.func_median, 
            1, 
            1, 
            'array[number]')

        calculator.funcs['mode'] = FunctionDefinition(
            'Statistics', 
            'mode', 
            'Mode of all values',
            ['array[number]'],
            StatisticalFunctionsFeature.func_mode, 
            1, 
            1, 
            'array[number]')

        calculator.funcs['stdev'] = FunctionDefinition(
            'Statistics', 
            'stdev', 
            'Standard deviation of all values',
            ['array[number]'],
            StatisticalFunctionsFeature.func_stdev, 
            1, 
            1, 
            'array[number]')


    def func_sum(self, vals, units, refs, flags):
        values = [v.value for v in vals[0]]
        return OperationResult(Decimal(sum(values)))

    def func_min(self, vals, units, refs, flags):
        min_val = min(vals[0], key=lambda x: x.value)
        res = OperationResult(min_val.value)
        res.set_ref(min_val.ref)
        res.original_value = min_val.original_value
        res.original_unit = min_val.original_unit
        return res

    def func_max(self, vals, units, refs, flags):
        values = [v.value for v in vals[0]]
        return OperationResult(Decimal(max(values)))

    def func_mean(self, vals, units, refs, flags):
        values = [v.value for v in vals[0]]
        return OperationResult(Decimal(statistics.mean(values)))

    def func_median(self, vals, units, refs, flags):
        values = [v.value for v in vals[0]]
        return OperationResult(Decimal(statistics.median(values)))

    def func_mode(self, vals, units, refs, flags):
        values = [v.value for v in vals[0]]
        return OperationResult(Decimal(statistics.mode(values)))

    def func_stdev(self, vals, units, refs, flags):
        values = [v.value for v in vals[0]]
        return OperationResult(Decimal(statistics.stdev(values)))
