#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.operators import *
from modularcalculator.features.feature import Feature
from modularcalculator.features.structure.functions import *

import re
import os.path


class ExternalFunctionsFeature(Feature):

    def id():
        return 'structure.externalfunctions'

    def category():
        return 'Structure'

    def title():
        return 'User Defined Functions'

    def desc():
        return 'Enables functions defined by the user'

    def dependencies():
        return ['state.assignment', 'structure.functions']

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('ext_function', ExternalFunctionsFeature.parse_ext_function)

        calculator.feature_options['structure.externalfunctions'] = {
            'symbol' : '@'
        }

    def parse_ext_function(self, expr, i, items, flags):
        symbol = self.feature_options['structure.externalfunctions']['symbol']
        ext_func_invoke_regex = re.compile(symbol + r'([a-zA-Z_]+)\(')
        
        next = expr[i:]
        ext_func_match = ext_func_invoke_regex.match(next)
        if ext_func_match:
            ext_func_name = ext_func_match.group(1)

            i = len(ext_func_name) + 1 + len(symbol)
            return_flags = {}
            args = []
            func_items = [ExternalFunctionNameItem(symbol + ext_func_name), FunctionStartItem()]
            while 'end_func' not in return_flags and i < len(next):
                try:
                    inner_items, length, return_flags = self.parse(next[i:], {'func': ext_func_name})
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
                    raise ParsingException(err.message, [FunctionItem(err.truncate(next), newitems, self, ext_func_name, [])], err.next)
            if 'end_func' not in return_flags:
                raise ParsingException('Function missing close symbol', [], next)
            return [ExternalFunctionItem(next[0:i], func_items, self, ext_func_name, args)], i, None
        return None, None, None


class ExternalFunctionItem(RecursiveOperandItem):

    def __init__(self, text, items, calculator, name, args):
        super().__init__(text, items, calculator)
        self.name = name
        self.args = args
    
    def desc(self):
        return 'ext_function'

    def value(self, flags):
        if self.name not in self.calculator.vars:
            raise ExecutionException("Variable {} not found".format(self.name), [self], '', True)
        path = self.calculator.vars[self.name][0]
        path = os.path.expanduser(path)
        
        inputs = []
        itemsi = 2
        for i, arg in enumerate(self.args):
            try:
                argresult = self.calculator.execute(arg, flags)
                itemsi += len(arg) + 1
                inputs.append(argresult)
            except ExecutionException as err:
                self.items = self.items[0:itemsi]
                self.items.extend(err.items)
                err.items = self.items
                self.text = err.truncate(self.text)
                raise ExecutionException(err.message, [self], err.next, True)

        try:
            fh = open(path, 'r')
            func_content = str.join("", fh.readlines())
        except:
            raise ExecutionException("Could not read file '{}'".format(path), [], None)

        backup_vars = self.calculator.vars

        self.calculator.vars = {}
        for i, var in enumerate(inputs):
            self.calculator.vars["PARAM{}".format(i)] = (var.value, var.unit)
        try:
            result = self.calculator.calculate(func_content)
        except ExecutionException as err:
            self.calculator.vars = backup_vars
            raise ExecutionException("Could not execute function '{}'".format(self.name), [], None)
        except Exception as err:
            self.calculator.vars = backup_vars
            raise err
        final_result = result.results[-1]

        self.calculator.vars = backup_vars

        return OperandResult(final_result.value, final_result.unit, None)

    def result(self, flags):
        return self.value(flags)


class ExternalFunctionNameItem(NonFunctionalItem):

    def __init__(self, name):
        super().__init__(name)

    def desc(self):
        return 'ext_function_name'
