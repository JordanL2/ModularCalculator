#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature

from decimal import *
import math
import statistics


class NumericalFormatFunctionsFeature(Feature):

    def id():
        return 'numerical.numericalformatfunctions'

    def category():
        return 'Numerical'

    def title():
        return 'Numerical Format Functions'

    def desc():
        return 'Functions for formatting numbers'

    def dependencies():
        return ['structure.functions', 'numerical.expnumbers']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['scientific'] = FunctionDefinition(
            'Numerical', 
            'scientific', 
            'Format number in scientific notation',
            ['number', '[places]'],
            NumericalFormatFunctionsFeature.func_scientific, 
            1, 
            2, 
            'number')
        calculator.funcs['scientific'].units_normalise = False


    def func_scientific(self, vals, units, refs, flags):
        num = self.number(vals[0])
        places = 3
        if len(vals) == 2:
            places = self.number(vals[1])
        scientificformat = '{0:.' + str(places) + 'E}'
        formattednumber = scientificformat.format(num)
        formattednumber = formattednumber.replace('+', '')
        res = OperationResult(formattednumber)
        res.set_unit(units[0])
        return res
