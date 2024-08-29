#!/usr/bin/python3

from modularcalculator.features.feature import Feature

from datetime import *


date_format = 'Date Format'
date_padding = 'Date Padding'
datetime_format = 'Date + Time Format'
datetime_padding = 'Date + Time Padding'
datetimehires_format = 'Date + Hi Res Time Format'
datetimehires_padding = 'Date + Hi Res Time Padding'
datetz_format = 'Date + Timezone Format'
datetz_padding = 'Date + Timezone Padding'
datetimetz_format = 'Date + Time + Timezone Format'
datetimetz_padding = 'Date + Time + Timezone Padding'
datetimehirestz_format = 'Date + Hi Res Time + Timezone Format'
datetimehirestz_padding = 'Date + Hi Res Time + Timezone Padding'

attempt_order = [datetimehirestz_format, datetimetz_format, datetz_format, datetimehires_format, datetime_format, date_format]


class DatesFeature(Feature):

    def id():
        return 'dates.dates'

    def category():
        return 'Date'

    def title():
        return 'Dates'

    def desc():
        return 'Date type'

    def dependencies():
        return ['strings.strings']

    def default_options():
        return {
            date_format: '%Y-%m-%d',
            date_padding: '0>10',
            datetime_format: '%Y-%m-%dT%H:%M:%S',
            datetime_padding: '0>19',
            datetimehires_format: '%Y-%m-%dT%H:%M:%S.%f',
            datetimehires_padding: '0>26',
            datetz_format: '%Y-%m-%d%z',
            datetz_padding: '0>15',
            datetimetz_format: '%Y-%m-%dT%H:%M:%S%z',
            datetimetz_padding: '0>24',
            datetimehirestz_format: '%Y-%m-%dT%H:%M:%S.%f%z',
            datetimehirestz_padding: '0>31',
        }

    @classmethod
    def install(cls, calculator):
        calculator.add_validator('date', 'date', DatesFeature.validate_date)

        calculator.feature_options['dates.dates'] = cls.default_options()

    def string_to_date(self, val):
        for attempt in attempt_order:
            try:
                return datetime.strptime(val, self.feature_options['dates.dates'][attempt])
            except ValueError:
                pass
        raise Exception("Can't parse date {0}".format(val))

    def correct_format_for_date(self, dt):
        dt_format = None
        dt_padding = None
        if dt.utcoffset() is None:
            if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
                dt_format = date_format
                dt_padding = date_padding
            elif dt.microsecond == 0:
                dt_format = datetime_format
                dt_padding = datetime_padding
            else:
                dt_format = datetimehires_format
                dt_padding = datetimehires_padding
        else:
            if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
                dt_format = datetz_format
                dt_padding = datetz_padding
            elif dt.microsecond == 0:
                dt_format = datetimetz_format
                dt_padding = datetimetz_padding
            else:
                dt_format = datetimehirestz_format
                dt_padding = datetimehirestz_padding
        return dt_format, dt_padding

    def date_to_string(self, dt):
        dt_format, dt_padding = DatesFeature.correct_format_for_date(self, dt)
        return format(
            dt.strftime(self.feature_options['dates.dates'][dt_format]),
            self.feature_options['dates.dates'][dt_padding])

    def validate_date(self, value, unit, ref):
        try:
            DatesFeature.string_to_date(self, value)
            return True
        except Exception:
            return False
