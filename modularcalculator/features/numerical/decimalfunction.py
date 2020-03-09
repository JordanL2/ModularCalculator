#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature


class DecimalFunctionFeature(Feature):

    def id():
        return 'numerical.decimalfunction'

    def category():
        return 'Numerical'

    def title():
        return 'Decimal Function'

    def desc():
        return 'Adds dec function to turn any number into a decimal'

    def dependencies():
        return ['numerical.decimalnumbers','structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['dec'] = FunctionDefinition(
            'Bases', 
            'dec', 
            'Convert a number from any base to base-10',
            ['number'],
            DecimalFunctionFeature.func_dec, 
            1, 
            1, 
            'number')
        calculator.funcs['dec'].auto_convert_numerical_result = False

    def func_dec(self, vals, units, refs, flags):
        return OperationResult(vals[0])
