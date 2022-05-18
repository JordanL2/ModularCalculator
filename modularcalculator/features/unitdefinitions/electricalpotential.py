#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class ElectricalPotentialUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.electricalpotential'

    def title():
        return 'Electrical Potential Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.electriccurrent', 'unitdefinitions.distance', 'unitdefinitions.time', 'unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('electricalpotential', 'Electrical Potential',
            ['mass', Number(1),
             'distance', Number(2),
             'time', Number(-3),
             'electriccurrent', Number(-1)])

        calculator.unit_normaliser.add_prefixed_unit('electricalpotential', UnitDefinitionVolt)


class UnitDefinitionVolt(UnitDefinition):

    namelist = ['volts','volt']
    symbollist = ['V']
    systems = ['si']
