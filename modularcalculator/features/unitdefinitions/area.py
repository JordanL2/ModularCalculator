#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class AreaUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.area'

    def title():
        return 'Area Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.distance']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('area', 'Area', ['distance', 2])

        calculator.unit_normaliser.add_unit('area', UnitDefinitionAcre())
        calculator.unit_normaliser.add_unit('area', UnitDefinitionHectare())


class UnitDefinitionAcre(UnitDefinition):

    namelist = ['acres','acre']
    symbollist = ['ac']
    unitscale = Number('4046.9')
    systems = ['us', 'uk']
    use_for_condense = False

class UnitDefinitionHectare(UnitDefinition):

    namelist = ['hectares','hectare']
    symbollist = ['ha']
    unitscale = Number('10000')
    systems = ['si']
    use_for_condense = False
