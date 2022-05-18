#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class InductanceUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.inductance'

    def title():
        return 'Inductance Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.electriccurrent', 'unitdefinitions.distance', 'unitdefinitions.time', 'unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('inductance', 'Inductance',
            ['mass', Number(1),
             'distance', Number(2),
             'time', Number(-2),
             'electriccurrent', Number(-2)])

        calculator.unit_normaliser.add_prefixed_unit('inductance', UnitDefinitionHenry)


class UnitDefinitionHenry(UnitDefinition):

    namelist = ['henries','henry']
    symbollist = ['H']
    systems = ['si']
