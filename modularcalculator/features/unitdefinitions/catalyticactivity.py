#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class CatalyticActivityUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.catalyticactivity'

    def title():
        return 'Catalytic Activity Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.substance', 'unitdefinitions.time']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('catalyticactivity', 'Catalytic Activity',
            ['substance', Number(1),
             'time', Number(-1)])

        calculator.unit_normaliser.add_prefixed_unit('catalyticactivity', UnitDefinitionKatal)


class UnitDefinitionKatal(UnitDefinition):

    namelist = ['katals','katal']
    symbollist = ['kat']
    systems = ['si']
