#!/usr/bin/python3

from modularcalculator.objects.units import *
from modularcalculator.objects.exceptions import *
from modularcalculator.features.structure.functions import FunctionDefinition
from modularcalculator.features.dates.dates import DatesFeature
from modularcalculator.objects.number import *
from modularcalculator.objects.operators import OperationResult
from modularcalculator.features.feature import Feature

from datetime import *


date_format = 'Human Readable Date Format'
date_padding = 'Human Readable Date Padding'
datetime_format = 'Human Readable Date + Time Format'
datetime_padding = 'Human Readable Date + Time Padding'
datetimehires_format = 'Human Readable Date + Hi Res Time Format'
datetimehires_padding = 'Human Readable Date + Hi Res Time Padding'
datetz_format = 'Human Readable Date + Timezone Format'
datetz_padding = 'Human Readable Date + Timezone Padding'
datetimetz_format = 'Human Readable Date + Time + Timezone Format'
datetimetz_padding = 'Human Readable Date + Time + Timezone Padding'
datetimehirestz_format = 'Human Readable Date + Hi Res Time + Timezone Format'
datetimehirestz_padding = 'Human Readable Date + Hi Res Time + Timezone Padding'


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
        return ['dates.dates','structure.functions']

    def default_options():
        return {
            date_format: '%A, %d-%b-%Y',
            date_padding: '',
            datetime_format: '%A, %d-%b-%Y at %H:%M:%S',
            datetime_padding: '',
            datetimehires_format: '%A, %d-%b-%Y at %H:%M:%S.%f',
            datetimehires_padding: '',
            datetz_format: '%A, %d-%b-%Y (%z)',
            datetz_padding: '',
            datetimetz_format: '%A, %d-%b-%Y at %H:%M:%S (%z)',
            datetimetz_padding: '',
            datetimehirestz_format: '%A, %d-%b-%Y at %H:%M:%S.%f (%z)',
            datetimehirestz_padding: '',
        }

    @classmethod
    def install(cls, calculator):
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
            'Determine the length of time between two dates, return answer in the given unit',
            ['date1', 'date2', '[unit]'],
            DateFunctionsFeature.func_datedifference,
            2,
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

        calculator.feature_options['dates.datefunctions'] = cls.default_options()

    def func_dateformat(self, vals, units, refs, flags):
        dt = DatesFeature.string_to_date(self, vals[0])
        dt_format, dt_padding = DatesFeature.correct_format_for_date(self, dt)
        return OperationResult(format(
            dt.strftime(self.feature_options['dates.datefunctions']['Human Readable ' + dt_format]),
            self.feature_options['dates.datefunctions']['Human Readable ' + dt_padding]))

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
        date1 = DatesFeature.string_to_date(self, vals[0])
        date2 = DatesFeature.string_to_date(self, vals[1])
        if ((date1.utcoffset() is None) != (date2.utcoffset() is None)):
            raise CalculatorException("Cannot compare dates with timezones and dates without timezones")
        td = abs(date1 - date2)

        seconds = Number(str(td.total_seconds()))
        seconds = round(seconds, min(6, getcontext().prec))
        fromunit = UnitPowerList.new([self.unit_normaliser.get_unit('seconds'), 1])
        tounit = UnitPowerList.new([self.unit_normaliser.get_unit('seconds'), 1])
        value = seconds
        if len(vals) >= 3:
            tounit = vals[2]
            value, tounit = self.unit_normaliser.unit_conversion(seconds, fromunit, tounit, False)

        res = OperationResult(value)
        res.set_unit(tounit)
        return res

    def func_now(self, vals, units, refs, flags):
        return OperationResult(DatesFeature.date_to_string(self, datetime.now()))
