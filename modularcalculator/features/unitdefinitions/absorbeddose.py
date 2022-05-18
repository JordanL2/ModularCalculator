#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class AbsorbedDoseUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.absorbeddose'

    def title():
        return 'Absorbed Dose Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.distance', 'unitdefinitions.time']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('absorbeddose', 'Absorbed Dose',
            ['distance', 2,
             'time', -2])

        calculator.unit_normaliser.add_prefixed_unit('absorbeddose', UnitDefinitionGray)


class UnitDefinitionGray(UnitDefinition):

    namelist = ['grays','gray']
    symbollist = ['Gy']
    systems = ['si']
    use_for_condense = False
