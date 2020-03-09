#!/usr/bin/python3

from modularcalculator.features.feature import Feature


class UnitSymbolsFeature(Feature):

    def id():
        return 'units.unitsymbols'

    def category():
        return 'Units'

    def title():
        return 'Unit Symbols'

    def desc():
        return 'Enables referring to units by one of their symbols rather than full name'

    def dependencies():
        return ['units.units']

    @classmethod
    def install(cls, calculator):
        calculator.unit_symbols_enabled = True

