#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class MagneticFluxUnitFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.magneticflux'

    def title():
        return 'Magnetic Flux Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.electriccurrent', 'unitdefinitions.distance', 'unitdefinitions.time', 'unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('magneticflux', 'Magnetic Flux',
            ['mass', Number(1),
             'distance', Number(2),
             'time', Number(-2),
             'electriccurrent', Number(-1)])

        calculator.unit_normaliser.add_prefixed_unit('magneticflux', UnitDefinitionWeber)


class UnitDefinitionWeber(UnitDefinition):

    namelist = ['webers','weber']
    symbollist = ['Wb']
    systems = ['si']
