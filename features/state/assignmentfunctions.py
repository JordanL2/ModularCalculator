#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.operators import OperationResult
from modularcalculator.features.structure.functions import FunctionDefinition
from modularcalculator.features.state.assignment import VariableItem
from modularcalculator.features.feature import Feature


class AssignmentFunctionsFeature(Feature):

    def id():
        return 'state.assignmentfunctions'

    def category():
        return 'State'

    def title():
        return 'Assignment Functions'

    def desc():
        return 'reset, delete'

    def dependencies():
        return ['state.assignment', 'structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.funcs['reset'] = FunctionDefinition('Assignment', 'reset', AssignmentFunctionsFeature.func_reset, 0, 0)
        calculator.funcs['delete'] = FunctionDefinition('Assignment', 'delete', AssignmentFunctionsFeature.func_delete, 1, 1)

    def func_reset(self, vals, units, refs, flags):
        self.vars = {}
        return OperationResult(None)

    def func_delete(self, vals, units, refs, flags):
        if isinstance(refs[0], VariableItem):
            varname = refs[0].var
            del self.vars[varname]
            return OperationResult(None)
        else:
            raise ExecutionException("Expecting variable, received".format(refs[0].desc()))
