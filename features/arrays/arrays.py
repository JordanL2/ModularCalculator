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

        calculator.validators['array'] = ArraysFeature.validate_array

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

    def validate_array(self, value, unit, ref):
        return type(value) == list


class ArrayItem(RecursiveOperandItem):

    def __init__(self, text, items, calculator, elements):
        super().__init__(text, items, calculator)
        self.elements = elements
        self.calculator = calculator

    def desc(self):
        return 'array'

    def value(self, flags):
        array = []
        arr = [0]

        for i, element in enumerate(self.elements):
            try:
                arr[0] += 1
                array.extend(element.value(flags, self.calculator, arr))
            except ExecuteException as err:
                self.items = self.items[0:arr[0]]
                self.items.extend(err.items)
                err.items = self.items
                self.text = err.truncate(self.text)
                self.truncated = True
                raise ExecuteException(err.message, [self], err.next, True)

        return array

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.elements = self.elements
        copy.calculator = self.calculator
        return copy


class ArrayElement():

    def __init__(self, element, end_element=None, step=None):
        self.element = element
        self.end_element = end_element
        self.step = step

    def value(self, flags, calculator, arr):
        element_result = calculator.execute(self.element, flags)
        if isinstance(element_result.value, ExecuteException):
            raise element_result.value
        if self.end_element is not None and not isinstance(element_result.value, Decimal):
            raise ExecuteException("Arrays with range must be numerical", [], None)
        arr[0] += len(self.element)

        end_element_result = None
        if self.end_element is not None:
            arr[0] += 1
            end_element_result = calculator.execute(self.end_element, flags)
            if isinstance(end_element_result.value, ExecuteException):
                raise end_element_result.value
            if not isinstance(end_element_result.value, Decimal):
                raise ExecuteException("Arrays with range must be numerical", [], None)
            arr[0] += len(self.end_element)
        else:
            return [element_result]

        step_result = OperandResult(Decimal('1'), element_result.unit, None)
        if self.step is not None:
            arr[0] += 1
            step_result = calculator.execute(self.step, flags)
            if isinstance(step_result.value, ExecuteException):
                raise step_result.value
            if not isinstance(step_result.value, Decimal):
                raise ExecuteException("Arrays with range must be numerical", [], None)
            arr[0] += len(self.step)

        if element_result.unit is not None or end_element_result.unit is not None or step_result.unit is not None:
            if element_result.unit is None:
                raise ExecuteException("Arrays with range must have a consistent unit for the start, end and step components", [], None)
            for right_element in (end_element_result, step_result):
                if right_element.unit is None:
                    raise ExecuteException("Arrays with range must have a consistent unit for the start, end and step components", [], None)
                values, units, resultunit = calculator.unit_normaliser.normalise_inputs([element_result.value, right_element.value], [element_result.unit, right_element.unit], True, False)
                right_element.value = values[1]
                right_element.unit = units[1]

        array = []
        n = element_result.value
        while n <= end_element_result.value:
            array.append(OperandResult(n, element_result.unit, None))
            n += step_result.value
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
