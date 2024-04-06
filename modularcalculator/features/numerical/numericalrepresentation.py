#!/usr/bin/python3

from modularcalculator.features.feature import Feature
from modularcalculator.objects.items import *
from modularcalculator.objects.operators import OperationResult, OperatorDefinition

class NumericalRepresentationFeature(Feature):

    def id():
        return 'numerical.numericalrepresentation'

    def category():
        return 'Numerical'

    def title():
        return 'Numerical Representations'

    def desc():
        return 'Ability to represent numbers in different forms'

    def dependencies():
        return []

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('numericalrepresentation', NumericalRepresentationFeature.parse_numericalrepresentation)
        calculator.validators['numericalrepresentation'] = NumericalRepresentationFeature.validate_numericalrepresentation

        op_as_def = OperatorDefinition(
            'Numerical',
            'as',
            'Change the numerical representation of a number',
            NumericalRepresentationFeature.op_as,
            1,
            1,
            ['number', 'numericalrepresentation'])
        op_as_def.auto_convert_numerical_result = False
        calculator.add_op(op_as_def)

    def parse_numericalrepresentation(self, expr, i, items, flags):
        next = expr[i:]

        for numrep in self.number_casters:
            numrep_name = numrep.name()
            if next.startswith(numrep_name) and (len(next) == len(numrep_name) or not next[len(numrep_name)].isalpha()):
                return [NumericalRepresentationItem(numrep_name)], len(numrep_name), None

        return None, None, None

    def validate_numericalrepresentation(self, value, unit, ref):
        return value in self.number_casters_dict.keys()

    def op_as(self, vals, units, refs, flags):
        numrep = vals[1]
        if numrep not in self.number_casters_dict.keys():
            raise CalculatorException("Could not find numerical representation '{}'".format(numrep))
        caster = self.number_casters_dict[numrep]
        val = caster.convert_to(self, vals[0])
        return OperationResult(val)


class NumericalRepresentationItem(OperandItem):

    def __init__(self, text):
        super().__init__(text)

    def desc(self):
        return 'numericalrepresentation'

    def value(self, flags):
        return self.text

    def result(self, flags):
        return OperandResult(self.value(flags), None, self)

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy
