#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class EnergyUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.energy'

    def title():
        return 'Energy Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.distance', 'unitdefinitions.time', 'unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('energy', 'Energy',
            ['mass', 1,
             'distance', 2,
             'time', -2])

        calculator.unit_normaliser.add_prefixed_unit('energy', UnitDefinitionJoule)


class UnitDefinitionJoule(UnitDefinition):

    namelist = ['joules','joule']
    symbollist = ['J']
    systems = ['si']
