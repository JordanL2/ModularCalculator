#!/usr/bin/python3

from modularcalculator.features.feature import Feature
from modularcalculator.features.structure.functions import FunctionDefinition
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *
from modularcalculator.objects.operators import OperationResult
from modularcalculator.objects.units import *


class GeneralUnitFunctionsFeature(Feature):

    def id():
        return 'units.unitfunctions'

    def category():
        return 'Units'

    def title():
        return 'Unit Functions'

    def desc():
        return ''

    def dependencies():
        return ['units.units', 'units.systems', 'structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['format'] = FunctionDefinition(
            'Units',
            'format',
            'Nicely format a value with a unit, optionally specify the unit system to use',
            ['value', '[system]'],
            GeneralUnitFunctionsFeature.func_format,
            1,
            2)
        calculator.funcs['format'].add_value_restriction(0, 0, 'number with unit')
        calculator.funcs['format'].add_value_restriction(1, 1, 'unitsystem')
        calculator.funcs['format'].units_normalise = False

        calculator.funcs['compact'] = FunctionDefinition(
            'Units',
            'compact',
            'Explicitly simplify the units for a value',
            ['value'],
            GeneralUnitFunctionsFeature.func_compact,
            1,
            1)
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
            if num >= Number(1) or last:
                if last:
                    num_of_unit, unit = GeneralUnitFunctionsFeature.find_first_unit_prefix_at_least_one(self, num, unit, systemunits)
                else:
                    num_of_unit = math.floor(num)
                    num_of_unit, new_unit = GeneralUnitFunctionsFeature.find_first_unit_prefix_at_least_one(self, num_of_unit, unit, systemunits)
                    if new_unit == unit:
                        num -= num_of_unit
                    else:
                        num = unit.convertfrom(num, False)
                        num = new_unit.convertto(num, False)
                        num -= num_of_unit
                        unit = new_unit
                if num_of_unit != Number(0):
                    parts.append("{0} {1}".format(str(num_of_unit), unit.get_name(num_of_unit)))

        res = OperationResult(str.join(', ', parts))
        res.set_unit(None)
        return res

    def find_first_unit_prefix_at_least_one(self, num, unit, systemunits):
        prefixedunitsofsametype = [s for s in systemunits if s.namelist[0] == unit.namelist[0]]
        old_num = unit.convertfrom(num, False)
        for prefixedunit in prefixedunitsofsametype:
            new_num = prefixedunit.convertto(old_num, False)
            if new_num >= Number(1) or prefixedunit == systemunits[-1]:
                return new_num, prefixedunit

    def func_compact(self, vals, units, refs, flags):
        value, unit = self.unit_normaliser.simplify_units(vals[0], units[0])
        res = OperationResult(value)
        res.set_unit(unit)
        return res
