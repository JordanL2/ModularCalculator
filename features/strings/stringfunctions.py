#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.operators import OperationResult
from modularcalculator.features.strings.strings import StringsFeature
from modularcalculator.features.structure.functions import FunctionDefinition
from modularcalculator.features.feature import Feature

from decimal import *


class StringFunctionsFeature(Feature):

    def id():
        return 'strings.stringfunctions'

    def category():
        return 'String'

    def title():
        return 'String Functions'

    def desc():
        return 'Functions to manipulate strings'

    def dependencies():
        return ['strings.strings','structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['length'] =  FunctionDefinition(
            'String', 
            'length', 
            'Length of string',
            ['string'],
            StringFunctionsFeature.func_length, 
            1, 
            1, 
            'string')

        calculator.funcs['lower'] =   FunctionDefinition(
            'String', 
            'lower', 
            'Lower-case a string',
            ['string'],
            StringFunctionsFeature.func_lower, 
            1, 
            1, 
            'string')

        calculator.funcs['upper'] =   FunctionDefinition(
            'String', 
            'upper', 
            'Upper-case a string',
            ['string'],
            StringFunctionsFeature.func_upper, 
            1, 
            1, 
            'string')

        calculator.funcs['lstrip'] =  FunctionDefinition(
            'String', 
            'lstrip', 
            'Remove all occurrences of a character from the left',
            ['string', 'character'],
            StringFunctionsFeature.func_lstrip, 
            2, 
            2, 
            'string')

        calculator.funcs['rstrip'] =  FunctionDefinition(
            'String', 
            'rstrip', 
            'Remove all occurrences of a character from the right',
            ['string', 'character'],
            StringFunctionsFeature.func_rstrip, 
            2, 
            2, 
            'string')

        calculator.funcs['strip'] =   FunctionDefinition(
            'String', 
            'strip', 
            'Remove all occurrences of a character from both ends',
            ['string', 'character'],
            StringFunctionsFeature.func_strip, 
            2, 
            2, 
            'string')

        calculator.funcs['find'] =    FunctionDefinition(
            'String', 
            'find', 
            'Return position of a substring in a string',
            ['string', 'substring'],
            StringFunctionsFeature.func_find, 
            2, 
            2, 
            'string')

        calculator.funcs['replace'] = FunctionDefinition(
            'String', 
            'replace', 
            'Replace all occurrences of substring with replacement',
            ['string', 'substring', 'replacement'],
            StringFunctionsFeature.func_replace, 
            3, 
            3, 
            'string')
        
        calculator.funcs['substr'] =  FunctionDefinition(
            'String', 
            'substr', 
            'Return characters in a string from start position, optionally to end position',
            ['string', 'start', 'end'],
            StringFunctionsFeature.func_substr, 
            2, 
            3)
        calculator.funcs['substr'].add_value_restriction(0, 0, 'string')
        calculator.funcs['substr'].add_value_restriction(1, 2, 'number')
        calculator.funcs['substr'].auto_convert_numerical_result = False

    def func_length(self, vals, units, refs, flags):
        return OperationResult(Decimal(len(StringsFeature.string(self, vals[0]))))

    def func_lower(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).lower())

    def func_upper(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).upper())

    def func_lstrip(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).lstrip(vals[1]))

    def func_rstrip(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).rstrip(StringsFeature.string(self, vals[1])))

    def func_strip(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).strip(StringsFeature.string(self, vals[1])))

    def func_find(self, vals, units, refs, flags):
        return OperationResult(Decimal(StringsFeature.string(self, vals[0]).find(StringsFeature.string(self, vals[1]))))

    def func_replace(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).replace(StringsFeature.string(self, vals[1]), StringsFeature.string(self, vals[2])))

    def func_substr(self, vals, units, refs, flags):
        start = int(vals[1])
        if len(vals) == 2:
            return OperationResult(StringsFeature.string(self, vals[0])[start:])
        elif len(vals) == 3:
            end = int(vals[2]) + 1
            if end <= 0:
                end += len(vals[0])
            return OperationResult(StringsFeature.string(self, vals[0])[start:end])
        else:
            raise CalculatorException("substr needs either 2 or 3 arguments, found {0}".format(len(vals)))
