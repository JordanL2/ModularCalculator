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
        return ['structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['sum'] = FunctionDefinition(
            'Statistics', 
            'sum', 
            'Sum all values',
            ['number', '...'],
            StatisticalFunctionsFeature.func_sum, 
            1, 
            None, 
            'number')
        calculator.funcs['min'] = FunctionDefinition(
            'Statistics', 
            'min', 
            'Minimum of all values',
            ['number', '...'],
            StatisticalFunctionsFeature.func_min, 
            1, 
            None, 
            'number')
        calculator.funcs['max'] = FunctionDefinition(
            'Statistics', 
            'max', 
            'Maximum of all values',
            ['number', '...'],
            StatisticalFunctionsFeature.func_max, 
            1, 
            None, 
            'number')
        calculator.funcs['mean'] = FunctionDefinition(
            'Statistics', 
            'mean', 
            'Average of all values',
            ['number', '...'],
            StatisticalFunctionsFeature.func_mean, 
            1, 
            None, 
            'number')
        calculator.funcs['median'] = FunctionDefinition(
            'Statistics', 
            'median', 
            'Median of all values',
            ['number', '...'],
            StatisticalFunctionsFeature.func_median, 
            1, 
            None, 
            'number')
        calculator.funcs['mode'] = FunctionDefinition(
            'Statistics', 
            'mode', 
            'Mode of all values',
            ['number', '...'],
            StatisticalFunctionsFeature.func_mode, 
            1, 
            None, 
            'number')
        calculator.funcs['stdev'] = FunctionDefinition(
            'Statistics', 
            'stdev', 
            'Standard deviation of all values',
            ['number', '...'],
            StatisticalFunctionsFeature.func_stdev, 
            1, 
            None, 
            'number')


    def func_sum(self, vals, units, refs, flags):
        return OperationResult(Decimal(sum(vals)))

    def func_min(self, vals, units, refs, flags):
        return OperationResult(Decimal(min(vals)))

    def func_max(self, vals, units, refs, flags):
        return OperationResult(Decimal(max(vals)))

    def func_mean(self, vals, units, refs, flags):
        return OperationResult(Decimal(statistics.mean(vals)))

    def func_median(self, vals, units, refs, flags):
        return OperationResult(Decimal(statistics.median(vals)))

    def func_mode(self, vals, units, refs, flags):
        return OperationResult(Decimal(statistics.mode(vals)))

    def func_stdev(self, vals, units, refs, flags):
        return OperationResult(Decimal(statistics.stdev(vals)))
