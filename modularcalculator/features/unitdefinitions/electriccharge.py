#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class ElectricChargeUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.electriccharge'

    def title():
        return 'Electric Charge Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.electriccurrent', 'unitdefinitions.time']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('electriccharge', 'Electric Charge',
            ['electriccurrent', Number(1),
             'time', Number(1)])

        calculator.unit_normaliser.add_prefixed_unit('electriccharge', UnitDefinitionCoulomb)


class UnitDefinitionCoulomb(UnitDefinition):

    namelist = ['coulombs','coulomb']
    symbollist = ['C']
    systems = ['si']
