#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.features.structure.functions import FunctionDefinition
from modularcalculator.features.dates.dates import DatesFeature
from modularcalculator.objects.operators import OperationResult
from modularcalculator.features.feature import Feature

from decimal import *
from datetime import *


datestr = 'Date Format Human Readable - Date'
datetimestr = 'Date Format Human Readable - Date and time'
datetimehiresstr = 'Date Format Human Readable - Date and time (incl. microseconds)'


class DateFunctionsFeature(Feature):

    def id():
        return 'dates.datefunctions'

    def category():
        return 'Date'

    def title():
        return 'Date Functions'

    def desc():
        return 'Functions to create and manipulate dates'

    def dependencies():
        return ['dates.dates']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['datecreate'] =  FunctionDefinition(
            'Date', 
            'datecreate', 
            'Create a date',
            ['year', 'month', 'day', '[hour', 'minute', 'second', '[microsecond]]'],
            DateFunctionsFeature.func_datecreate, 
            3, 
            7, 
            'number')
        calculator.funcs['datecreate'].units_normalise = False

        calculator.funcs['dateformat'] =  FunctionDefinition(
            'Date', 
            'dateformat', 
            'Nicely format a date for easy reading',
            ['date'],
            DateFunctionsFeature.func_dateformat, 
            1, 
            1, 
            'date')
        calculator.funcs['dateformat'].units_normalise = False
        
        calculator.funcs['dateadd'] =  FunctionDefinition(
            'Date', 
            'dateadd', 
            'Add a time period to a date',
            ['date', 'time'],
            DateFunctionsFeature.func_dateadd, 
            2, 
            2)
        calculator.funcs['dateadd'].add_value_restriction(0, 0, 'date')
        calculator.funcs['dateadd'].add_value_restriction(1, 1, 'number')
        calculator.funcs['dateadd'].add_unit_restriction(1, 1, ['time', 1])
        calculator.funcs['dateadd'].units_normalise = False
        
        calculator.funcs['datesubtract'] =  FunctionDefinition(
            'Date', 
            'datesubtract', 
            'Subtract a time period from a date',
            ['date', 'time'],
            DateFunctionsFeature.func_datesubtract, 
            2, 
            2)
        calculator.funcs['datesubtract'].add_value_restriction(0, 0, 'date')
        calculator.funcs['datesubtract'].add_value_restriction(1, 1, 'number')
        calculator.funcs['datesubtract'].add_unit_restriction(1, 1, ['time', 1])
        calculator.funcs['datesubtract'].units_normalise = False
        
        calculator.funcs['datedifference'] =  FunctionDefinition(
            'Date', 
            'datedifference', 
            'Determine the length of time between two dates',
            ['date1', 'date2'],
            DateFunctionsFeature.func_datedifference, 
            3, 
            3)
        calculator.funcs['datedifference'].add_value_restriction(0, 1, 'date')
        calculator.funcs['datedifference'].add_value_restriction(2, 2, 'unit')
        
        calculator.funcs['now'] =  FunctionDefinition(
            'Date', 
            'now', 
            'Return the current date and time',
            [],
            DateFunctionsFeature.func_now, 
            0, 
            0)

        calculator.feature_options['dates.dates'][datestr] =          {'Format': '%A, %d-%b-%Y', 'Padding': ''}
        calculator.feature_options['dates.dates'][datetimestr] =      {'Format': '%A, %d-%b-%Y at %H:%M:%S', 'Padding': ''}
        calculator.feature_options['dates.dates'][datetimehiresstr] = {'Format': '%A, %d-%b-%Y at %H:%M:%S.%f', 'Padding': ''}

    def func_datecreate(self, vals, units, refs, flags):
        return OperationResult(DatesFeature.date_to_string(self, datetime(*vals)))

    def func_dateformat(self, vals, units, refs, flags):
        dt = DatesFeature.string_to_date(self, vals[0])
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
            return OperationResult(format(
                dt.strftime(self.feature_options['dates.dates'][datestr]['Format']), 
                self.feature_options['dates.dates'][datestr]['Padding']))
        if dt.microsecond == 0:
            return OperationResult(format(
                dt.strftime(self.feature_options['dates.dates'][datetimestr]['Format']), 
                self.feature_options['dates.dates'][datetimestr]['Padding']))
        return OperationResult(format(
            dt.strftime(self.feature_options['dates.dates'][datetimehiresstr]['Format']), 
            self.feature_options['dates.dates'][datetimehiresstr]['Padding']))

    def func_dateadd(self, vals, units, refs, flags):
        dt = DatesFeature.string_to_date(self, vals[0])

        num, fromunit = vals[1], units[1]
        tounit = self.unit_normaliser.get_unit('seconds')
        seconds, tounit = self.unit_normaliser.unit_conversion(num, fromunit, tounit, False)
        td = timedelta(seconds=float(seconds))

        dt += td

        res = OperationResult(DatesFeature.date_to_string(self, dt))
        res.set_unit(None)
        return res

    def func_datesubtract(self, vals, units, refs, flags):
        return DateFunctionsFeature.func_dateadd(self, [vals[0], -(vals[1])], units, refs, flags)

    def func_datedifference(self, vals, units, refs, flags):
        td = abs(DatesFeature.string_to_date(self, vals[0]) - DatesFeature.string_to_date(self, vals[1]))

        seconds = Decimal(td.total_seconds())
        seconds = round(seconds, min(6, getcontext().prec))
        fromunit = self.unit_normaliser.get_unit('seconds')
        tounit = vals[2]
        value, tounit = self.unit_normaliser.unit_conversion(seconds, fromunit, tounit, False)

        res = OperationResult(value)
        res.set_unit(tounit)
        return res

    def func_now(self, vals, units, refs, flags):
        return OperationResult(DatesFeature.date_to_string(self, datetime.now()))
