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
        calculator.add_validator('numericalrepresentation', 'number type', NumericalRepresentationFeature.validate_numericalrepresentation)

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

        for numrep in self.number_types.keys():
            if next.startswith(numrep) and (len(next) == len(numrep) or not next[len(numrep)].isalpha()):
                return [NumericalRepresentationItem(numrep)], len(numrep), None

        return None, None, None

    def validate_numericalrepresentation(self, value, unit, ref):
        return isinstance(value, NumericalRepresentationValue) and value.name() in self.number_types.keys()

    def op_as(self, vals, units, refs, flags):
        numrep = vals[1]
        numrep = numrep.name()
        if numrep not in self.number_types.keys():
            raise CalculatorException("Could not find numerical representation '{}'".format(numrep))
        number_type = self.number_types[numrep]
        val = number_type.convert_to(self, vals[0])
        res = OperationResult(val)
        if units[0] is not None:
            res.set_unit(units[0])
        return res


class NumericalRepresentationItem(OperandItem):

    def __init__(self, text):
        super().__init__(text)

    def desc(self):
        return 'numericalrepresentation'

    def category(self):
        return 'special'

    def value(self, flags):
        return NumericalRepresentationValue(self.text)

    def result(self, flags):
        return OperandResult(self.value(flags), None, self)

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy


class NumericalRepresentationValue(ObjectValue):

    def __init__(self, text):
        super().__init__('numericalrepresentation', text, 'special')
