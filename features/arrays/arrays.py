#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.exceptions import *
from modularcalculator.features.feature import Feature


class ArraysFeature(Feature):

    def id():
        return 'arrays.arrays'

    def category():
        return 'Arrays'

    def title():
        return 'Arrays'

    def desc():
        return 'Enables array type'

    def dependencies():
        return []

    def default_options():
        return {
            'Open': '[',
            'Range': '..',
            'Step': 'step',
            'Param': ',',
            'Close': ']',
        }

    @classmethod
    def install(cls, calculator):
        calculator.feature_options[cls.id()] = cls.default_options()

        calculator.add_parser('array', ArraysFeature.parse_array)
        calculator.add_parser('array_range', ArraysFeature.parse_array_range)
        calculator.add_parser('array_step', ArraysFeature.parse_array_step)
        calculator.add_parser('array_param', ArraysFeature.parse_array_param)
        calculator.add_parser('array_end', ArraysFeature.parse_array_end)

    def parse_array(self, expr, i, items, flags):
        next = expr[i:]
        symbol = self.feature_options['arrays.arrays']['Open']

        if len(next) >= len(symbol) and next[0:len(symbol)] == symbol:
            pass

        return None, None, None

    def parse_array_range(self, expr, i, items, flags):
        next = expr[i:]
        symbol = self.feature_options['arrays.arrays']['Range']

        if len(next) >= len(symbol) and next[0:len(symbol)] == symbol:
            pass

        return None, None, None

    def parse_array_step(self, expr, i, items, flags):
        next = expr[i:]
        symbol = self.feature_options['arrays.arrays']['Step']

        if len(next) >= len(symbol) and next[0:len(symbol)] == symbol:
            pass

        return None, None, None

    def parse_array_param(self, expr, i, items, flags):
        next = expr[i:]
        symbol = self.feature_options['arrays.arrays']['Param']

        if len(next) >= len(symbol) and next[0:len(symbol)] == symbol:
            pass

        return None, None, None

    def parse_array_end(self, expr, i, items, flags):
        next = expr[i:]
        symbol = self.feature_options['arrays.arrays']['Close']

        if len(next) >= len(symbol) and next[0:len(symbol)] == symbol:
            pass

        return None, None, None


class ArrayItem(RecursiveOperandItem):

    def __init__(self, text, elements):
        super().__init__(text)
        self.elements = elements

    def desc(self):
        return 'array'

    def value(self, flags):
        array = []

        for i, element in enumerate(self.elements):
            array.extend(element.value(flags))

        return array

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.elements = self.elements
        return copy


class ArrayElement():

    def __init__(self, element, end_element=None, step=None):
        self.element = element
        self.end_element = end_element
        self.step_val = step_val

    def value(self, flags):
        element_result = self.calculator.execute(self.element, flags)

        end_element_result = None
        if self.end_element:
            end_element_result = val = self.calculator.execute(self.end_element, flags)
        else:
            return [element_result]

        step_result = Decimal('1')
        if self.step:
            step_result = val = self.calculator.execute(self.step, flags)

        return [x for x in range(element_result, end_element_result + step_result, step_result)]
