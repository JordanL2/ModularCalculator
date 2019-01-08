#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class DataUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.data'

    def title():
        return 'Data Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + []

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('data', 'Data')

        extended_si_prefixes = [
            ('zetta',  'Z', Decimal('1000000000000000000000')),
            ('yotta',  'Y', Decimal('1000000000000000000000000')),
        ]

        iec_prefixes = [
            ('kibi',  'ki', Decimal('1024')),
            ('mebi',  'Mi', Decimal('1048576')),
            ('gibi',  'Gi', Decimal('1073741824')),
            ('tebi',  'Ti', Decimal('1099511627776')),
            ('pebi',  'Pi', Decimal('1125899906842624')),
            ('exbi',  'Ei', Decimal('1152921504606846976')),
            ('zebi',  'Zi', Decimal('1180591620717411303424')),
            ('yobi',  'Yi', Decimal('1208925819614629174706176')),
        ]

        calculator.unit_normaliser.add_prefixed_unit('data', UnitDefinitionBit, Decimal('1'))
        calculator.unit_normaliser.get_unit('bits').systems.append('iec')
        for prefix in extended_si_prefixes:
            calculator.unit_normaliser.add_unit('data', UnitDefinitionBit(prefix))
        for prefix in iec_prefixes:
            unit = UnitDefinitionBit(prefix)
            unit.systems = ['iec']
            calculator.unit_normaliser.add_unit('data', unit)

        calculator.unit_normaliser.add_prefixed_unit('data', UnitDefinitionByte, Decimal('1'))
        calculator.unit_normaliser.get_unit('bytes').systems.append('iec')
        for prefix in extended_si_prefixes:
            calculator.unit_normaliser.add_unit('data', UnitDefinitionByte(prefix))
        for prefix in iec_prefixes:
            unit = UnitDefinitionByte(prefix)
            unit.systems = ['iec']
            calculator.unit_normaliser.add_unit('data', unit)


class UnitDefinitionBit(UnitDefinition):

    namelist = ['bits','bit']
    symbollist = ['bit'] # Otherwise we're stopping b from being used as a variable
    systems = ['si']
    use_for_condense = False

class UnitDefinitionByte(UnitDefinition):

    namelist = ['bytes','byte']
    symbollist = ['B']
    unitscale = Decimal('8')
    systems = ['si']
    use_for_condense = False