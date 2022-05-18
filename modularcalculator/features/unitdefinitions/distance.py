#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class DistanceUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.distance'

    def title():
        return 'Distance Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + []

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('distance', 'Distance')

        calculator.unit_normaliser.add_prefixed_unit('distance', UnitDefinitionMeter, None, Number('1000'))
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionMeter(('centi', 'c', Number('0.01'))))

        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightYear())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightWeek())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightDay())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightHour())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightMinute())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightSecond())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionAstronomicalUnit())
        calculator.unit_normaliser.add_prefixed_unit('distance', UnitDefinitionParsec, Number('1'))

        calculator.unit_normaliser.add_unit('distance', UnitDefinitionInch())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionFeet())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionYard())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionMile())

        calculator.unit_normaliser.add_unit('distance', UnitDefinitionNauticalMile())


class UnitDefinitionMeter(UnitDefinition):

    namelist = ['meters','meter','metres','metre']
    symbollist = ['m']
    systems = ['si']

class UnitDefinitionLightYear(UnitDefinition):

    namelist = ['lightyears','lightyear']
    unitscale = Number('9460730472580800')
    systems = ['asu']

class UnitDefinitionLightWeek(UnitDefinition):

    namelist = ['lightweeks','lightweek']
    unitscale = Number('181314478598400')
    systems = ['asu']
    use = False

class UnitDefinitionLightDay(UnitDefinition):

    namelist = ['lightdays','lightday']
    unitscale = Number('25902068371200')
    systems = ['asu']

class UnitDefinitionLightHour(UnitDefinition):

    namelist = ['lighthours','lighthour']
    unitscale = Number('1079252848800')
    systems = ['asu']

class UnitDefinitionLightMinute(UnitDefinition):

    namelist = ['lightminutes','lightminute']
    unitscale = Number('17987547480')
    systems = ['asu']

class UnitDefinitionLightSecond(UnitDefinition):

    namelist = ['lightseconds','lightsecond']
    unitscale = Number('299792458')
    systems = ['asu']

class UnitDefinitionAstronomicalUnit(UnitDefinition):

    namelist = ['astronomical units','astronomical unit']
    symbollist = ['au']
    unitscale = Number('149597870700')
    systems = ['asu']

class UnitDefinitionParsec(UnitDefinition):

    namelist = ['parsecs','parsec']
    symbollist = ['pc']
    unitscale = Number('30856775810000000')
    systems = ['asu']

class UnitDefinitionInch(UnitDefinition):

    namelist = ['inches','inch']
    symbollist = ['in']
    unitscale = Number('0.0254')
    systems = ['us', 'uk']

class UnitDefinitionFeet(UnitDefinition):

    namelist = ['feet','foot']
    symbollist = ['ft']
    unitscale = Number('0.3048')
    systems = ['us', 'uk']

class UnitDefinitionYard(UnitDefinition):

    namelist = ['yards','yard']
    symbollist = ['yd']
    unitscale = Number('0.9144')
    systems = ['us', 'uk']

class UnitDefinitionMile(UnitDefinition):

    namelist = ['miles','mile']
    symbollist = ['mi']
    unitscale = Number('1609.344')
    systems = ['us', 'uk']

class UnitDefinitionNauticalMile(UnitDefinition):

    namelist = ['nautical miles','nautical mile']
    symbollist = ['nmi']
    unitscale = Number('1852')
    systems = ['nautical']
