#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class LuminousFluxUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.luminousflux'

    def title():
        return 'Luminous Flux Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.luminousintensity', 'unitdefinitions.solidangle']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('luminousflux', 'Luminous Flux',
            ['luminousintensity', 1,
             'solidangle', 1])

        calculator.unit_normaliser.add_prefixed_unit('luminousflux', UnitDefinitionLumen)


class UnitDefinitionLumen(UnitDefinition):

    namelist = ['lumens','lumen']
    symbollist = ['lm']
    systems = ['si']
