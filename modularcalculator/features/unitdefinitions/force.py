#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class ForceUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.force'

    def title():
        return 'Force Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.distance', 'unitdefinitions.time', 'unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('force', 'Force',
            ['mass', Number(1),
             'distance', Number(1),
             'time', Number(-2)])

        calculator.unit_normaliser.add_prefixed_unit('force', UnitDefinitionNewton)


class UnitDefinitionNewton(UnitDefinition):

    namelist = ['newtons','newton']
    symbollist = ['N']
    systems = ['si']
