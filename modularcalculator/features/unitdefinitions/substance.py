#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class SubstanceUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.substance'

    def title():
        return 'Substance Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + []

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('substance', 'Substance')

        calculator.unit_normaliser.add_prefixed_unit('substance', UnitDefinitionMole)


class UnitDefinitionMole(UnitDefinition):

    namelist = ['moles','mole']
    symbollist = ['mol']
    systems = ['si']
