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

    def convert(self, num, power, relative):
        if relative:
            return num
        if power.to_decimal() == -1:
            return num + Number('273.15')
        if power.to_decimal() == 1:
            return num - Number('273.15')
        raise Exception("Can't perform absolute conversion with a power other than 1")


class UnitDefinitionFahrenheit(UnitDefinition):

    namelist = ['Fahrenheit','Fahrenheit','deg F']
    symbollist = ['°F']
    systems = ['us', 'uk']

    def convert(self, num, power, relative):
        if relative:
            return num / (Number(5, 9) ** power)
        if power.to_decimal() == -1:
            return (num + Number('459.67')) * Number(5, 9)
        if power.to_decimal() == 1:
            return (num * Number(9, 5)) - Number('459.67')
        raise Exception("Can't perform absolute conversion with a power other than 1")
