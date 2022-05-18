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
            ('zetta',  'Z', Number('1000000000000000000000')),
            ('yotta',  'Y', Number('1000000000000000000000000')),
        ]

        iec_prefixes = [
            ('kibi',  'ki', Number('1024')),
            ('mebi',  'Mi', Number('1048576')),
            ('gibi',  'Gi', Number('1073741824')),
            ('tebi',  'Ti', Number('1099511627776')),
            ('pebi',  'Pi', Number('1125899906842624')),
            ('exbi',  'Ei', Number('1152921504606846976')),
            ('zebi',  'Zi', Number('1180591620717411303424')),
            ('yobi',  'Yi', Number('1208925819614629174706176')),
        ]

        calculator.unit_normaliser.add_prefixed_unit('data', UnitDefinitionBit, Number('1'))
        calculator.unit_normaliser.get_unit('bits').systems.append('iec')
        for prefix in extended_si_prefixes:
            calculator.unit_normaliser.add_unit('data', UnitDefinitionBit(prefix))
        for prefix in iec_prefixes:
            unit = UnitDefinitionBit(prefix)
            unit.systems = ['iec']
            calculator.unit_normaliser.add_unit('data', unit)

        calculator.unit_normaliser.add_prefixed_unit('data', UnitDefinitionByte, Number('1'))
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
    unitscale = Number('8')
    systems = ['si']
    use_for_condense = False