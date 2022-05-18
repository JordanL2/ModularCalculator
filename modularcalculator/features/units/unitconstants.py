#!/usr/bin/python3

from modularcalculator.features.feature import Feature
from modularcalculator.objects.number import *


class UnitConstantsFeature(Feature):

    def id():
        return 'units.unitconstants'

    def category():
        return 'Units'

    def title():
        return 'Unit Constants'

    def desc():
        return 'Constants with a unit'

    def dependencies():
        return ['units.units', 'numerical.numericalconstants', 'units.basicunitprefixes', 'unitdefinitions.distance', 'unitdefinitions.mass', 'unitdefinitions.time', 'unitdefinitions.energy']

    @classmethod
    def install(cls, calculator):
        calculator.constants['G'] = (Number('0.0000000000667408'), calculator.unit_normaliser.make_multiunit(
            ['meter', Number(3),
             'kilogram', Number(-1),
             'second', Number(-2)]))

        calculator.constants['earthgravity'] = (Number('9.80665'), calculator.unit_normaliser.make_multiunit(
            ['meter', Number(1),
             'second', Number(-2)]))

        calculator.constants['speedoflight'] = (Number('299792458'), calculator.unit_normaliser.make_multiunit(
            ['meter', Number(1),
             'second', Number(-1)]))

        calculator.constants['Planck'] = (Number('0.000000000000000000000000000000000662607015'), calculator.unit_normaliser.make_multiunit(
            ['joule', Number(1),
             'second', Number(1)]))
