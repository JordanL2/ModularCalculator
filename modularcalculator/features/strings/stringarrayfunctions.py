#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.operators import OperationResult
from modularcalculator.features.strings.strings import StringsFeature
from modularcalculator.features.structure.functions import FunctionDefinition
from modularcalculator.features.feature import Feature

from decimal import *


class StringArrayFunctionsFeature(Feature):

    def id():
        return 'strings.stringarrayfunctions'

    def category():
        return 'String'

    def title():
        return 'String Array Functions'

    def desc():
        return 'Functions to split/join strings'

    def dependencies():
        return ['strings.strings','structure.functions','arrays.arrays']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['split'] =  FunctionDefinition(
            'String', 
            'split', 
            'Split a string on a delimiter',
            ['string', 'delimiter'],
            StringArrayFunctionsFeature.func_split, 
            2, 
            2, 
            'string')

        calculator.funcs['join'] =   FunctionDefinition(
            'String', 
            'join', 
            'Join an array of strings together, joined by a delimiter',
            ['strings', 'delimiter'],
            StringArrayFunctionsFeature.func_join, 
            2, 
            2)
        calculator.funcs['join'].add_value_restriction(0, 0, 'array[string]')
        calculator.funcs['join'].add_value_restriction(1, 1, 'string')

    def func_split(self, vals, units, refs, flags):
        string = StringsFeature.string(self, vals[0])
        splitter = StringsFeature.string(self, vals[1])
        results = [OperandResult(r, None, None) for r in string.split(splitter)]
        return OperationResult(results)

    def func_join(self, vals, units, refs, flags):
        delimiter = vals[1]
        values = [StringsFeature.string(self, v.value) for v in vals[0]]
        return OperationResult(vals[1].join(values))
