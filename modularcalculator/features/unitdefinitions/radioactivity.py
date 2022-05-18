#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class RadioactivityUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.radioactivity'

    def title():
        return 'Radioactivity Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.time']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('radioactivity', 'Radioactivity',
            ['time', -1])

        calculator.unit_normaliser.add_prefixed_unit('radioactivity', UnitDefinitionBecquerel)


class UnitDefinitionBecquerel(UnitDefinition):

    namelist = ['becquerels','becquerel']
    symbollist = ['Bq']
    systems = ['si']
    use_for_condense = False
