#!/usr/bin/python3

from modularcalculator.features.feature import Feature

from datetime import *


date_format = 'Date Format'
date_padding = 'Date Padding'
datetime_format = 'Date + Time Format'
datetime_padding = 'Date + Time Padding'
datetimehires_format = 'Date + Hi Res Time Format'
datetimehires_padding = 'Date + Hi Res Time Padding'


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
        }

    @classmethod
    def install(cls, calculator):
        calculator.validators['date'] = DatesFeature.validate_date

        calculator.feature_options['dates.dates'] = cls.default_options()

    def string_to_date(self, val):
        try:
            return datetime.strptime(val, self.feature_options['dates.dates'][datetimehires_format])
        except ValueError:
            try:
                return datetime.strptime(val, self.feature_options['dates.dates'][datetime_format])
            except ValueError:
                return datetime.strptime(val, self.feature_options['dates.dates'][date_format])

    def date_to_string(self, dt):
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
            return format(
                dt.strftime(self.feature_options['dates.dates'][date_format]), 
                self.feature_options['dates.dates'][date_padding])
        if dt.microsecond == 0:
            return format(
                dt.strftime(self.feature_options['dates.dates'][datetime_format]), 
                self.feature_options['dates.dates'][datetime_padding])
        return format(
            dt.strftime(self.feature_options['dates.dates'][datetimehires_format]), 
            self.feature_options['dates.dates'][datetimehires_padding])

    def validate_date(self, value, unit, ref):
        try:
            DatesFeature.string_to_date(self, value)
            return True
        except Exception:
            return False
