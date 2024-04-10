#!/usr/bin/python3

from modularcalculator.objects.api import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.operators import *
from modularcalculator.features.feature import Feature
from modularcalculator.features.structure.functions import *

import re
import os.path


class FunctionPointersFeature(Feature):

    def id():
        return 'structure.functionpointers'

    def category():
        return 'Structure'

    def title():
        return 'Pointers to Functions'

    def desc():
        return 'Enables a variable to contain a reference to a function'

    def dependencies():
        return ['state.assignment', 'structure.functions']

    def default_options():
        return {
            'Symbol' : '@'
        }

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('function_pointer', FunctionPointersFeature.parse_function_pointer)
        calculator.function_pointer_handlers = []

        calculator.feature_options['structure.functionpointers'] = cls.default_options()

    def parse_function_pointer(self, expr, i, items, flags):
        symbol = self.feature_options['structure.functionpointers']['Symbol']
        func_pointer_invoke_regex = re.compile(re.escape(symbol) + r'([a-zA-Z_][a-zA-Z0-9_]*)\(')

        next = expr[i:]
        func_pointer_match = func_pointer_invoke_regex.match(next)
        if func_pointer_match:
            func_pointer_name = func_pointer_match.group(1)

            i = len(func_pointer_name) + 1 + len(symbol)
            return_flags = {}
            args = []
            func_items = [FunctionPointerNameItem(symbol + func_pointer_name), FunctionStartItem()]
            while 'end_func' not in return_flags and i < len(next):
                try:
                    inner_items, length, return_flags = self.parse(next[i:], {'func': func_pointer_name, 'ignore_terminators': True})
                    inner_items = inner_items[0]
                    i += length + 1
                    if len(inner_items) > 0:
                        args.append(inner_items)
                        func_items.extend(inner_items)
                    if 'end_func' in return_flags:
                        func_items.append(FunctionEndItem())
                    else:
                        func_items.append(FunctionParamItem())
                except ParsingException as err:
                    newitems = func_items + err.statements[0]
                    err.statements = [newitems]
                    raise ParseException(err.message, [FunctionItem(err.truncate(next), newitems, self, func_pointer_name, [])], err.next)
            if 'end_func' not in return_flags:
                raise ParseException('Function missing close symbol', [], next)
            return [FunctionPointerItem(next[0:i], func_items, self, func_pointer_name, args)], i, None
        return None, None, None


class FunctionPointerItem(RecursiveOperandItem):

    def __init__(self, text, items, calculator, name, args):
        super().__init__(text, items, calculator)
        self.name = name
        self.args = args

    def desc(self):
        return 'function_pointer'

    def category(self):
        return 'function'

    def value(self, flags):
        if self.name not in self.calculator.vars:
            raise ExecuteException("Variable {} not found".format(self.name), [self], '', True)

        # Function pointer
        ref = self.calculator.vars[self.name][0]

        # Execute the items for each argument, put the results in a list of inputs
        inputs = []
        itemsi = 2
        for i, arg in enumerate(self.args):
            old_itemsi = itemsi
            try:
                argresult = self.calculator.execute(arg, flags)
                itemsi += len(arg) + 1
                inputs.append(argresult)
            except ExecuteException as err:
                self.items = self.items[0:itemsi]
                self.items.extend(err.items)
                err.items = self.items
                self.text = err.truncate(self.text)
                self.truncated = True
                raise ExecuteException(err.message, [self], err.next, True)
            if isinstance(argresult.value, Exception):
                err = argresult.value
                itemsi = old_itemsi
                self.items = self.items[0:itemsi]
                self.items.extend(err.items)
                err.items = self.items
                self.text = err.truncate(self.text)
                self.truncated = True
                raise ExecuteException(err.message, [self], err.next, True)

        for handler in self.calculator.function_pointer_handlers:
            if handler.should_handle(ref):
                try:
                    func = handler.handle(self.calculator, ref)
                    return func.call(self.calculator, inputs, flags)
                except ExecuteException as err:
                    self.items = []
                    self.text = ''
                    raise ExecuteException(err.message, [self], self.text, True)

        self.items = []
        old_text = self.text
        self.text = ''
        raise ExecuteException("No function pointer handler found for {}".format(old_text), [self], self.text, True)

    def result(self, flags):
        return self.value(flags)

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.name = self.name
        copy.args = self.args.copy()
        return copy


class FunctionPointerNameItem(NonFunctionalItem):

    def __init__(self, name):
        super().__init__(name)

    def desc(self):
        return 'function_pointer_name'

    def category(self):
        return 'function'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy
