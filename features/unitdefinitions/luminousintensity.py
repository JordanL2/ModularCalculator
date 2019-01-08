#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class LuminousIntensityUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.luminousintensity'

    def title():
        return 'Luminous Intensity Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + []

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('luminousintensity', 'Luminous Intensity')

        calculator.unit_normaliser.add_prefixed_unit('luminousintensity', UnitDefinitionCandela)


class UnitDefinitionCandela(UnitDefinition):

    namelist = ['candelas','candela']
    symbollist = ['cd']
    systems = ['si']
