#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *

from decimal import *


class VolumeUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.volume'

    def title():
        return 'Volume Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.distance']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('volume', 'Volume', ['distance', 3])
        
        calculator.unit_normaliser.add_prefixed_unit('volume', UnitDefinitionLiter, None, Decimal('1'))
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionLiter(('centi', 'c', Decimal('0.01'))))
        
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUKFluidOunce())
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUKGill())
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUKPint())
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUKQuart())
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUKGallon())

        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUSDram())
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUSFluidOunce())
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUSGill())
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUSCup())
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUSPint())
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUSQuart())
        calculator.unit_normaliser.add_unit('volume', UnitDefinitionUSGallon())
        
        calculator.unit_normaliser.add_ambiguous_unit(AmbiguousUnitDefinitionFluidOunce(), ['US fluid ounce', 'UK fluid ounce'])
        calculator.unit_normaliser.add_ambiguous_unit(AmbiguousUnitDefinitionPint(), ['US pint', 'UK pint'])
        calculator.unit_normaliser.add_ambiguous_unit(AmbiguousUnitDefinitionQuart(), ['US quart', 'UK quart'])
        calculator.unit_normaliser.add_ambiguous_unit(AmbiguousUnitDefinitionGallon(), ['US gallon', 'UK gallon'])


class UnitDefinitionLiter(UnitDefinition):

    namelist = ['liters','liter','litres','litre']
    symbollist = ['l']
    unitscale = Decimal('0.001')
    systems = ['si']

class UnitDefinitionUKFluidOunce(UnitDefinition):

    namelist = ['UK fluid ounces','UK fluid ounce']
    symbollist = ['ukfloz','ukfl.oz']
    unitscale = Decimal('0.0000284130625')
    systems = ['uk']

class UnitDefinitionUKGill(UnitDefinition):

    namelist = ['UK gills','UK gill']
    symbollist = ['ukgill']
    unitscale = Decimal('0.0001420653125')
    systems = ['uk']
    use = False

class UnitDefinitionUKPint(UnitDefinition):

    namelist = ['UK pints','UK pint']
    symbollist = ['ukpt']
    unitscale = Decimal('0.00056826125')
    systems = ['uk']

class UnitDefinitionUKQuart(UnitDefinition):

    namelist = ['UK quarts','UK quart']
    symbollist = ['ukquart']
    unitscale = Decimal('0.0011365225')
    systems = ['uk']
    use = False

class UnitDefinitionUKGallon(UnitDefinition):

    namelist = ['UK gallons','UK gallon']
    symbollist = ['ukgal']
    unitscale = Decimal('0.00454609')
    systems = ['uk']

class UnitDefinitionUSDram(UnitDefinition):

    namelist = ['US drams','US dram']
    symbollist = ['usdr']
    unitscale = Decimal('0.00000184834559765625')
    systems = ['us']

class UnitDefinitionUSFluidOunce(UnitDefinition):

    namelist = ['US fluid ounces','US fluid ounce']
    symbollist = ['usfloz','usfl.oz']
    unitscale = Decimal('0.0000295735295625')
    systems = ['us']

class UnitDefinitionUSGill(UnitDefinition):

    namelist = ['US gills','US gill']
    symbollist = ['usgill']
    unitscale = Decimal('0.00011829411825')
    systems = ['us']
    use = False

class UnitDefinitionUSCup(UnitDefinition):

    namelist = ['US cups','US cup']
    symbollist = ['uscup']
    unitscale = Decimal('0.0002365882365')
    systems = ['us']

class UnitDefinitionUSPint(UnitDefinition):

    namelist = ['US pints','US pint']
    symbollist = ['uspt']
    unitscale = Decimal('0.000473176473')
    systems = ['us']

class UnitDefinitionUSQuart(UnitDefinition):

    namelist = ['US quarts','US quart']
    symbollist = ['usquart']
    unitscale = Decimal('0.000946352946')
    systems = ['us']

class UnitDefinitionUSGallon(UnitDefinition):

    namelist = ['US gallons','US gallon']
    symbollist = ['usgal']
    unitscale = Decimal('0.003785411784')
    systems = ['us']

class AmbiguousUnitDefinitionFluidOunce(AmbiguousUnitDefinition):

    namelist = ['fluid ounces','fluid ounce']
    symbollist = ['floz','fl.oz']

class AmbiguousUnitDefinitionPint(AmbiguousUnitDefinition):

    namelist = ['pints','pint']
    symbollist = ['pt']

class AmbiguousUnitDefinitionQuart(AmbiguousUnitDefinition):

    namelist = ['quarts','quart']
    symbollist = ['quart']

class AmbiguousUnitDefinitionGallon(AmbiguousUnitDefinition):

    namelist = ['gallons','gallon']
    symbollist = ['gal']
