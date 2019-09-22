#!/usr/bin/python3

from modularcalculator.features.state.assignment import VariableItem
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.operators import OperationResult, OperatorDefinition
from modularcalculator.features.feature import Feature


class AssignmentOperatorsFeature(Feature):

    def id():
        return 'state.assignmentoperators'

    def category():
        return 'State'

    def title():
        return 'Assignment Operators'

    def desc():
        return '++, += etc'

    def dependencies():
        return ['state.assignment', 'structure.operators']

    @classmethod
    def install(cls, calculator):
        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '++', 
            '', #TODO
            AssignmentOperatorsFeature.op_var_increment, 
            1, 
            0, 
            ['variable']))
        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '--', 
            '', #TODO
            AssignmentOperatorsFeature.op_var_decrement, 
            1, 
            0, 
            ['variable']))
        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '+=', 
            '', #TODO
            AssignmentOperatorsFeature.op_var_add, 
            1, 
            1, 
            ['variable', 'number']), 
        {'units_normalise': False})
        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '-=', 
            '', #TODO
            AssignmentOperatorsFeature.op_var_subtract, 
            1, 
            1, 
            ['variable', 'number']), 
        {'units_normalise': False})
        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '*=', 
            '', #TODO
            AssignmentOperatorsFeature.op_var_multiply, 
            1, 
            1, 
            ['variable', 'number']), 
        {'units_normalise': False})
        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '/=', 
            '', #TODO
            AssignmentOperatorsFeature.op_var_divide, 
            1, 
            1, 
            ['variable', 'number']), 
        {'units_normalise': False})
        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '^=', 
            '', #TODO
            AssignmentOperatorsFeature.op_var_power, 
            1, 
            1, 
            ['variable', 'number']), 
        {'units_normalise': False})
        calculator.add_op(OperatorDefinition(
            'Assignment', 
            '%=', 
            '', #TODO
            AssignmentOperatorsFeature.op_var_modulus, 
            1, 
            1, 
            ['variable', 'number']), 
        {'units_normalise': False})
        calculator.add_op(OperatorDefinition(
            'Assignment', 
            r'\=', 
            '', #TODO
            AssignmentOperatorsFeature.op_var_integer_divide, 
            1, 
            1, 
            ['variable', 'number']), 
        {'units_normalise': False})

    def op_var_increment(self, vals, units, refs, flags):
        return AssignmentOperatorsFeature.assignment_operator(self, '+', [vals[0], Decimal('1')], [units[0], None], [refs[0], None], flags)

    def op_var_decrement(self, vals, units, refs, flags):
        return AssignmentOperatorsFeature.assignment_operator(self, '-', [vals[0], Decimal('1')], [units[0], None], [refs[0], None], flags)

    def op_var_add(self, vals, units, refs, flags):
        return AssignmentOperatorsFeature.assignment_operator(self, '+', vals, units, refs, flags)

    def op_var_subtract(self, vals, units, refs, flags):
        return AssignmentOperatorsFeature.assignment_operator(self, '-', vals, units, refs, flags)

    def op_var_multiply(self, vals, units, refs, flags):
        return AssignmentOperatorsFeature.assignment_operator(self, '*', vals, units, refs, flags)

    def op_var_divide(self, vals, units, refs, flags):
        return AssignmentOperatorsFeature.assignment_operator(self, '/', vals, units, refs, flags)

    def op_var_power(self, vals, units, refs, flags):
        return AssignmentOperatorsFeature.assignment_operator(self, '^', vals, units, refs, flags)

    def op_var_modulus(self, vals, units, refs, flags):
        return AssignmentOperatorsFeature.assignment_operator(self, '%', vals, units, refs, flags)

    def op_var_integer_divide(self, vals, units, refs, flags):
        return AssignmentOperatorsFeature.assignment_operator(self, '\\', vals, units, refs, flags)

    def assignment_operator(self, sym, vals, units, refs, flags):
        if isinstance(refs[0], VariableItem):
            if 'stateless' not in flags.keys() or not flags['stateless']:
                varname = refs[0].var
                var = self.vars[varname]
                op = self.ops_list[sym]
                op_result = op.call(self, [OperandResult(var[0], var[1], None), OperandResult(vals[1], units[1], refs[1])], flags)
                self.vars[varname] = (op_result.value, op_result.unit)
            res = OperationResult(vals[1])
            res.set_unit(units[1])
            return res
        else:
            raise ExecutionException("Expecting variable, received".format(refs[0].desc()))
