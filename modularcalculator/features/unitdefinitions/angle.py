#!/usr/bin/python3

from modularcalculator.features.numerical.numericalconstants import NumericalConstantsFeature
from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class AngleUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.angle'

    def title():
        return 'Angle Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + []

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('angle', 'Angle')

        calculator.unit_normaliser.add_unit('angle', UnitDefinitionRadian())
        calculator.unit_normaliser.add_unit('angle', UnitDefinitionDegree())


class UnitDefinitionRadian(UnitDefinition):

    namelist = ['radians','radian']
    symbollist = ['rad']
    systems = ['si']

class UnitDefinitionDegree(UnitDefinition):

    namelist = ['degrees','degree']
    symbollist = ['°','deg']
    unitscale = Number(NumericalConstantsFeature.tau, 360)
    systems = ['si']
