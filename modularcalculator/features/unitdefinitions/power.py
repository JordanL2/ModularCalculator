#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class PowerUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.power'

    def title():
        return 'Power Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.distance', 'unitdefinitions.time', 'unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('power', 'Power', ['mass', 1, 'distance', 2, 'time', -3])
        
        calculator.unit_normaliser.add_prefixed_unit('power', UnitDefinitionWatt)


class UnitDefinitionWatt(UnitDefinition):

    namelist = ['watts','watt']
    symbollist = ['W']
    systems = ['si']
