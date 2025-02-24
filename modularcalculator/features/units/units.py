#!/usr/bin/python3

from modularcalculator.features.feature import Feature
from modularcalculator.features.numerical.basicarithmetic import BasicArithmeticFeature
from modularcalculator.objects.items import *
from modularcalculator.objects.number import *
from modularcalculator.objects.operators import OperationResult, OperatorDefinition
from modularcalculator.objects.units import *


class UnitsFeature(Feature):

    def id():
        return 'units.units'

    def category():
        return 'Units'

    def title():
        return 'Units'

    def desc():
        return 'Units base feature'

    def dependencies():
        return []

    @classmethod
    def install(cls, calculator):
        calculator.enable_units()
        calculator.unit_simplification = True
        calculator.unit_normaliser.prefixes = [
            (None, None, Number(1)),
        ]
        calculator.unit_symbols_enabled = False

        calculator.add_parser('units', UnitsFeature.parse_units)

        calculator.unit_assignment_op = 'UNIT_ASSIGNMENT'
        calculator.unit_multiply_op = 'UNIT_MULTIPLY'
        calculator.unit_divide_op = 'UNIT_DIVIDE'

        calculator.add_op(OperatorDefinition(
            'Units',
            'to',
            'Convert a value with a unit to another unit',
            UnitsFeature.op_unit_conversion,
            1,
            1,
            [['number with unit', 'unit'], 'unit']),
        {'units_normalise': False})

        calculator.add_op(OperatorDefinition(
            'Units',
            'UNIT_ASSIGNMENT',
            'Assign a unit to a value',
            BasicArithmeticFeature.op_number_multiply,
            1,
            1,
            ['number', 'unit']),
        {'units_normalise': False, 'hidden': True})

        calculator.add_op(OperatorDefinition(
            'Units',
            'UNIT_MULTIPLY',
            'Multiply two units',
            BasicArithmeticFeature.op_number_multiply,
            1,
            1,
            'unit'),
        {'units_normalise': False, 'hidden': True})

        calculator.add_op(OperatorDefinition(
            'Units',
            'UNIT_DIVIDE',
            'Divide two units',
            BasicArithmeticFeature.op_number_divide,
            1,
            1,
            'unit'),
        {'units_normalise': False, 'hidden': True})

        calculator.add_validator('unit', 'unit', UnitsFeature.validate_unit)
        calculator.add_validator('number with unit', 'number with unit', UnitsFeature.validate_number_with_unit)

    def parse_units(self, expr, i, items, flags):
        next = expr[i:]
        next_lower = next.lower()

        for length in range(min(self.unit_normaliser.unitnamesmaxlength, len(next)), 0, -1):

            name = next_lower[0: length]
            if name in self.unit_normaliser.unitnames:
                if len(next) == len(name) or not UnitsFeature.unit_char(self, next[len(name)]):
                    unittext = next[0: len(name)]
                    unit_def = self.unit_normaliser.get_unit(unittext)
                    unitobj = UnitPowerList.newfromunit(unit_def)
                    return [UnitItem(unittext, unitobj)], len(unittext), None

            if self.unit_symbols_enabled:
                symbol = next[0: length]
                if symbol in self.unit_normaliser.unitsymbols:
                    if len(next) == len(symbol) or not UnitsFeature.unit_char(self, next[len(symbol)]):
                        unit_def = self.unit_normaliser.get_unit(symbol)
                        unitobj = UnitPowerList.newfromunit(unit_def)
                        return [UnitItem(symbol, unitobj)], len(symbol), None

        return None, None, None

    def unit_char(self, char):
        return char.isalpha() or char == '_'

    def op_unit_conversion(self, vals, units, refs, flags):
        if isinstance(vals[0], UnitPowerList):
            units[0] = vals[0]
            vals[0] = Number(1)
        num = vals[0]
        if vals[1] is not None and not isinstance(vals[1], UnitPowerList) and vals[1].to_decimal() != 1:
            raise CalculatorException("Second operand must be just a unit")
        fromunit = units[0]
        tounit = vals[1]
        if tounit is None:
            raise CalculatorException("Second operand is not set")
        if not isinstance(tounit, UnitPowerList):
            raise CalculatorException("Second operand is not a unit")

        num, tounit = self.unit_normaliser.unit_conversion(num, fromunit, tounit, False)
        tounit.no_simplify = True

        res = OperationResult(num)
        res.set_unit(tounit)
        return res

    def validate_unit(self, value, unit, ref):
        try:
            return isinstance(value, UnitPowerList)
        except Exception:
            return False

    def validate_number_with_unit(self, value, unit, ref):
        try:
            self.number(value)
            return unit is not None
        except Exception:
            return False


class UnitItem(OperandItem):

    def __init__(self, text, unit):
        super().__init__(text)
        self.unit = unit

    def desc(self):
        return 'unit'

    def category(self):
        return 'special'

    def value(self, flags):
        return self.unit

    def result(self, flags):
        return OperandResult(self.value(flags), None, self)

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.unit = self.unit.copy()
        return copy
