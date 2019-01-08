#!/usr/bin/python3

from modularcalculator.features.feature import Feature

from decimal import *


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
            ('atto',  'a', Decimal('0.000000000000000001')),
            ('femto', 'f', Decimal('0.000000000000001')),
            ('pico',  'p', Decimal('0.000000000001')),
            ('nano',  'n', Decimal('0.000000001')),
            ('giga',  'G', Decimal('1000000000')),
            ('tera',  'T', Decimal('1000000000000')),
            ('peta',  'P', Decimal('1000000000000000')),
            ('exa',   'E', Decimal('1000000000000000000')),
        ])
