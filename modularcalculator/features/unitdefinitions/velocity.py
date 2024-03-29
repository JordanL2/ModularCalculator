#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class VelocityUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.velocity'

    def title():
        return 'Velocity Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.distance', 'unitdefinitions.time']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('velocity', 'Velocity',
            ['distance', 1,
             'time', -1])

        calculator.unit_normaliser.add_unit('velocity', UnitDefinitionKnot())

        calculator.unit_normaliser.add_multiunit('velocity',
            ['meter', Number(1),
             'second', Number(-1)])


class UnitDefinitionKnot(UnitDefinition):

    namelist = ['knots','knot']
    symbollist = ['kn','kt']
    unitscale = Number(1852, 3600)
    systems = ['nautical']
