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
        start_symbol = self.feature_options['arrays.arrays']['Open']
        range_symbol = self.feature_options['arrays.arrays']['Range']
        step_symbol = self.feature_options['arrays.arrays']['Step']
        param_symbol = self.feature_options['arrays.arrays']['Param']
        end_symbol = self.feature_options['arrays.arrays']['Close']

        if len(next) >= len(start_symbol) and next[0:len(start_symbol)] == start_symbol:
            i = len(start_symbol)
            elements = []
            return_flags = {}
            array_items = [ArrayStartItem(start_symbol)]
            while 'end_array' not in return_flags and i < len(next):
                try:
                    items, length, return_flags = self.parse(next[i:], {'array': True, 'ignore_terminators': True})
                    items = items[0]
                    array_items += items
                    if len(items) > 0:
                        i += length
                        element = ArrayElement(items)

                        if 'array_range' in return_flags:
                            i += len(range_symbol)
                            array_items += [ArrayRangeItem(range_symbol)]
                            items, length, return_flags = self.parse(next[i:], {'array': True, 'ignore_terminators': True})
                            items = items[0]
                            array_items += items
                            if len(items) > 0:
                                i += length
                                element.end_element = items

                                if 'array_step' in return_flags:
                                    i += len(step_symbol)
                                    array_items += [ArrayStepItem(step_symbol)]
                                    items, length, return_flags = self.parse(next[i:], {'array': True, 'ignore_terminators': True})
                                    items = items[0]
                                    array_items += items
                                    if len(items) > 0:
                                        i += length
                                        element.step = items

                        elements.append(element)

                except ParsingException as err:
                    newitems = array_items.copy()
                    newitems.extend(err.statements[0])
                    err.statements = [newitems]
                    raise ParseException(err.message, [ArrayItem(err.truncate(next), newitems, self, elements)], err.next)

                if 'array_param' in return_flags:
                    i += len(param_symbol)
                    array_items += [ArrayParamItem(param_symbol)]

            if 'end_array' in return_flags:
                i += len(end_symbol)
                array_items += [ArrayEndItem(end_symbol)]
                return [ArrayItem(next[0:i], array_items, self, elements)], i, None
            else:
                raise ParseException('Array missing close symbol', [], next)

        return None, None, None

    def parse_array_range(self, expr, i, items, flags):
        next = expr[i:]
        symbol = self.feature_options['arrays.arrays']['Range']

        array = ('array' in flags.keys() and flags['array'])
        if array and len(next) >= len(symbol) and next[0:len(symbol)] == symbol:
            return None, None, {'end': True, 'array_range': True}

        return None, None, None

    def parse_array_step(self, expr, i, items, flags):
        next = expr[i:]
        symbol = self.feature_options['arrays.arrays']['Step']

        array = ('array' in flags.keys() and flags['array'])
        if array and len(next) >= len(symbol) and next[0:len(symbol)] == symbol:
            return None, None, {'end': True, 'array_step': True}

        return None, None, None

    def parse_array_param(self, expr, i, items, flags):
        next = expr[i:]
        symbol = self.feature_options['arrays.arrays']['Param']

        array = ('array' in flags.keys() and flags['array'])
        if array and len(next) >= len(symbol) and next[0:len(symbol)] == symbol:
            return None, None, {'end': True, 'array_param': True}

        return None, None, None

    def parse_array_end(self, expr, i, items, flags):
        next = expr[i:]
        symbol = self.feature_options['arrays.arrays']['Close']

        array = ('array' in flags.keys() and flags['array'])
        if array and len(next) >= len(symbol) and next[0:len(symbol)] == symbol:
            return None, None, {'end': True, 'end_array': True}

        return None, None, None


class ArrayItem(RecursiveOperandItem):

    def __init__(self, text, items, calculator, elements):
        super().__init__(text, items, calculator)
        self.elements = elements
        self.calculator = calculator

    def desc(self):
        return 'array'

    def value(self, flags):
        array = []

        for i, element in enumerate(self.elements):
            array.extend(element.value(flags, self.calculator))

        return array

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.elements = self.elements
        return copy


class ArrayElement():

    def __init__(self, element, end_element=None, step=None):
        self.element = element
        self.end_element = end_element
        self.step = step

    def value(self, flags, calculator):
        element_result = calculator.execute(self.element, flags)

        end_element_result = None
        if self.end_element:
            end_element_result = val = calculator.execute(self.end_element, flags)
        else:
            return [element_result]

        step_result = Decimal('1')
        if self.step:
            step_result = val = calculator.execute(self.step, flags)
            step_result = step_result.value

        array = []
        n = element_result.value
        while n <= end_element_result.value:
            array.append(OperandResult(n, None, None))
            n += step_result
        return array


class ArrayStartItem(NonFunctionalItem):

    def __init__(self, text):
        super().__init__(text)

    def desc(self):
        return 'array_start'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy


class ArrayRangeItem(NonFunctionalItem):

    def __init__(self, text):
        super().__init__(text)

    def desc(self):
        return 'array_range'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy


class ArrayStepItem(NonFunctionalItem):

    def __init__(self, text):
        super().__init__(text)

    def desc(self):
        return 'array_step'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy


class ArrayParamItem(NonFunctionalItem):

    def __init__(self, text):
        super().__init__(text)

    def desc(self):
        return 'array_param'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy


class ArrayEndItem(NonFunctionalItem):

    def __init__(self, text):
        super().__init__(text)

    def desc(self):
        return 'array_end'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy
