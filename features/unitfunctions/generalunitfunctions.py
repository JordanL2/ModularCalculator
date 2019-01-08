#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.units import *
from modularcalculator.features.structure.functions import FunctionDefinition
from modularcalculator.objects.operators import OperationResult
from modularcalculator.features.feature import Feature

from decimal import *


class GeneralUnitFunctionsFeature(Feature):

    def id():
        return 'unitfunctions.generalunitfunctions'

    def category():
        return 'Unit Functions'

    def title():
        return 'General Unit Functions'

    def desc():
        return ''

    def dependencies():
        return ['units.units', 'units.systems', 'structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['format'] = FunctionDefinition('Units', 'format', GeneralUnitFunctionsFeature.func_format, 1, 2)
        calculator.funcs['format'].add_value_restriction(0, 0, 'number with unit')
        calculator.funcs['format'].add_value_restriction(1, 1, 'unitsystem')
        calculator.funcs['format'].units_normalise = False
        
        calculator.funcs['compact'] = FunctionDefinition('Units', 'compact', GeneralUnitFunctionsFeature.func_compact, 1, 1)
        calculator.funcs['compact'].add_value_restriction(0, 0, 'number with unit')

    def func_format(self, vals, units, refs, flags):
        num, unit = vals[0], units[0]
        num, unit = self.unit_normaliser.simplify_units(num, unit)
        if unit is None:
            raise CalculatorException("Input must have a unit")
        if len(unit.list()) != 1:
            raise CalculatorException("Can only format single units")
        power = unit.list()[0].power
        if power != 1:
            raise CalculatorException("Unit must have power of 1")
        
        singleunit = unit.list()[0].unit
        if len(vals) >= 2:
            system = vals[1]
        else:
            if singleunit.systems is None or len(singleunit.systems) == 0:
                raise CalculatorException("Unit is not part of a measuring system")
            system = self.unit_normaliser.get_preferred_system(singleunit.systems)
        
        systemunits = self.unit_normaliser.get_system(system, singleunit.dimension)
        if len(systemunits) == 0:
            raise CalculatorException("No units in system {0} found for dimension {1}".format(system, singleunit.dimension))
        nonprefixedsystemunits = [s for s in systemunits if s.nameprefix is None]

        parts = []
        for systemunit in nonprefixedsystemunits:
            num = unit.convertfrom(num, False)
            num = systemunit.convertto(num, False)
            unit = systemunit
            last = (systemunit == nonprefixedsystemunits[-1])
            if num >= Decimal('1') or last:
                if last:
                    num_of_unit, unit = GeneralUnitFunctionsFeature.find_first_unit_prefix_at_least_one(self, num, unit, systemunits)
                else:
                    num_of_unit = self.floor_number(num)
                    num_of_unit, new_unit = GeneralUnitFunctionsFeature.find_first_unit_prefix_at_least_one(self, num_of_unit, unit, systemunits)
                    if new_unit == unit:
                        num -= num_of_unit
                    else:
                        num = unit.convertfrom(num, False)
                        num = new_unit.convertto(num, False)
                        num -= num_of_unit
                        unit = new_unit
                num_of_unit = self.round_number(num_of_unit)
                if num_of_unit != Decimal('0'):
                    parts.append("{0} {1}".format(self.number_to_string(num_of_unit), unit.get_name(num_of_unit)))

        res = OperationResult(str.join(', ', parts))
        res.set_unit(None)
        return res

    def find_first_unit_prefix_at_least_one(self, num, unit, systemunits):
        prefixedunitsofsametype = [s for s in systemunits if s.namelist[0] == unit.namelist[0]]
        old_num = unit.convertfrom(num, False)
        for prefixedunit in prefixedunitsofsametype:
            new_num = prefixedunit.convertto(old_num, False)
            if self.round_number(new_num) >= Decimal('1') or prefixedunit == systemunits[-1]:
                return new_num, prefixedunit

    def func_compact(self, vals, units, refs, flags):
        value, unit = self.unit_normaliser.simplify_units(vals[0], units[0])
        res = OperationResult(value)
        res.set_unit(unit)
        return res
