#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *

from decimal import *


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
        
        calculator.unit_normaliser.add_prefixed_unit('distance', UnitDefinitionMeter, None, Decimal('1000'))
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionMeter(('centi', 'c', Decimal('0.01'))))

        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightYear())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightWeek())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightDay())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightHour())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightMinute())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionLightSecond())
        calculator.unit_normaliser.add_unit('distance', UnitDefinitionAstronomicalUnit())
        calculator.unit_normaliser.add_prefixed_unit('distance', UnitDefinitionParsec, Decimal('1'))
        
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
    symbollist = ['lightyear']
    unitscale = Decimal('9460730472580800')
    systems = ['asu']

class UnitDefinitionLightWeek(UnitDefinition):

    namelist = ['lightweeks','lightweek']
    symbollist = ['lightweek']
    unitscale = Decimal('181314478598400')
    systems = ['asu']
    use = False

class UnitDefinitionLightDay(UnitDefinition):

    namelist = ['lightdays','lightday']
    symbollist = ['lightday']
    unitscale = Decimal('25902068371200')
    systems = ['asu']

class UnitDefinitionLightHour(UnitDefinition):

    namelist = ['lighthours','lighthour']
    symbollist = ['lighthour']
    unitscale = Decimal('1079252848800')
    systems = ['asu']

class UnitDefinitionLightMinute(UnitDefinition):

    namelist = ['lightminutes','lightminute']
    symbollist = ['lightminute']
    unitscale = Decimal('17987547480')
    systems = ['asu']

class UnitDefinitionLightSecond(UnitDefinition):

    namelist = ['lightseconds','lightsecond']
    symbollist = ['lightsecond']
    unitscale = Decimal('299792458')
    systems = ['asu']

class UnitDefinitionAstronomicalUnit(UnitDefinition):

    namelist = ['astronomical units','astronomical unit']
    symbollist = ['au']
    unitscale = Decimal('149597870700')
    systems = ['asu']

class UnitDefinitionParsec(UnitDefinition):

    namelist = ['parsecs','parsec']
    symbollist = ['pc']
    unitscale = Decimal('30856775810000000')
    systems = ['asu']

class UnitDefinitionInch(UnitDefinition):

    namelist = ['inches','inch']
    symbollist = ['in']
    unitscale = Decimal('0.0254')
    systems = ['us', 'uk']

class UnitDefinitionFeet(UnitDefinition):

    namelist = ['feet','foot']
    symbollist = ['ft']
    unitscale = Decimal('0.3048')
    systems = ['us', 'uk']

class UnitDefinitionYard(UnitDefinition):

    namelist = ['yards','yard']
    symbollist = ['yd']
    unitscale = Decimal('0.9144')
    systems = ['us', 'uk']

class UnitDefinitionMile(UnitDefinition):

    namelist = ['miles','mile']
    symbollist = ['mi']
    unitscale = Decimal('1609.344')
    systems = ['us', 'uk']

class UnitDefinitionNauticalMile(UnitDefinition):

    namelist = ['nautical miles','nautical mile']
    symbollist = ['nmi']
    unitscale = Decimal('1852')
    systems = ['nautical']
