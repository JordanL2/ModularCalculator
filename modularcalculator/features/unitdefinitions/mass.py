#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class MassUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.mass'

    def title():
        return 'Mass Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + []

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('mass', 'Mass')

        calculator.unit_normaliser.add_prefixed_unit('mass', UnitDefinitionGram, None, Number('1000'))
        calculator.unit_normaliser.add_prefixed_unit('mass', UnitDefinitionTonne, Number('1'))

        calculator.unit_normaliser.add_unit('mass', UnitDefinitionGrain())
        calculator.unit_normaliser.add_unit('mass', UnitDefinitionOunce())
        calculator.unit_normaliser.add_unit('mass', UnitDefinitionPound())
        calculator.unit_normaliser.add_unit('mass', UnitDefinitionStone())
        calculator.unit_normaliser.add_unit('mass', UnitDefinitionShortTon())
        calculator.unit_normaliser.add_unit('mass', UnitDefinitionLongTon())

        calculator.unit_normaliser.add_ambiguous_unit(AmbiguousUnitDefinitionTon(), ['short ton', 'long ton'])


class UnitDefinitionGram(UnitDefinition):

    namelist = ['grams','gram']
    symbollist = ['g']
    unitscale = Number('0.001')
    systems = ['si']

class UnitDefinitionTonne(UnitDefinition):

    namelist = ['tonnes','tonne']
    unitscale = Number('1000')
    systems = ['si']

class UnitDefinitionGrain(UnitDefinition):

    namelist = ['grains','grain']
    symbollist = ['gr']
    unitscale = Number('0.00006479891')
    systems = ['us', 'uk']

class UnitDefinitionOunce(UnitDefinition):

    namelist = ['ounces','ounce']
    symbollist = ['oz']
    unitscale = Number('0.028349523125')
    systems = ['us', 'uk']

class UnitDefinitionPound(UnitDefinition):

    namelist = ['pounds','pound']
    symbollist = ['lb']
    unitscale = Number('0.45359237')
    systems = ['us', 'uk']

class UnitDefinitionStone(UnitDefinition):

    namelist = ['stone','stone']
    symbollist = ['st']
    unitscale = Number('6.35029318')
    systems = ['uk']

class AmbiguousUnitDefinitionTon(AmbiguousUnitDefinition):

    namelist = ['tons','ton']

class UnitDefinitionShortTon(UnitDefinition):

    namelist = ['short tons','short ton']
    unitscale = Number('907.18474')
    systems = ['us']

class UnitDefinitionLongTon(UnitDefinition):

    namelist = ['long tons','long ton']
    unitscale = Number('1016.0469088')
    systems = ['uk']
