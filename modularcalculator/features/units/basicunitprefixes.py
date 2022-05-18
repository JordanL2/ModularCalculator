#!/usr/bin/python3

from modularcalculator.features.feature import Feature
from modularcalculator.objects.number import *


class BasicUnitPrefixesFeature(Feature):

    def id():
        return 'units.basicunitprefixes'

    def category():
        return 'Units'

    def title():
        return 'Basic Unit Prefixes'

    def desc():
        return 'Standard unit prefixes from micro to mega.'

    def dependencies():
        return ['units.units']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.prefixes.extend([
            ('micro', 'µ', Number('0.000001')),
            ('milli', 'm', Number('0.001')),
            ('kilo',  'k', Number('1000')),
            ('mega',  'M', Number('1000000')),
        ])
