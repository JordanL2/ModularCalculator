#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.operators import OperationResult, OperatorDefinition
from modularcalculator.features.feature import Feature

import re


class AssignmentFeature(Feature):

    def id():
        return 'state.assignment'

    def category():
        return 'State'

    def title():
        return 'Variable Assignment'

    def desc():
        return 'Eg: x=1'

    def dependencies():
        return ['structure.operators']

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('var', AssignmentFeature.parse_var)

        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '=', 
            'Assign a value to a variable',
            AssignmentFeature.op_var_set, 
            1, 
            1, 
            ['variable', [None, 'array']]), 
        {'units_normalise': False})
        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '||=', 
            'Assign a value to a variable only if the variable doesn\'t exist yet',
            AssignmentFeature.op_var_set_if_empty, 
            1, 
            1, 
            ['variable', [None, 'array']]), 
        {'units_normalise': False})

        #calculator.vars = {}

        calculator.validators['variable'] = AssignmentFeature.validate_variable

    var_regex = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)')

    def parse_var(self, expr, i, items, flags):
        next = expr[i:]
        var_match = AssignmentFeature.var_regex.match(next)
        if (var_match):
            var = var_match.group(1)
            return [VariableItem(var)], len(var), None
        return None, None, None

    def op_var_set(self, vals, units, refs, flags):
        if isinstance(refs[0], VariableItem):
            if 'stateless' not in flags.keys() or not flags['stateless']:
                self.vars[refs[0].var] = (vals[1], units[1])
            res = OperationResult(vals[1])
            res.set_unit(units[1])
            return res
        else:
            raise ExecuteException("Expecting variable, received".format(refs[0].desc()), [], None)

    def op_var_set_if_empty(self, vals, units, refs, flags):
        if isinstance(refs[0], VariableItem):
            if 'stateless' not in flags.keys() or not flags['stateless']:
                if refs[0].var not in self.vars:
                    self.vars[refs[0].var] = (vals[1], units[1])
            res = OperationResult(vals[1])
            res.set_unit(units[1])
            return res
        else:
            raise ExecuteException("Expecting variable, received".format(refs[0].desc()), [], None)

    def validate_variable(self, value, unit, ref):
        try:
            return isinstance(ref, VariableItem)
        except Exception:
            return False


class VariableItem(OperandItem):

    def __init__(self, var):
        super().__init__(var)
        self.var = var

    def desc(self):
        return 'variable'

    def value(self, flags, calculator):
        if self.var not in calculator.vars:
            return OperandResult(None, None, self)
        valueunit = calculator.vars[self.var]
        value = valueunit[0]
        unit = valueunit[1]
        if unit is not None:
            unit = unit.copy()
        return OperandResult(value, unit, self)

    def result(self, flags, calculator):
        return self.value(flags, calculator)

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.var = self.var
        return copy
