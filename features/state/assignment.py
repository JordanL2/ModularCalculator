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
        return []

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('var', AssignmentFeature.parse_var)

        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '=', 
            '', #TODO
            AssignmentFeature.op_var_set, 
            1, 
            1, 
            ['variable', None]), 
        {'units_normalise': False})
        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '||=', 
            '', #TODO
            AssignmentFeature.op_var_set_if_empty, 
            1, 
            1, 
            ['variable', None]), 
        {'units_normalise': False})

        calculator.vars = {}

        calculator.validators['variable'] = AssignmentFeature.validate_variable

    var_regex = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)')

    def parse_var(self, expr, i, items, flags):
        next = expr[i:]
        var_match = AssignmentFeature.var_regex.match(next)
        if (var_match):
            var = var_match.group(1)
            return [VariableItem(var, self)], len(var), None
        return None, None, None

    def op_var_set(self, vals, units, refs, flags):
        if isinstance(refs[0], VariableItem):
            if 'stateless' not in flags.keys() or not flags['stateless']:
                self.vars[refs[0].var] = (vals[1], units[1])
            res = OperationResult(vals[1])
            res.set_unit(units[1])
            return res
        else:
            raise ExecutionException("Expecting variable, received".format(refs[0].desc()))

    def op_var_set_if_empty(self, vals, units, refs, flags):
        if isinstance(refs[0], VariableItem):
            if 'stateless' not in flags.keys() or not flags['stateless']:
                if refs[0].var not in self.vars:
                    self.vars[refs[0].var] = (vals[1], units[1])
            res = OperationResult(vals[1])
            res.set_unit(units[1])
            return res
        else:
            raise ExecutionException("Expecting variable, received".format(refs[0].desc()))

    def validate_variable(self, value, unit, ref):
        try:
            return isinstance(ref, VariableItem)
        except Exception:
            return False


class VariableItem(OperandItem):

    def __init__(self, var, calculator):
        super().__init__(var)
        self.var = var
        self.calculator = calculator

    def desc(self):
        return 'variable'

    def value(self, flags):
        if self.var not in self.calculator.vars:
            return OperandResult(None, None, self)
        valueunit = self.calculator.vars[self.var]
        value = valueunit[0]
        unit = valueunit[1]
        if unit is not None:
            unit = unit.copy()
        return OperandResult(value, unit, self)

    def result(self, flags):
        return self.value(flags)
