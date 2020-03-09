#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.features.feature import Feature

import re


class ConstantsFeature(Feature):

    def id():
        return 'state.constants'

    def category():
        return 'State'

    def title():
        return 'Constants'

    def desc():
        return 'Base feature for constants'

    def dependencies():
        return []

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('constant', ConstantsFeature.parse_constant)

        calculator.constants = {}

    constant_regex = re.compile(r'([a-zA-Z]+)')

    def parse_constant(self, expr, i, items, flags):
        next = expr[i:]
        constant_match = ConstantsFeature.constant_regex.match(next)
        if (constant_match):
            constant = constant_match.group(1)
            if constant in self.constants.keys():
                return [ConstantItem(constant, self.constants[constant])], len(constant), None
        return None, None, None


class ConstantItem(OperandItem):

    def __init__(self, constant, valunit):
        super().__init__(constant)
        self.constant = constant
        if not isinstance(valunit, tuple):
            valunit = (valunit, None)
        self.val = valunit[0]
        self.unit = valunit[1]

    def desc(self):
        return 'constant'

    def value(self, flags):
        if self.unit is not None:
            return OperandResult(self.val, self.unit.copy(), self)
        return OperandResult(self.val, None, self)

    def result(self, flags):
        return self.value(flags)

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.constant = self.constant
        copy.val = self.val
        copy.unit = self.unit
        return copy
