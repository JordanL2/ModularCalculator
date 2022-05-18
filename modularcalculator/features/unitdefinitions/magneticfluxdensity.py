#!/usr/bin/python3

from modularcalculator.features.unitdefinitions.abstractunitfeature import *


class MagneticFluxDensityFeature(AbstractUnitFeature):

    def id():
        return 'unitdefinitions.magneticfluxdensity'

    def title():
        return 'Magnetic Flux Density Units'

    def desc():
        return ''

    def dependencies():
        return AbstractUnitFeature.dependencies() + ['unitdefinitions.electriccurrent', 'unitdefinitions.time', 'unitdefinitions.mass']

    @classmethod
    def install(cls, calculator):
        calculator.unit_normaliser.add_dimension('magneticfluxdensity', 'Magnetic Flux Density',
            ['mass', Number(1),
             'time', Number(-2),
             'electriccurrent', Number(-1)])

        calculator.unit_normaliser.add_prefixed_unit('magneticfluxdensity', UnitDefinitionTelsa)


class UnitDefinitionTelsa(UnitDefinition):

    namelist = ['teslas','tesla']
    symbollist = ['T']
    systems = ['si']
