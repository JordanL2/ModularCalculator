#!/usr/bin/python3

from modularcalculator.features.structure.functions import FunctionDefinition
from modularcalculator.objects.operators import OperationResult
from modularcalculator.features.feature import Feature

from decimal import *
import math


class OrbitalMechanicsFunctionsFeature(Feature):

    def id():
        return 'unitfunctions.orbitalmechanicsfunctions'

    def category():
        return 'Unit Functions'

    def title():
        return 'Orbital Mechanics Functions'

    def desc():
        return ''

    def dependencies():
        return ['units.units', 'structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['deltav'] = FunctionDefinition(
            'Orbital Mechanics', 
            'deltav', 
            '', #TODO
            '', #TODO
            OrbitalMechanicsFunctionsFeature.func_deltav, 
            3, 
            3, 
            'number')
        calculator.funcs['deltav'].add_unit_restriction(0, 0, ['time', 1])
        calculator.funcs['deltav'].add_unit_restriction(1, 2, ['mass', 1])
        calculator.funcs['deltav'].units_multi = True

    def func_deltav(self, vals, units, refs, flags):
        num, fromunit = vals[0], units[0]
        tounit = self.unit_normaliser.get_unit('seconds')
        isp, tounit = self.unit_normaliser.unit_conversion(num, fromunit, tounit, False)

        mass_ratio = vals[1] / vals[2]

        res = OperationResult(isp * Decimal(math.log(mass_ratio)) * Decimal('9.80665'))
        res.set_unit(self.unit_normaliser.make_multiunit(['meter', 1, 'second', -1]))
        return res
