#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class EquivalentDoseUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.equivalentdose'

    def title():
        return 'Equivalent Dose Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.distance', 'unitdefinitions.time']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('equivalentdose', 'Equivalent Dose', ['distance', 2, 'time', -2])
        
        calculator.unit_normaliser.add_prefixed_unit('equivalentdose', UnitDefinitionSievert)


class UnitDefinitionSievert(UnitDefinition):

    namelist = ['sieverts','sievert']
    symbollist = ['Sv']
    systems = ['si']
    use_for_condense = False
