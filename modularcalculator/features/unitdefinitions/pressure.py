#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class PressureUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.pressure'

    def title():
        return 'Pressure Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.distance', 'unitdefinitions.time', 'unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('pressure', 'Pressure', ['mass', 1, 'distance', -1, 'time', -2])
        
        calculator.unit_normaliser.add_prefixed_unit('pressure', UnitDefinitionPascal)

        calculator.unit_normaliser.add_unit('pressure', UnitDefinitionAtmosphere())
        calculator.unit_normaliser.add_unit('pressure', UnitDefinitionPSI())


class UnitDefinitionPascal(UnitDefinition):

    namelist = ['pascals','pascal']
    symbollist = ['Pa']
    systems = ['si']

class UnitDefinitionAtmosphere(UnitDefinition):

    namelist = ['atmospheres','atmosphere']
    symbollist = ['atm']
    unitscale = Decimal('101325')

class UnitDefinitionPSI(UnitDefinition):

    namelist = ['pound-force per square inch','pound-force per square inch']
    symbollist = ['psi']
    unitscale = Decimal('6894.757')
    systems = ['us', 'uk']
