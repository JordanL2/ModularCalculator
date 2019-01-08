#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class AccelerationUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.acceleration'

    def title():
        return 'Acceleration Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.distance','unitdefinitions.time']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('acceleration', 'Acceleration', ['distance', 1, 'time', -2])
        
        calculator.unit_normaliser.add_unit('acceleration', UnitDefinitionGee())

        calculator.unit_normaliser.add_multiunit('acceleration', ['meter', 1, 'second', -2])


class UnitDefinitionGee(UnitDefinition):

    namelist = ['gees','gee']
    symbollist = ['gee']
    unitscale = Decimal('9.80665')
    systems = []
    use_for_condense = False
