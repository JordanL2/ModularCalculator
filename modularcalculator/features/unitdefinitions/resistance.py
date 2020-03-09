#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class ResistanceUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.resistance'

    def title():
        return 'Resistance Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.electriccurrent', 'unitdefinitions.distance', 'unitdefinitions.time', 'unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('resistance', 'Resistance', ['mass', 1, 'distance', 2, 'time', -3, 'electriccurrent', -2])
    	
        calculator.unit_normaliser.add_prefixed_unit('resistance', UnitDefinitionOhm)


class UnitDefinitionOhm(UnitDefinition):

    namelist = ['ohms','ohm']
    symbollist = ['Ω']
    systems = ['si']
