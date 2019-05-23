#!/usr/bin/python3

from modularcalculator.features.feature import Feature
from modularcalculator.objects.items import *


class UnitSystemsFeature(Feature):

    def id():
        return 'units.systems'

    def category():
        return 'Units'

    def title():
        return 'Unit Systems'

    def desc():
        return 'Systems of measurements, eg: SI, Imperial, US Customary'

    def dependencies():
        return ['units.units']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.systems['gregorian'] = UnitSystemGregorian()
        calculator.unit_normaliser.systems['si'] = UnitSystemSI()
        calculator.unit_normaliser.systems['us'] = UnitSystemUS()
        calculator.unit_normaliser.systems['uk'] = UnitSystemUK()
        calculator.unit_normaliser.systems['asu'] = UnitSystemASU()
        calculator.unit_normaliser.systems['nautical'] = UnitSystemNautical()
        calculator.unit_normaliser.systems['iec'] = UnitSystemIEC()

        calculator.unit_normaliser.systems_preference.extend(['gregorian', 'si', 'us', 'uk', 'asu', 'nautical', 'iec'])

        calculator.add_parser('unitsystems', UnitSystemsFeature.parse_unitsystems)

        calculator.validators['unitsystem'] = UnitSystemsFeature.validate_unit_system

    def parse_unitsystems(self, expr, i, items, flags):
        next = expr[i:]
        
        for system in self.unit_normaliser.systems.keys():
            if next.startswith(system) and (len(next) == len(system) or not next[len(system)].isalpha()):
                return [UnitSystemItem(system)], len(system), None
            
        return None, None, None

    def validate_unit_system(self, value, unit, ref):
        return value in self.unit_normaliser.systems.keys()


class UnitSystemItem(OperandItem):

    def __init__(self, text):
        super().__init__(text)

    def desc(self):
        return 'unitsystem'

    def value(self, flags):
        return self.text

    def result(self, flags):
        return OperandResult(self.value(flags), None, self)


class UnitSystemGregorian:

    name = 'Gregorian'

class UnitSystemSI:

    name = 'International System of Units'

class UnitSystemUS:

    name = 'US Customary'

class UnitSystemUK:

    name = 'British Imperial'

class UnitSystemASU:

    name = 'Astronomical System of Units'

class UnitSystemNautical:

    name = 'Nautical'

class UnitSystemIEC:

    name = 'ISO/IEC 80000'
