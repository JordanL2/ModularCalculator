#!/usr/bin/python3

from modularcalculator.features.feature import Feature
from modularcalculator.objects.number import *


class AdvancedUnitPrefixesFeature(Feature):

    def id():
        return 'units.advancedunitprefixes'

    def category():
        return 'Units'

    def title():
        return 'Advanced Unit Prefixes'

    def desc():
        return 'Advanced unit prefixes from atto to exa.'

    def dependencies():
        return ['units.units', 'units.basicunitprefixes']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.prefixes.extend([
            ('atto',  'a', Number('0.000000000000000001')),
            ('femto', 'f', Number('0.000000000000001')),
            ('pico',  'p', Number('0.000000000001')),
            ('nano',  'n', Number('0.000000001')),
            ('giga',  'G', Number('1000000000')),
            ('tera',  'T', Number('1000000000000')),
            ('peta',  'P', Number('1000000000000000')),
            ('exa',   'E', Number('1000000000000000000')),
        ])
