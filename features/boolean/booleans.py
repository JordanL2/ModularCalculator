#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.operators import OperationResult, OperatorDefinition
from modularcalculator.features.feature import Feature

from decimal import *
import re


class BooleansFeature(Feature):

    def id():
        return 'boolean.booleans'

    def category():
        return 'Boolean'

    def title():
        return 'Booleans'

    def desc():
        return 'Boolean type'

    def dependencies():
        return []

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('boolean', BooleansFeature.parse_boolean)
      
        calculator.add_op(OperatorDefinition(
            'Boolean', 
            '!', 
            'Not',
            BooleansFeature.op_boolean_not, 
            0, 
            1, 
            'boolean'),
        {'rtl': True})
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            '<',
            'Less than',
            BooleansFeature.op_number_lessthan, 
            1, 
            1, 
            'number'))
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            '>', 
            'More than',
            BooleansFeature.op_number_morethan, 
            1, 
            1, 
            'number'))
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            '<=', 
            'Less than or equal to',
            BooleansFeature.op_number_lessthanequal, 
            1, 
            1, 
            'number'))
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            '>=', 
            'More than or equal to',
            BooleansFeature.op_number_morethanequal, 
            1, 
            1, 
            'number'))
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            '==', 
            'Equal to',
            BooleansFeature.op_number_equals, 
            1, 
            1, 
            'number'))
        calculator.add_op(OperatorDefinition(
            'Numerical', 
            '!=', 
            'Not equal to',
            BooleansFeature.op_number_notequals, 
            1, 
            1, 
            'number'))
        calculator.add_op(OperatorDefinition(
            'Boolean', 
            '&', 
            'And',
            BooleansFeature.op_boolean_and, 
            1, 
            1, 
            ['boolean', ['boolean', 'exception']]),
        {'inputs_can_be_exceptions': True})
        calculator.add_op(OperatorDefinition(
            'Boolean', 
            '|', 
            'Or',
            BooleansFeature.op_boolean_or, 
            1, 
            1, 
            ['boolean', ['boolean', 'exception']]), 
        {'inputs_can_be_exceptions': True})
        calculator.add_op(OperatorDefinition(
            'Boolean', 
            '?', 
            'Ternary - If A is true, then B, else C',
            BooleansFeature.op_boolean_conditional, 
            1, 
            [1, ':', 1], 
            ['boolean', None, None]), 
        {'units_normalise': False, 'inputs_can_be_exceptions': True})

        calculator.add_number_caster('boolean', BooleansFeature.number_bool)

        calculator.validators['boolean'] = BooleansFeature.validate_boolean

    bool_regex = re.compile(r'(true|false)(\W|$)', re.IGNORECASE)

    def parse_boolean(self, expr, i, items, flags):
        next = expr[i:]
        bool_match = BooleansFeature.bool_regex.match(next)
        if (bool_match):
            boolstring = bool_match.group(1)
            return [LiteralItem(boolstring, (boolstring.lower() == 'true'))], len(boolstring), None
        return None, None, None

    def op_boolean_not(self, vals, units, refs, flags):
        return OperationResult(not BooleansFeature.boolean(self, vals[0]))

    def op_number_equals(self, vals, units, refs, flags):
        return OperationResult(vals[0] == vals[1])

    def op_number_notequals(self, vals, units, refs, flags):
        return OperationResult(vals[0] != vals[1])

    def op_number_lessthan(self, vals, units, refs, flags):
        return OperationResult(vals[0] < vals[1])

    def op_number_morethan(self, vals, units, refs, flags):
        return OperationResult(vals[0] > vals[1])

    def op_number_lessthanequal(self, vals, units, refs, flags):
        return OperationResult(vals[0] <= vals[1])

    def op_number_morethanequal(self, vals, units, refs, flags):
        return OperationResult(vals[0] >= vals[1])

    def op_boolean_and(self, vals, units, refs, flags):
        return OperationResult(BooleansFeature.boolean(self, vals[0]) and BooleansFeature.boolean(self, vals[1]))

    def op_boolean_or(self, vals, units, refs, flags):
        return OperationResult(BooleansFeature.boolean(self, vals[0]) or BooleansFeature.boolean(self, vals[1]))

    def op_boolean_conditional(self, vals, units, refs, flags):
        if BooleansFeature.boolean(self, vals[0]):
            res = OperationResult(vals[1])
            res.set_unit(units[1])
            res.set_ref(refs[1])
            return res
        res = OperationResult(vals[2])
        res.set_unit(units[2])
        res.set_ref(refs[2])
        return res

    def boolean(self, val):
        if type(val) == bool:
            return val
        raise CalculatingException('Cannot cast to boolean: ' + repr(val))

    def number_bool(self, val):
        if isinstance(val, bool):
            if val:
                return Decimal(1), False
            else:
                return Decimal(0), False
        return None, None

    def validate_boolean(self, value, unit, ref):
        try:
            BooleansFeature.boolean(self, value)
            return True
        except Exception:
            return False
