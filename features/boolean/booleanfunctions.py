#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.operators import OperationResult
from modularcalculator.features.boolean.booleans import BooleansFeature
from modularcalculator.features.structure.functions import FunctionDefinition
from modularcalculator.features.feature import Feature

from decimal import *


class BooleanFunctionsFeature(Feature):

    def id():
        return 'boolean.booleanfunctions'

    def category():
        return 'Boolean'

    def title():
        return 'Boolean Functions'

    def desc():
        return 'and, or, counttrue'

    def dependencies():
        return ['boolean.booleans']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['and'] = FunctionDefinition(
            'Boolean', 
            'and', 
            'Returns true if all input is true', 
            'and(var1...)',
            BooleanFunctionsFeature.func_and, 
            1, 
            None, 
            'boolean')
        calculator.funcs['or'] = FunctionDefinition(
            'Boolean', 
            'or', 
            'Returns true if at least one input is true', 
            'or(var1...)',
            BooleanFunctionsFeature.func_or, 
            1, 
            None, 
            'boolean')
        calculator.funcs['counttrue'] = FunctionDefinition(
            'Boolean', 
            'counttrue', 
            'Returns the number of inputs that are true',
            'counttrue(var1...)', 
            BooleanFunctionsFeature.func_counttrue, 
            1, 
            None, 
            'boolean')

    def func_and(self, vals, units, refs, flags):
        for val in vals:
            if not BooleansFeature.boolean(self, val):
                return OperationResult(False)
        return OperationResult(True)

    def func_or(self, vals, units, refs, flags):
        for val in vals:
            if BooleansFeature.boolean(self, val):
                return OperationResult(True)
        return OperationResult(False)

    def func_counttrue(self, vals, units, refs, flags):
        count = 0
        for val in vals:
            if BooleansFeature.boolean(self, val):
                count += 1
        return OperationResult(Decimal(count))
