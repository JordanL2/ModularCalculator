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
        calculator.funcs['concat_arrays'] = FunctionDefinition(
            'Arrays', 
            'concat_arrays', 
            'Concatenate two arrays',
            ['array', 'array'],
            ArrayFunctionsFeature.func_array_concat, 
            2, 
            2)#, 
            #'array')
        calculator.funcs['concat_arrays'].array_inputs_raw = True

        calculator.funcs['element'] = FunctionDefinition(
            'Arrays', 
            'element', 
            'Fetch a single element from an array',
            ['array', 'array'],
            ArrayFunctionsFeature.func_array_element, 
            2, 
            2)#, 
            #'array')
        calculator.funcs['element'].array_inputs_raw = True

        calculator.funcs['elements'] = FunctionDefinition(
            'Arrays', 
            'elements', 
            'Fetch a set of elements from an array, making a new array',
            ['array', 'array'],
            ArrayFunctionsFeature.func_array_elements, 
            2, 
            2)#, 
            #'array')
        calculator.funcs['elements'].array_inputs_raw = True

        calculator.funcs['filter'] = FunctionDefinition(
            'Arrays', 
            'filter', 
            'Filter an array',
            ['array', 'array'],
            ArrayFunctionsFeature.func_array_filter, 
            2, 
            2)#, 
            #'array')
        calculator.funcs['filter'].array_inputs_raw = True


    def func_array_concat(self, vals, units, refs, flags):
        res =  OperationResult()
        res.set_unit(units[0])
        return res

    def func_array_element(self, vals, units, refs, flags):
        res =  OperationResult()
        res.set_unit(units[0])
        return res

    def func_array_elements(self, vals, units, refs, flags):
        res =  OperationResult()
        res.set_unit(units[0])
        return res

    def func_array_filter(self, vals, units, refs, flags):
        res =  OperationResult()
        res.set_unit(units[0])
        return res
