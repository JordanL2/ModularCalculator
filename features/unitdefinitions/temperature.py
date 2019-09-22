#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class TemperatureUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.temperature'

    def title():
        return 'Temperature Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + []

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('temperature', 'Temperature')

        calculator.unit_normaliser.add_prefixed_unit('temperature', UnitDefinitionKelvin)
        for unit in [ 
                UnitDefinitionCelsius(), 
                UnitDefinitionFahrenheit(),
            ]:
            calculator.unit_normaliser.add_unit('temperature', unit)


class UnitDefinitionKelvin(UnitDefinition):

    namelist = ['kelvin','kelvin']
    symbollist = ['K']
    systems = ['si']


class UnitDefinitionCelsius(UnitDefinition):
    
    namelist = ['Celsius','Celsius','deg C']
    symbollist = ['°C']
    systems = ['si']

    def convertfrom(self, num, relative):
        if relative:
            return num
        return num + Decimal('273.15')

    def convertto(self, num, relative):
        if relative:
            return num
        return num - Decimal('273.15')


class UnitDefinitionFahrenheit(UnitDefinition):

    namelist = ['Fahrenheit','Fahrenheit','deg F']
    symbollist = ['°F']
    systems = ['us', 'uk']

    def convertfrom(self, num, relative):
        if relative:
            return num * Decimal('5') / Decimal('9')
        return (num + Decimal('459.67')) * Decimal('5') / Decimal('9')

    def convertto(self, num, relative):
        if relative:
            return num * Decimal('9') / Decimal('5')
        return (num * Decimal('9') / Decimal('5')) - Decimal('459.67')
