#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class PressureUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.pressure'

    def title():
        return 'Pressure Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.distance', 'unitdefinitions.time', 'unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('pressure', 'Pressure', ['mass', 1, 'distance', -1, 'time', -2])
        
        calculator.unit_normaliser.add_prefixed_unit('pressure', UnitDefinitionPascal)


class UnitDefinitionPascal(UnitDefinition):

    namelist = ['pascals','pascal']
    symbollist = ['Pa']
    systems = ['si']
