#!/usr/bin/python3

from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *

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
        total = Number(0)
        for v in values:
            total += v
        return OperationResult(total)

    def func_min(self, vals, units, refs, flags):
        min_val = min(vals[0], key=lambda x: x.value)
        res = OperationResult(min_val.original_value)
        res.set_unit(min_val.original_unit)
        res.set_ref(min_val.ref)
        return res

    def func_max(self, vals, units, refs, flags):
        max_val = max(vals[0], key=lambda x: x.value)
        res = OperationResult(max_val.original_value)
        res.set_unit(max_val.original_unit)
        res.set_ref(max_val.ref)
        return res

    def func_mean(self, vals, units, refs, flags):
        values = [v.value.to_decimal() for v in vals[0]]
        return OperationResult(Number(statistics.mean(values)))

    def func_median(self, vals, units, refs, flags):
        values = [v.value.to_decimal() for v in vals[0]]
        return OperationResult(Number(statistics.median(values)))

    def func_mode(self, vals, units, refs, flags):
        values = [v.value.to_decimal() for v in vals[0]]
        return OperationResult(Number(statistics.mode(values)))

    def func_stdev(self, vals, units, refs, flags):
        values = [v.value.to_decimal() for v in vals[0]]
        return OperationResult(Number(statistics.stdev(values)))
