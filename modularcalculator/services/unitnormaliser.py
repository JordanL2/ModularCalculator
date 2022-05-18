#!/usr/bin/python3

from modularcalculator.engine import *
from modularcalculator.objects.number import *
from modularcalculator.objects.units import *

import math


class UnitNormaliser:

    def __init__(self, calculator):
        self.calculator = calculator

        self.systems = {}
        self.systems_preference = []

        self.dimensions = {}
        self.relationships = {}

        self.units = {}
        self.ambiguous_units = []
        self.multiunits = {}
        self.prefixes = []

        self.unitnames = {}
        self.unitnamesmaxlength = 0
        self.unitsymbols = {}
        self.unitsymbolsmaxlength = 0

        self.simplify_allow_prefixed_units = True
        self.simplify_preferred_magnitude = 1
        self.simplify_penalise_below = Number('0.1')
        self.simplify_penalty = 1000

    def list_units(self):
        return [unit for unitlist in self.units.values() for unit in unitlist] + self.ambiguous_units

    def add_dimension(self, dimension, title, relationship=None):
        self.dimensions[dimension] = title
        if relationship is not None:
            dimensions = self.relationship_to_dimensions(relationship)
            self.relationships[dimension] = dimensions

    def add_unit(self, dimension, unit):
        if dimension not in self.dimensions:
            raise Exception("Dimension not found: {0}".format(dimension))
        unit.dimension = dimension
        if dimension not in self.units:
            self.units[dimension] = []
        self.units[dimension].append(unit)
        for name in unit.names():
            self.unitnames[name.lower()] = unit
            if len(name) > self.unitnamesmaxlength:
                self.unitnamesmaxlength = len(name)
        for symbol in unit.symbols():
            self.unitsymbols[symbol] = unit
            if len(symbol) > self.unitsymbolsmaxlength:
                self.unitsymbolsmaxlength = len(symbol)

    def add_prefixed_unit(self, dimension, unit, minscale=None, maxscale=None):
        hit_min = False
        for prefix in self.prefixes:
            if (minscale is None or minscale <= prefix[2]) and (maxscale is None or maxscale >= prefix[2]):
                self.add_unit(dimension, unit(prefix))

    def add_ambiguous_unit(self, ambiguous_unit, units):
        for unit in units:
            ambiguous_unit.add_unit(self.get_unit(unit))
        self.ambiguous_units.append(ambiguous_unit)
        for name in ambiguous_unit.names():
            self.unitnames[name.lower()] = ambiguous_unit
            if len(name) > self.unitnamesmaxlength:
                self.unitnamesmaxlength = len(name)
        for symbol in ambiguous_unit.symbols():
            self.unitsymbols[symbol] = ambiguous_unit
            if len(symbol) > self.unitsymbolsmaxlength:
                self.unitsymbolsmaxlength = len(symbol)

    def add_multiunit(self, dimension, units):
        multiunit = self.make_multiunit(units)
        if dimension not in self.multiunits:
            self.multiunits[dimension] = []
        self.multiunits[dimension].append(multiunit)

    def get_unit(self, unitname):
        for unit in self.ambiguous_units:
            if unit.isunit(unitname):
                return self.get_preferred_unit(unit)
        if unitname.lower() in self.unitnames:
            return self.unitnames[unitname.lower()]
        if unitname in self.unitsymbols:
            return self.unitsymbols[unitname]
        return None

    def get_system(self, system, dimension=None):
        units = []
        for this_dimension in self.units.keys():
            if dimension is None or dimension == this_dimension:
                for unit in self.units[this_dimension]:
                    if system in unit.systems and unit.use:
                        units.append(unit)
        return sorted(units, key=lambda u: u.convertfrom(Number(1), False), reverse=True)

    def get_preferred_system(self, systems):
        for system in self.systems_preference:
            if system in systems:
                return system
        return None

    def get_preferred_unit(self, ambiguous_unit):
        system = self.get_preferred_system(ambiguous_unit.units.keys())
        return ambiguous_unit.units[system]

    def unit_conversion(self, num, fromunit, tounit, relative):
        if fromunit == tounit:
            return num, fromunit
        if fromunit is None:
            raise CalculatorException("From unit is not set")
        if tounit is None:
            raise CalculatorException("To unit is not set")
        if self.unit_normalised_dimensionlist(fromunit) != self.unit_normalised_dimensionlist(tounit):
            raise CalculatorException("Can't convert units: {0} and {1}".format(fromunit.plural(), tounit.plural()))

        if fromunit != tounit:
            num = fromunit.convertfrom(num, relative)
            num = tounit.convertto(num, relative)

        return num, tounit

    def make_multiunit(self, units):
        units = units.copy()
        for i in range(0, len(units), 2):
            units[i] = self.get_unit(units[i])
        return UnitPowerList.new(units)

    def normalise_inputs(self, values, units, multi, relative):
        resultunit = None
        actualunits = [unit for unit in units if unit is not None]
        if len(actualunits) > 0 and not multi:
            resultunit = actualunits[0]

        if len(actualunits) > 0 and len(values) > 1:
            if multi:
                for i in range(len(values) - 2, -1, -1):
                    for j in range(i + 1, len(values)):
                        if units[i] is not None and units[j] is not None:
                            values[i], units[i], values[j], units[j] = self.normalise_from_left(values[i], units[i].copy(), values[j], units[j].copy(), relative)
                            values[i], units[i], values[j], units[j] = self.normalise_from_right(values[i], units[i].copy(), values[j], units[j].copy(), relative)
            else:
                for i in range(1, len(units)):
                    values[i], units[i] = self.unit_conversion(values[i], units[i], units[0], relative)

        return values, units, resultunit

    def normalise_from_left(self, value1, unit1, value2, unit2, relative):
        unitdimensions = self.get_units_by_dimension(unit1)
        for dimensionlist, unit in unitdimensions.items():
            for power in (1, -1):
                dimensions = dimensionlist.multiply(power)

                unitlist2 = [u for u in self.get_subunit_list(unit2) if u.unit not in unitdimensions.values()]
                unitsfound = self.find_units_matching_dimensions([dimensions], unitlist2)[0]
                while len(unitsfound) > 0:
                    unitsfound = unitsfound[0]
                    value2 = unit2.addandconvert(value2, unit, power, relative)
                    for remove in unitsfound:
                        value2 = unit2.removeandconvert(value2, remove.unit, remove.power, relative)
                    unitlist2 = [u for u in self.get_subunit_list(unit2) if u.unit not in unitdimensions.values()]
                    unitsfound = self.find_units_matching_dimensions([dimensions], unitlist2)[0]

        return value1, unit1.check_empty(), value2, unit2.check_empty()

    def normalise_from_right(self, value1, unit1, value2, unit2, relative):
        unitlist1 = self.get_subunit_list(unit1)
        unitdimensions2 = self.get_units_by_dimension(unit2)
        for dimensionlist, unit in unitdimensions2.items():
            for power in (1, -1):
                dimensions = dimensionlist.multiply(power)
                unitsfound = self.find_units_matching_dimensions([dimensions], unitlist1)[0]
                if len(unitsfound) > 0:
                    unitsfound = unitsfound[0]
                    value2 = unit2.removeandconvert(value2, unit, power, relative)
                    for add in unitsfound:
                        addpower = add.power * abs(power)
                        value2 = unit2.addandconvert(value2, add.unit, addpower, relative)

        return value1, unit1.check_empty(), value2, unit2.check_empty()

    def simplify_units(self, value, unit):
        if len(unit.list()) > 1 or (len(unit.list()) == 1 and unit.list()[0].power < 0):
            unit = unit.copy()
            dimensions_list = list(self.units.keys())
            powerlist = [1, -1, 2, -2]
            replacedimensions_list = [self.normalised_dimension(d).multiply(p) for d in dimensions_list for p in powerlist]

            while True:
                unitlist = self.get_subunit_list(unit)
                systems = set([s for u in unitlist for s in u.unit.systems])
                unitsfound_list_list = self.find_units_matching_dimensions(replacedimensions_list, unitlist)

                for i, unitsfound_list in enumerate(unitsfound_list_list):
                    dimension = dimensions_list[int(i / len(powerlist))]
                    units = self.units[dimension]
                    if dimension in self.multiunits:
                        units = units.copy()
                        units.extend(self.multiunits[dimension])
                    power = powerlist[i % len(powerlist)]

                    found = False
                    for unitsfound in unitsfound_list:
                        multpower = min([unit.find(u.unit).power / u.power for u in unitsfound])
                        if (len(unitsfound) > 1) or (len(unit.list()) == 1 and unit.list()[0].power < 0 and unit.list()[0].power == -(power * multpower)):
                            closest_unit = None
                            closest_value = None
                            unitsfound_dimensioncount = len([d for u in unitsfound for d in self.normalised_dimension(u.unit.dimension)])
                            for replace_unit in units:
                                replace_unit_systems = None
                                if not self.simplify_allow_prefixed_units and isinstance(replace_unit, UnitDefinition) and replace_unit.nameprefix is not None and replace_unit.nameprefix != '':
                                    continue
                                elif isinstance(replace_unit, UnitPowerList):
                                    replace_unit_systems = [s for u in replace_unit.list() for s in u.unit.systems]
                                else:
                                    replace_unit_systems = replace_unit.systems + replace_unit.relevant_to_systems
                                if isinstance(replace_unit, UnitDefinition) and not replace_unit.use_for_condense:
                                    continue
                                elif len([s for s in replace_unit_systems if s in systems]) == 0:
                                    continue
                                elif isinstance(replace_unit, UnitPowerList) and len([d for u in replace_unit.list() for d in self.normalised_dimension(u.unit.dimension)]) >= unitsfound_dimensioncount:
                                    continue
                                else:
                                    if value == Number(0):
                                        # Value is 0, so just get the simplest unit possible
                                        if closest_unit is None or abs(math.log10(replace_unit.unitscale)) < abs(math.log10(closest_unit.unitscale)):
                                            closest_unit = replace_unit
                                            closest_value = value
                                    else:
                                        replace_value = value
                                        for unitpower in unitsfound:
                                            replace_value = unitpower.unit.convert(replace_value, -(unitpower.power * multpower), False)
                                        replace_value = replace_unit.convert(replace_value, (power * multpower), False)
                                        if closest_value is None or self.get_closeness(replace_value) < self.get_closeness(closest_value):
                                            closest_unit = replace_unit
                                            closest_value = replace_value
                            if closest_unit is not None:
                                for subunit in unitsfound:
                                    value = unit.removeandconvert(value, subunit.unit, int(subunit.power * multpower), False)
                                value = unit.addandconvert(value, closest_unit, int(power * multpower), False)
                                found = True
                                break
                    if found:
                        break
                else:
                    break

        value, unit = self.dedupe(value, unit)

        return value, unit.check_empty()

    # Check if any remaining subunits are the same dimension
    def dedupe(self, value, unit):
        if len(unit.list()) > 1:
            # Get list of dimensions and index of subunits
            dimensions = {}
            for di in [(u.unit.dimension, i) for i, u in enumerate(unit.list())]:
                if di[0] not in dimensions:
                    dimensions[di[0]] = []
                dimensions[di[0]].append(di[1])

            for dimension in dimensions:
                units_i = dimensions[dimension]
                if len(units_i) > 1:
                    # Need to de-dupe. This code should only happen if the remaining units cancel out completely.
                    power = sum([unit.list()[i].power for i in units_i])
                    if power != 0:
                        raise Exception("simplify_units did not dedupe units")

                    # Remove existing units
                    units_to_remove = [unit.list()[i] for i in units_i]
                    for unit_to_remove in units_to_remove:
                        value = unit.removeandconvert(value, unit_to_remove.unit, unit_to_remove.power, False)


        return value, unit

    def get_closeness(self, num):
        closeness = abs(math.log10(abs(float(num))) - self.simplify_preferred_magnitude)
        if num < self.simplify_penalise_below:
            closeness *= self.simplify_penalty
        return closeness

    def find_units_matching_dimensions(self, dimension_lists, unitlist):
        unit_dimensionlist = [d for u in unitlist for d in u.dimensions]
        unit_dimensionlist_dimensions = [d.dimension for d in unit_dimensionlist]
        dimension_lists_dimensions = [d for dl in dimension_lists for d in dl.list()]
        for dimension in dimension_lists_dimensions:
            if dimension.dimension in unit_dimensionlist_dimensions:
                break
        else:
            return [[] for d in range(0, len(dimension_lists))]

        dimensionlist_map = {}
        for dimension in dimension_lists_dimensions + unit_dimensionlist:
            if dimension.dimension not in dimensionlist_map:
                dimensionlist_map[dimension.dimension] = len(dimensionlist_map)

        goals = []
        for dimensions in dimension_lists:
            goals.append([0] * len(dimensionlist_map))
            for dimension in dimensions:
                goals[-1][dimensionlist_map[dimension.dimension]] = dimension.power

        unitlist_max = []
        unitlist_min = []
        for unit in unitlist:
            if unit.power < 0:
                unitlist_min.append(int(unit.power))
                unitlist_max.append(0)
            else:
                unitlist_min.append(0)
                unitlist_max.append(int(unit.power))
        unitlist_counter = unitlist_min.copy()

        found = [[] for d in range(0, len(dimension_lists))]
        stop = False
        while not stop:

            thisgoal = [0] * len(dimensionlist_map)
            for i in range(0, len(unitlist_counter)):
                n = unitlist_counter[i]
                for dimension in unitlist[i].dimensions:
                    thisgoal[dimensionlist_map[dimension.dimension]] += (n * dimension.power)

            for j, goal in enumerate(goals):
                if goal == thisgoal:
                    returnlist = []
                    for i in range(0, len(unitlist_counter)):
                        if unitlist_counter[i] != 0:
                            returnlist.append(UnitPower(unitlist[i].unit, unitlist_counter[i]))
                    found[j].append(returnlist)

            unitlist_counter[-1] += 1
            for i in range(len(unitlist_counter) - 1, -1, -1):
                if unitlist_counter[i] > unitlist_max[i]:
                    if i == 0:
                        stop = True
                        break
                    unitlist_counter[i] = unitlist_min[i]
                    unitlist_counter[i - 1] += 1

        return found

    def unit_normalised_dimensionlist(self, unit):
        return DimensionPowerList([DimensionPower(d.dimension, d.power * u.power) for u in self.get_subunit_list(unit) for d in u.dimensions]).deduplicate()

    def get_subunit_list(self, unit):
        return [UnitPowerDimensions(u.unit, u.power, self.normalised_dimension(u.unit.dimension)) for u in unit.list()]

    def normalised_dimension(self, dimension):
        if dimension in self.relationships:
            return self.relationships[dimension]
        return DimensionPowerList([DimensionPower(dimension, 1)])

    def get_units_by_dimension(self, unit):
        dimensiontounit = {}
        for unitpower in unit.list():
            dimensiontounit[self.normalised_dimension(unitpower.unit.dimension)] = unitpower.unit
        return dimensiontounit

    def relationship_to_dimensions(self, relationship):
        dimensions = []
        for i in range(0, int(len(relationship) / 2)):
            dimension = relationship[i * 2]
            power = relationship[i * 2 + 1]
            if dimension not in self.dimensions:
                raise Exception("Dimension not found: {0}".format(dimension))
            dimensions.append(DimensionPower(dimension, power))
        return DimensionPowerList(dimensions)

    def unit_to_relationship(self, unit):
        if unit is None:
            return None
        return self.dimensionlist_to_relationship(self.unit_normalised_dimensionlist(unit))

    def standardise_relationship(self, relationship):
        return self.dimensionlist_to_relationship(self.relationship_to_dimensions(relationship.copy()))

    def dimensionlist_to_relationship(self, dimensionlist):
        return [(d.dimension, d.power) for d in dimensionlist]

    def check_unit_dimensions(self, unit, relationship):
        unit_relationship = self.unit_to_relationship(unit)
        expected_relationship = self.standardise_relationship(relationship.copy())
        return unit_relationship == expected_relationship
