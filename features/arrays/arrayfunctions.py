#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.exceptions import *
from modularcalculator.features.feature import Feature
from modularcalculator.features.structure.functions import *


class ArrayFunctionsFeature(Feature):

    def id():
        return 'arrays.arrayfunctions'

    def category():
        return 'Arrays'

    def title():
        return 'Array Functions'

    def desc():
        return 'Functions for manipulating arrays'

    def dependencies():
        return ['arrays.arrays', 'structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['concat'] = FunctionDefinition(
            'Arrays', 
            'concat', 
            'Concatenate two arrays',
            ['array', 'array'],
            ArrayFunctionsFeature.func_array_concat, 
            2, 
            2, 
            'array')

        calculator.funcs['element'] = FunctionDefinition(
            'Arrays', 
            'element', 
            'Fetch a single element from an array',
            ['array', 'number'],
            ArrayFunctionsFeature.func_array_element, 
            2, 
            2)
        calculator.funcs['element'].add_value_restriction(0, 0, ['array'])
        calculator.funcs['element'].add_value_restriction(1, 1, ['number'])

        calculator.funcs['filter'] = FunctionDefinition(
            'Arrays', 
            'filter', 
            'Filter an array based on a second array of booleans',
            ['array', 'array[boolean]'],
            ArrayFunctionsFeature.func_array_filter, 
            2, 
            2)
        calculator.funcs['filter'].add_value_restriction(0, 0, ['array'])
        calculator.funcs['filter'].add_value_restriction(1, 1, ['array[boolean]'])

        calculator.funcs['count'] = FunctionDefinition(
            'Arrays',
            'count',
            'Count the number of elements in an array',
            ['array'],
            ArrayFunctionsFeature.func_array_count,
            1,
            1,
            'array')


    def func_array_concat(self, vals, units, refs, flags):
        res =  OperationResult(vals[0] + vals[1])
        return res

    def func_array_element(self, vals, units, refs, flags):
        array = vals[0]
        index = int(vals[1]) - 1
        element = array[index]
        res =  OperationResult(element.value)
        res.set_unit(element.unit)
        res.set_ref(element.ref)
        return res

    def func_array_filter(self, vals, units, refs, flags):
        new_array = []
        for i, truth in enumerate(vals[1]):
            if truth.value:
                new_array.append(vals[0][i])
        res =  OperationResult(new_array)
        return res

    def func_array_count(self, vals, units, refs, flags):
        res =  OperationResult(Decimal(len(vals[0])))
        return res
