#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class SolidAngleUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.solidangle'

    def title():
        return 'Solid Angle Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + []

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('solidangle', 'Solid Angle')

        calculator.unit_normaliser.add_unit('solidangle', UnitDefinitionSteradian())


class UnitDefinitionSteradian(UnitDefinition):

    namelist = ['steradians','steradian']
    symbollist = ['sr']
    systems = ['si']
