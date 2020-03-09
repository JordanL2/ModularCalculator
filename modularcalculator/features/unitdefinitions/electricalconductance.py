#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class ElectricalConductanceUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.electricalconductance'

    def title():
        return 'Electrical Conductance Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.electriccurrent', 'unitdefinitions.distance', 'unitdefinitions.time', 'unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('electricalconductance', 'Electrical Conductance', ['time', 3, 'electriccurrent', 2, 'mass', -1, 'distance', -2])
    	
        calculator.unit_normaliser.add_prefixed_unit('electricalconductance', UnitDefinitionSiemens)


class UnitDefinitionSiemens(UnitDefinition):

    namelist = ['siemens','siemens']
    symbollist = ['S']
    systems = ['si']
