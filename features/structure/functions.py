#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.operators import *
from modularcalculator.features.feature import Feature

import re


class FunctionsFeature(Feature):

    def id():
        return 'structure.functions'

    def category():
        return 'Structure'

    def title():
        return 'Functions'

    def desc():
        return 'Enables functions'

    def dependencies():
        return []

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('function', FunctionsFeature.parse_function)
        calculator.add_parser('function_param', FunctionsFeature.parse_function_param)
        calculator.add_parser('function_end', FunctionsFeature.parse_end_function)

        calculator.funcs = {}

    func_regex = re.compile(r'([a-zA-Z_]+)\(')

    def parse_function(self, expr, i, items, flags):
        next = expr[i:]
        func_match = FunctionsFeature.func_regex.match(next)
        if func_match:
            func = func_match.group(1)
            if func in self.funcs:
                i = len(func) + 1
                return_flags = {}
                args = []
                func_items = [FunctionNameItem(func), FunctionStartItem()]
                while 'end_func' not in return_flags and i < len(next):
                    try:
                        inner_items, length, return_flags = self.parse(next[i:], {'func': func, 'ignore_terminators': True})
                        i += length + 1
                        if len(inner_items) > 0:
                            args.append(inner_items)
                            func_items.extend(inner_items)
                        if 'end_func' in return_flags:
                            func_items.append(FunctionEndItem())
                        else:
                            func_items.append(FunctionParamItem())
                    except ParsingException as err:
                        newitems = func_items + err.items
                        err.items = newitems
                        raise ParsingException(err.message, [FunctionItem(err.truncate(next), newitems, self, func, [])], err.next)
                if 'end_func' not in return_flags:
                    raise ParsingException('Function missing close symbol', [], next)
                return [FunctionItem(next[0:i], func_items, self, func, args)], i, None
        return None, None, None

    def parse_function_param(self, expr, i, items, flags):
        next = expr[i:]
        inner = ('inner_expr' in flags.keys() and flags['inner_expr'])
        if next.startswith(',') and 'func' in flags.keys() and not inner:
            return None, None, {'end': True}
        return None, None, None

    def parse_end_function(self, expr, i, items, flags):
        next = expr[i:]
        inner = ('inner_expr' in flags.keys() and flags['inner_expr'])
        if next.startswith(')') and 'func' in flags.keys() and not inner:
            return None, None, {'end': True, 'end_func': True}
        return None, None, None


class FunctionDefinition(Operation):

    def __init__(self, category, name, description, syntax, ref, minparams=None, maxparams=None, objtypes=None):
        self.func = name
        super().__init__(category, "Function " + name, description, syntax, ref, minparams, maxparams, objtypes)


class FunctionItem(RecursiveOperandItem):

    def __init__(self, text, items, calculator, name, args):
        super().__init__(text, items, calculator)
        self.name = name
        self.args = args
    
    def desc(self):
        return 'function'

    def value(self, flags):
        func = self.calculator.funcs[self.name]
        inputs = []
        itemsi = 2
        for i, arg in enumerate(self.args):
            old_itemsi = itemsi
            try:
                argresult = self.calculator.execute(arg, flags)
                itemsi += len(arg) + 1
                inputs.append(argresult)
            except ExecutionException as err:
                self.items = self.items[0:itemsi]
                self.items.extend(err.items)
                err.items = self.items
                self.text = err.truncate(self.text)
                self.truncated = True
                raise ExecutionException(err.message, [self], err.next, True)
            if not func.inputs_can_be_exceptions and isinstance(argresult.value, Exception):
                err = argresult.value
                itemsi = old_itemsi
                self.items = self.items[0:itemsi]
                self.items.extend(err.items)
                err.items = self.items
                self.text = err.truncate(self.text)
                self.truncated = True
                raise ExecutionException(err.message, [self], err.next, True)
        return func.call(self.calculator, inputs, flags)

    def result(self, flags):
        return self.value(flags)


class FunctionNameItem(NonFunctionalItem):

    def __init__(self, name):
        super().__init__(name)

    def desc(self):
        return 'function_name'


class FunctionStartItem(NonFunctionalItem):

    def __init__(self):
        super().__init__('(')

    def desc(self):
        return 'function_start'


class FunctionParamItem(NonFunctionalItem):

    def __init__(self):
        super().__init__(',')

    def desc(self):
        return 'function_param'


class FunctionEndItem(NonFunctionalItem):

    def __init__(self):
        super().__init__(')')

    def desc(self):
        return 'function_end'
