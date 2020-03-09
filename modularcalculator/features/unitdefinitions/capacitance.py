#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class CapacitanceUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.capacitance'

    def title():
        return 'Capacitance Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.electriccurrent','unitdefinitions.distance','unitdefinitions.time','unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('capacitance', 'Capacitance', ['electriccurrent', 2, 'time', 4, 'mass', -1, 'distance', -2])
    	
        calculator.unit_normaliser.add_prefixed_unit('capacitance', UnitDefinitionFarad)


class UnitDefinitionFarad(UnitDefinition):

    namelist = ['farads','farad']
    symbollist = ['F']
    systems = ['si']
