#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class FrequencyUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.frequency'

    def title():
        return 'Frequency Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.time']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('frequency', 'Frequency',
            ['time', -1])

        calculator.unit_normaliser.add_prefixed_unit('frequency', UnitDefinitionHertz)


class UnitDefinitionHertz(UnitDefinition):

    namelist = ['hertz','hertz']
    symbollist = ['Hz']
    systems = ['si']
