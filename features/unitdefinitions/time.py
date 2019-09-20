#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *

from decimal import *


class TimeUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.time'

    def title():
        return 'Time Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + []

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('time', 'Time')

        calculator.unit_normaliser.add_prefixed_unit('time', UnitDefinitionSecond, None, Decimal('1'))
        for unit in [
                UnitDefinitionMinute(),
                UnitDefinitionHour(),
                UnitDefinitionDay(),
                UnitDefinitionWeek(),
                UnitDefinitionMonth(),
                UnitDefinitionYear(),
            ]:
            calculator.unit_normaliser.add_unit('time', unit)


class UnitDefinitionSecond(UnitDefinition):

    namelist = ['seconds','second']
    symbollist = ['s']
    systems = ['si', 'gregorian']

class UnitDefinitionMinute(UnitDefinition):

    namelist = ['minutes','minute']
    unitscale = Decimal('60')
    systems = ['gregorian']

class UnitDefinitionHour(UnitDefinition):

    namelist = ['hours','hour']
    symbollist = ['h']
    unitscale = Decimal('3600')
    systems = ['gregorian']
    relevant_to_systems = ['us', 'uk', 'nautical']

class UnitDefinitionDay(UnitDefinition):

    namelist = ['days','day']
    unitscale = Decimal('86400')
    systems = ['gregorian']

class UnitDefinitionWeek(UnitDefinition):

    namelist = ['weeks','week']
    unitscale = Decimal('604800')
    systems = ['gregorian']
    use = False

class UnitDefinitionMonth(UnitDefinition):

    namelist = ['months','month']
    unitscale = Decimal('2629746')
    systems = ['gregorian']

class UnitDefinitionYear(UnitDefinition):

    namelist = ['years','year']
    symbollist = ['yr']
    unitscale = Decimal('31556952')
    systems = ['gregorian']
