#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class ElectricCurrentUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.electriccurrent'

    def title():
        return 'Electric Current Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + []

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('electriccurrent', 'Electric Current')
    	
        calculator.unit_normaliser.add_prefixed_unit('electriccurrent', UnitDefinitionAmpere)


class UnitDefinitionAmpere(UnitDefinition):

    namelist = ['amperes','ampere']
    symbollist = ['A']
    systems = ['si']
