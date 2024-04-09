#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.exceptions import *
from modularcalculator.engine import *
from modularcalculator.features.feature import Feature
from modularcalculator.features.structure.functions import *

from functools import partial


class InlineFunctionsFeature(Feature):

    def id():
        return 'structure.inlinefunctions'

    def category():
        return 'Structure'

    def title():
        return 'Inline Functions'

    def desc():
        return 'Define a function inline and repeatedly execute it'

    def dependencies():
        return ['structure.functionpointers', 'structure.terminator']

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('inline_function', InlineFunctionsFeature.parse_inline_function)
        calculator.add_parser('inline_function_end', InlineFunctionsFeature.parse_inline_function_end)
        calculator.function_pointer_handlers.append(InlineFunctionsPointerHandler)

    def parse_inline_function(self, expr, i, items, flags):
        next = expr[i:]
        if next.startswith('{'):
            flags['inline_function'] = True
            inner_items, length, return_flags = None, None, None
            try:
                inner_items, length, return_flags = self.parse(next[1:], flags)
                inner_items = [ii for i in inner_items for ii in i]
            except ParsingException as err:
                err.statements[0].insert(0, InlineFunctionStartItem())
                raise ParseException(err.message, [InlineFunctionItem(err.truncate(next), [i for s in err.statements for i in s], self)], err.next, True)
            inner_items.insert(0, InlineFunctionStartItem())
            if 'end_inline_function' not in return_flags:
                raise ParseException('Inline function missing close symbol', [], next)
            return [InlineFunctionItem(next[0:length + 2], inner_items, self)], length + 2, None
        return None, None, None

    def parse_inline_function_end(self, expr, i, items, flags):
        next = expr[i:]
        inner = ('inline_function' in flags.keys() and flags['inline_function'])
        if next.startswith('}'):
            if (inner):
                return [InlineFunctionEndItem()], None, {'end': True, 'end_inline_function': True}
            raise ParseException('Unexpected inline function close symbol found', [], next)
        return None, None, None


class InlineFunctionItem(RecursiveOperandItem):

    def __init__(self, text, items, calculator):
        super().__init__(text, items, calculator)

    def desc(self):
        return 'inline_function'

    def category(self):
        return 'structural'

    def value(self, flags):
        return OperandResult(self, None, None)

    def result(self, flags):
        return self.value(flags)

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy


class InlineFunctionStartItem(NonFunctionalItem):

    def __init__(self):
        super().__init__('{')

    def desc(self):
        return 'inline_function_start'

    def category(self):
        return 'structural'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy


class InlineFunctionEndItem(NonFunctionalItem):

    def __init__(self):
        super().__init__('}')

    def desc(self):
        return 'inline_function_end'

    def category(self):
        return 'structural'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy


class InlineFunctionsPointerHandler:

    @staticmethod
    def should_handle(ref):
        return isinstance(ref, InlineFunctionItem)

    @staticmethod
    def handle(calculator, ref):
        # Inline function definition to execute
        func = FunctionDefinition(
            'INLINE',
            'inline function',
            '',
            [],
            partial(InlineFunctionsPointerHandler.do_function, ref))

        # Disable any kind of auto conversion of inputs
        func.units_normalise = False
        func.auto_convert_numerical_inputs = False
        func.auto_convert_numerical_result = False

        return func

    @staticmethod
    def do_function(ref, calculator, vals, units, refs, flags):
        # Back up the calculator state
        backup_vars = dict(calculator.vars)

        # For each input, set it in the calculator state as a variable called "PARAM" + n
        for i in range(0, len(vals)):
            calculator.vars["PARAM{}".format(i + 1)] = (vals[i], units[i])

        try:
            statement_items = []
            val = None
            for item in ref.items:
                if item.desc() == 'terminator':
                    if len(functional_items(statement_items)) > 0:
                        val = calculator.execute(statement_items, flags.copy())
                    statement_items = []
                else:
                    statement_items.append(item)
            if len(functional_items(statement_items)) > 0:
                val = calculator.execute(statement_items, flags.copy())
            if isinstance(val.value, Exception):
                calculator.vars = backup_vars
                raise val.value

            # Restore calculator state
            calculator.vars = backup_vars

            res = OperationResult(val.value)
            res.set_unit(val.unit)
            return res
        except ExecuteException as err:
            calculator.vars = backup_vars
            raise err
