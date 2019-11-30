#!/usr/bin/python3

from modularcalculator.objects.api import *
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
        return ['state.assignment', 'structure.functions', 'strings.strings', 'structure.terminator']

    def default_options():
        return {
            'Symbol' : '@'
        }

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('ext_function', ExternalFunctionsFeature.parse_ext_function)

        calculator.feature_options['structure.externalfunctions'] = cls.default_options()

    def parse_ext_function(self, expr, i, items, flags):
        symbol = self.feature_options['structure.externalfunctions']['Symbol']
        ext_func_invoke_regex = re.compile(re.escape(symbol) + r'([a-zA-Z_][a-zA-Z0-9_]*)\(')
        
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
                    inner_items, length, return_flags = self.parse(next[i:], {'func': ext_func_name, 'ignore_terminators': True})
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
                    raise ParseException(err.message, [FunctionItem(err.truncate(next), newitems, self, ext_func_name, [])], err.next)
            if 'end_func' not in return_flags:
                raise ParseException('Function missing close symbol', [], next)
            return [ExternalFunctionItem(next[0:i], func_items, self, ext_func_name, args)], i, None
        return None, None, None


class ExternalFunctionItem(RecursiveOperandItem):

    input_line_regex = re.compile(r'^#INPUT((\s+\S+)+)')

    def __init__(self, text, items, calculator, name, args):
        super().__init__(text, items, calculator)
        self.name = name
        self.args = args
    
    def desc(self):
        return 'ext_function'

    def value(self, flags):
        if self.name not in self.calculator.vars:
            raise ExecuteException("Variable {} not found".format(self.name), [self], '', True)
        path = self.calculator.vars[self.name][0]
        path = os.path.expanduser(path)
        
        inputs = []
        itemsi = 2
        for i, arg in enumerate(self.args):
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

        try:
            fh = open(path, 'r')
            func_content = str.join("", fh.readlines())
        except:
            raise ExecuteException("Could not read file '{}'".format(path), [], None)
        inputs.append(OperandResult(func_content, None, None))

        func = FunctionDefinition(
            'EXTERNAL', 
            'external function', 
            path,
            [],
            ExternalFunctionItem.do_function)

        topline = func_content.split('\n', 1)[0]
        input_line_regex_match = self.input_line_regex.match(topline)
        if input_line_regex_match:
            i = 0
            for value_unit in input_line_regex_match.group(1).split():

                value = None
                unit = None
                power = None

                if ',' in value_unit:
                    value, unit = value_unit.split(',')
                else:
                    value, unit = value_unit, None

                if unit is not None and '^' in unit:
                    unit, power = unit.split('^')
                else:
                    unit, power = unit, 1

                func.add_value_restriction(i, i, [value])
                if unit is not None:
                    func.add_unit_restriction(i, i, [unit, power])
                i += 1

        return func.call(self.calculator, inputs, flags)

    def do_function(self, vals, units, refs, flags):
        func_content = vals.pop(-1)
        units.pop(-1)
        refs.pop(-1)

        backup_vars = self.vars
        self.vars = {}
        
        for i in range(0, len(vals)):
            self.vars["PARAM{}".format(i + 1)] = (vals[i], units[i])
        try:
            result = self.calculate(func_content)
        except Exception as err:
            self.vars = backup_vars
            raise err
        
        self.vars = backup_vars
        
        last_result = get_last_result(result.results)
        res = OperationResult(last_result.value)
        res.set_unit(last_result.unit)
        return res

    def result(self, flags):
        return self.value(flags)

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.name = self.name
        copy.args = self.args.copy()
        return copy


class ExternalFunctionNameItem(NonFunctionalItem):

    def __init__(self, name):
        super().__init__(name)

    def desc(self):
        return 'ext_function_name'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy
