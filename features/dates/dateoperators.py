#!/usr/bin/python3

from modularcalculator.features.dates.datefunctions import DateFunctionsFeature
from modularcalculator.objects.operators import OperatorDefinition
from modularcalculator.features.feature import Feature


class DateOperatorsFeature(Feature):

    def id():
        return 'dates.dateoperators'

    def category():
        return 'Date'

    def title():
        return 'Date Operators'

    def desc():
        return 'Operators to easily add/subtract time periods to dates'

    def dependencies():
        return ['dates.dates','structure.operators']

    @classmethod
    def install(cls, calculator):
        date_add_op = OperatorDefinition(
            'Date', 
            '+%', 
            'Add a time period to a date',
            DateOperatorsFeature.op_date_add, 
            1, 
            1, 
            ['date', 'number'])
        date_add_op.add_unit_restriction(1, 1, ['time', 1])
        calculator.add_op(date_add_op, {'units_normalise': False})

        date_sub_op = OperatorDefinition(
            'Date', 
            '-%', 
            'Subtract a time period from a date',
            DateOperatorsFeature.op_date_subtract, 
            1, 
            1, 
            ['date', 'number'])
        date_sub_op.add_unit_restriction(1, 1, ['time', 1])
        calculator.add_op(date_sub_op, {'units_normalise': False})

    def op_date_add(self, vals, units, refs, flags):
    	return DateFunctionsFeature.func_dateadd(self, [vals[0], vals[1]], units, refs, flags)

    def op_date_subtract(self, vals, units, refs, flags):
    	return DateFunctionsFeature.func_datesubtract(self, [vals[0], vals[1]], units, refs, flags)
