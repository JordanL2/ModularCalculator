#!/usr/bin/python3

from modularcalculator.features.feature import Feature

from datetime import *


datestr = 'Date Format - Date'
datetimestr = 'Date Format - Date and time'
datetimehiresstr = 'Date Format - Date and time (incl. microseconds)'


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

    @classmethod
    def install(cls, calculator):
        calculator.validators['date'] = DatesFeature.validate_date

        calculator.feature_options['dates.dates'] = {
            datestr:          {'Format': '%Y-%m-%d', 'Padding': '0>10'},
            datetimestr:      {'Format': '%Y-%m-%dT%H:%M:%S', 'Padding': '0>19'},
            datetimehiresstr: {'Format': '%Y-%m-%dT%H:%M:%S.%f', 'Padding': '0>26'}
        }

    def string_to_date(self, val):
        try:
            return datetime.strptime(val, self.feature_options['dates.dates'][datetimehiresstr]['Format'])
        except ValueError:
            try:
                return datetime.strptime(val, self.feature_options['dates.dates'][datetimestr]['Format'])
            except ValueError:
                return datetime.strptime(val, self.feature_options['dates.dates'][datestr]['Format'])

    def date_to_string(self, dt):
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
            return format(
                dt.strftime(self.feature_options['dates.dates'][datestr]['Format']), 
                self.feature_options['dates.dates'][datestr]['Padding'])
        if dt.microsecond == 0:
            return format(
                dt.strftime(self.feature_options['dates.dates'][datetimestr]['Format']), 
                self.feature_options['dates.dates'][datetimestr]['Padding'])
        return format(
            dt.strftime(self.feature_options['dates.dates'][datetimehiresstr]['Format']), 
            self.feature_options['dates.dates'][datetimehiresstr]['Padding'])

    def validate_date(self, value, unit, ref):
        try:
            DatesFeature.string_to_date(self, value)
            return True
        except Exception:
            return False
