#!usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *


class AbstractUnitDefinition:

    nameprefix = None
    symbolprefix = None
    namelist = None
    symbollist = None

    def __init__(self, prefix=None):
        if prefix is not None:
            self.nameprefix = prefix[0]
            self.symbolprefix = prefix[1]

    def __str__(self):
        return self.plural()

    def isunit(self, name):
        return (name.lower() in [n.lower() for n in self.names()] or name in self.symbols())

    def get_name(self, num):
        if num == Number(1):
            return self.singular()
        return self.plural()

    def plural(self):
        return self.names()[0]

    def singular(self):
        return self.names()[1]

    def symbol(self):
        return self.symbols()[0]

    def has_symbols(self):
        return self.symbollist is not None and len(self.symbollist) > 0

    def names(self):
        if self.namelist is None:
            return []
        if self.nameprefix is not None:
            return [self.nameprefix + n for n in self.namelist]
        return self.namelist

    def symbols(self):
        if self.symbollist is None:
            return []
        if self.symbolprefix is not None:
            return [self.symbolprefix + n for n in self.symbollist]
        return self.symbollist


class AmbiguousUnitDefinition(AbstractUnitDefinition):

    units = None

    def __init__(self):
        self.units = {}

    def add_unit(self, unit):
        for system in unit.systems:
            if system in self.units:
                raise Exception("Already have a unit for system {0}".format(system))
            self.units[system] = unit


class UnitDefinition(AbstractUnitDefinition):

    dimension = None
    unitscale = Number(1)
    systems = []
    relevant_to_systems = []
    use = True
    use_for_condense = True

    def __init__(self, prefix=None):
        super().__init__(prefix)
        if prefix is not None:
            self.unitscale *= prefix[2]
        self.systems = self.systems.copy()
        self.relevant_to_systems = self.relevant_to_systems.copy()

    def list(self):
        return [UnitPower(self, Number(1))]

    def convert(self, num, power, relative):
        if power > 0:
            for n in range(0, int(power)):
                num = self.convertto(num, relative)
        else:
            for n in range(0, abs(int(power))):
                num = self.convertfrom(num, relative)
        return num

    def convertfrom(self, num, relative):
        return num * self.unitscale

    def convertto(self, num, relative):
        return num / self.unitscale


class AbstractPower:

    keyclass = None
    keyfield = None

    def __init__(self, obj, power):
        if not isinstance(obj, self.keyclass):
            raise Exception("object must be of type {0}".format(self.keyclass.__name__))
        setattr(self, self.keyfield, obj)

        if not isinstance(power, Number):
            raise Exception("power must be of type Number")
        if round(power, getcontext().prec - 2) != round(power):
            raise CalculatorException("Non-integer power {0}".format(power))
        self.power = Number(round(power))

    def __eq__(self, other):
        return getattr(self, self.keyfield) == getattr(other, self.keyfield) and self.power == other.power

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return str(getattr(self, self.keyfield)) + '^' + str(self.power)

    def copy(self):
        return type(self)(getattr(self, self.keyfield), self.power)

    def multiply(self, power):
        return type(self)(getattr(self, self.keyfield), self.power * power)

    def key(self):
        raise Exception("Must overrride this method")


class AbstractPowerList:

    keyclass = None

    def __init__(self, objs=None):
        if objs is not None:
            if not isinstance(objs, list):
                raise Exception("objs must be of type list")
            for obj in objs:
                if not isinstance(obj, self.keyclass):
                    raise Exception("objs must be of type list of ".format(self.keyclass.__name__))
            self._set(objs)
        else:
            self.clear()

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return str.join(', ', sorted([str(o) for o in self.list()], key=str))

    def __len__(self):
        return len(self.list())

    def __iter__(self):
        return iter(self.list())

    def __add__(self, other):
        return type(self)(self.list() + other.list())

    def _add(self, obj):
        self._objects.append(obj)

    def _del(self, obj):
        self._objects.remove(obj)

    def _set(self, objs):
        self._objects = objs

    def list(self):
        return self._objects

    def clear(self):
        self._set([])

    def find(self, key):
        for obj in self.list():
            if obj.key() == key:
                return obj
        return None

    def add(self, key, power):
        existing = self.find(key)
        if existing is None:
            self._add(self.keyclass(key, Number(power)))
        else:
            existing.power += power
            if existing.power == 0:
                self._del(existing)

    def remove(self, key, power):
        self.add(key, -power)

    def copy(self):
        return type(self)([o.copy() for o in self.list()])

    def multiply(self, power):
        return type(self)([o.multiply(power) for o in self.list()])

    def merge(self, other):
        newlist = self.copy()
        for obj in other.list():
            newlist.add(obj.key(), obj.power)
        return newlist

    def deduplicate(self):
        newlist = self.copy()
        for i, obj in enumerate(newlist.list()):
           duplicates = [o for j, o in enumerate(newlist.list()[i + 1:]) if o.key() == obj.key()]
           for duplicate in duplicates:
               obj.power += duplicate.power
               newlist._del(duplicate)
        return newlist.remove_zeros()

    def remove_zeros(self):
        return type(self)([o.copy() for o in self.list() if o.power != 0])

    def check_empty(self):
        if len(self.list()) == 0:
            return None
        return self


class UnitPower(AbstractPower):

    keyclass = UnitDefinition
    keyfield = 'unit'

    def key(self):
        return self.unit


class UnitPowerList(AbstractPowerList):

    keyclass = UnitPower

    no_simplify = False

    def new(unitpowers):
        unitpowerlist = UnitPowerList()
        for i in range(0, int(len(unitpowers) / 2)):
            unit = unitpowers[i * 2]
            power = Number(unitpowers[i * 2 + 1])
            unitpowerlist.addall(unit, power)
        return unitpowerlist.check_empty()

    def newfromunit(unit):
        unitpowerlist = UnitPowerList()
        unitpowerlist.add(unit, 1)
        return unitpowerlist

    def copy(self):
        unitpowerlist = super().copy()
        unitpowerlist.no_simplify = self.no_simplify
        return unitpowerlist

    def get_name(self, num, string_result=True):
        if num == Number(1):
            return self.singular(False, string_result)
        return self.plural(False, string_result)

    def plural(self, negative_powers=False, string_result=True):
        return self.name(True, False, negative_powers, string_result)

    def singular(self, negative_powers=False, string_result=True):
        return self.name(False, False, negative_powers, string_result)

    def symbol(self, string_result=True):
        return self.name(False, True, False, string_result)

    def has_symbols(self):
        for unitpower in self.list():
            if not unitpower.unit.has_symbols():
                return False
        return True

    def name(self, plural, symbol, negative_powers, string_result):
        mults = []
        divs = []
        for unitpower in self.list():
            if unitpower.power < 0:
                divs.append(unitpower)
            else:
                mults.append(unitpower)
        if len(mults) == 0:
            negative_powers = True

        multstrings = []
        for i, mult in enumerate(mults):
            last = i == len(mults) - 1
            unitname = mult.unit.singular()
            if symbol:
                unitname = mult.unit.symbol()
            elif plural and last:
                unitname = mult.unit.plural()
            multstrings.append((' ', 'space'))
            if mult.power > 1:
                multstrings.append((unitname, 'unit'))
                multstrings.append(('^', 'op'))
                multstrings.append((str(mult.power), 'literal'))
            else:
                multstrings.append((unitname, 'unit'))
        if len(multstrings) > 0:
            multstrings.pop(0)

        divstrings = []
        for i, div in enumerate(divs):
            unitname = div.unit.singular()
            if symbol:
                unitname = div.unit.symbol()
            elif negative_powers:
                unitname = div.unit.plural()
            divstrings.append((' ', 'space'))
            if div.power < -1 or negative_powers:
                divstrings.append((unitname, 'unit'))
                divstrings.append(('^', 'op'))
                if negative_powers:
                    divstrings.append((str(div.power), 'literal'))
                else:
                    divstrings.append((str(-div.power), 'literal'))
            else:
                divstrings.append((unitname, 'unit'))
        if len(divstrings) > 0:
            divstrings.pop(0)
        if len(mults) > 0 and len(divs) > 1 and not negative_powers:
            divstrings = [('(', 'inner_expr_start')] + divstrings + [('(', 'inner_expr_end')]

        finalstrings = []
        if len(mults) > 0 and len(divs) > 0:
            finalstrings = multstrings + [('/', 'op')] + divstrings
        elif len(mults) > 0:
            finalstrings = multstrings
        elif len(divs) > 0:
            finalstrings = divstrings

        if string_result:
            return ''.join([s[0] for s in finalstrings])
        else:
            return finalstrings

    def convert(self, num, power, relative):
        for unitpower in self.list():
            num = unitpower.unit.convert(num, unitpower.power * power, relative)
        return num

    def convertfrom(self, num, relative):
        return self.convert(num, -1, relative)

    def convertto(self, num, relative):
        return self.convert(num, 1, relative)

    def addall(self, unitlist, power):
        for unitpower in unitlist.list():
            self.add(unitpower.unit, unitpower.power * power)

    def removeall(self, unit, power):
        self.addall(unit, -power)

    def addandconvert(self, value, unit, power, relative):
        value = unit.convert(value, power, relative)
        self.addall(unit, power)
        return value

    def removeandconvert(self, value, unit, power, relative):
        value = unit.convert(value, -power, relative)
        self.removeall(unit, power)
        return value

    def power(self, power):
        return self.multiply(power).remove_zeros().check_empty()


class DimensionPower(AbstractPower):

    keyclass = str
    keyfield = 'dimension'

    def key(self):
        return self.dimension


class DimensionPowerList(AbstractPowerList):

    keyclass = DimensionPower


class UnitPowerDimensions(UnitPower):

    def __init__(self, unit, power, dimensions):
        super().__init__(unit, power)
        self.dimensions = dimensions
