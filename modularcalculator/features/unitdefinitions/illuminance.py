#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class IlluminanceUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.illuminance'

    def title():
        return 'Illuminance Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.luminousintensity', 'unitdefinitions.solidangle', 'unitdefinitions.distance']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('illuminance', 'Illuminance',
            ['luminousintensity', Number(1),
             'solidangle', Number(1),
             'distance', Number(-2)])

        calculator.unit_normaliser.add_prefixed_unit('illuminance', UnitDefinitionLux)


class UnitDefinitionLux(UnitDefinition):

    namelist = ['lux','lux']
    symbollist = ['lx']
    systems = ['si']
