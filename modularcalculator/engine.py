#!/usr/bin/python3

from modularcalculator.objects.api import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.units import *
from modularcalculator.services.unitnormaliser import *

import time


class Engine:

    def __init__(self):
        self.parsers = []
        self.ops = []
        self.finalizers = []
        self.validators = { 'exception': { 'desc': 'exception', 'ref': Engine.validate_exception } }

        self.multiply_op = None
        self.divide_op = None
        self.implicit_multiply_op = None

        self.unit_normaliser = None
        self.unit_simplification = False
        self.unit_assignment_op = None
        self.unit_multiply_op = None
        self.unit_divide_op = None

    def setup(self):
        self.ops_list = dict([(sym, op) for prec in self.ops for sym, op in prec.items()])
        self.ops_symbols = [sym for prec in self.ops for sym in prec.keys()] + [sym for prec in self.ops for op in prec.values() for sym in op.linputs + op.rinputs if isinstance(sym, str)]

    def enable_units(self):
        self.unit_normaliser = UnitNormaliser(self)

    def unit_simplification_set(self, enabled):
        self.unit_simplification = enabled

    def unit_simplification_get(self):
        return self.unit_simplification

    def calculate(self, expr, flags=None):
        if flags is None:
            flags = {}

        response = CalculatorResponse()
        if len(expr) > 0:

            try:
                # Parse statements from expression
                statements, length, return_flags = self.parse(expr, flags)

                for i, items in enumerate(statements):
                    result = CalculatorResult(items_text(items), items)
                    result.set_timing('parse', return_flags['times'][i])

                    # Only execute statement if there are functional items in it
                    if len(functional_items(items)) > 0 and ('parse_only' not in flags or not flags['parse_only']):
                        try:
                            # Execute statement, time how long it takes
                            start_time = time.perf_counter()
                            answer = self.execute(items, flags)
                            if isinstance(answer.value, Exception):
                                raise answer.value
                            result.set_timing('exec', time.perf_counter() - start_time)

                            # Finalize the answer, time how long it takes
                            start_time = time.perf_counter()
                            final = self.finalize(answer)
                            result.set_timing('finalize', time.perf_counter() - start_time)
                            result.set_answer(final.value, final.unit)

                        except ExecuteException as err:
                            raise ExecutionException(err.message, statements[0:i] + [err.items], err.next, err.truncated)

                        except CalculatorException as err:
                            raise ExecutionException(err.message, statements[0:i] + [[]], None, False)

                    response.add_result(result)

                    if 'include_state' in flags and flags['include_state']:
                        result.set_state(self.vars.copy())

            except CalculatingException as err:
                err.set_response(response)
                raise err

        return response

    def parse(self, expr, flags):
        statements = [[]]
        i = 0
        lasti = 0
        start_time = time.perf_counter()
        times = []

        while(i < len(expr)):
            next = expr[i:]

            # Iterate through list of parsers, attempt to parse the next part of the expression with each one
            for parser in self.parsers:
                try:
                    items_found, length, return_flags = parser['ref'](self, expr, i, statements[-1], flags.copy())
                except ParseException as err:
                    statements[-1].extend(err.items)
                    raise ParsingException(err.message, statements, err.next)

                break_after_this = False
                if items_found is not None or (length is not None and length > 0):
                    # Items were found, or length was > 0, meaning we should advance though the expression
                    break_after_this = True
                    if items_found is not None:
                        # Add the items found to the current statement
                        statements[-1].extend(items_found)
                    if length is not None:
                        # Advance our position in the expression
                        i += length

                if return_flags is not None and 'end_statement' in return_flags:
                    # The current statement has been terminated, start a fresh one
                    return_flags = self.update_times(start_time, statements, times, return_flags)
                    start_time = time.perf_counter()
                    statements.append([])
                if return_flags is not None and 'end' in return_flags:
                    # All parsing has been terminated (for example, we're parsing an inner statement and hit a closing bracket)
                    return_flags = self.update_times(start_time, statements, times, return_flags)
                    return statements, i, return_flags

                # Since a parser returned something, we start from the list of parsers at the beginning next time
                if break_after_this:
                    break

            # If our position has not changed after going through the entire list of parsers, then we've hit something we cannot parse
            if i == lasti:
                raise ParsingException("Could not parse: {0}".format(next), statements, next)
            lasti = i

        self.update_times(start_time, statements, times, {})

        return statements, i, {'times': times}

    def update_times(self, start_time, statements, times, return_flags):
        if len(times) <= len(statements):
            times.append(0)
        times[len(statements) - 1] = time.perf_counter() - start_time
        if return_flags is None:
            return_flags = {}
        return_flags['times'] = times
        return return_flags

    def execute(self, items, flags):
        items = copy_items(items)
        original_items = items
        very_original_items = copy_items(items)
        # Strip out all non-functional items for now as they aren't relevant to the actual execution
        items = functional_items(items)
        try:
            if len(items) == 0:
                raise ExecuteException("Empty expression", [], None)

            # For each operand, evaluate them so we only have a flat list of actual values left, which can be passed into operators
            for i, item in enumerate(items):
                items[i] = self.execute_operand(items[i], original_items[0:i], flags)
                items[i]._INDEX = i

            while True:
                # Step through each precedence level of operators, so highest precedence ones are executed first
                for prec in self.ops:
                    # By default, we step through the items from left to right
                    item_order = range(0, len(items))
                    # Some operator precedence levels needs to evaluate items from right to left
                    if self.ops_list[list(prec)[0]].rtl:
                        item_order = reversed(item_order)

                    for i in item_order:
                        # Gather information about the current, previous, and next items
                        item = items[i]
                        item_is_unit = self.is_unit(item)
                        item_is_op = self.is_op(item)
                        prev_is_unit = (i > 0 and self.is_unit(items[i - 1]))
                        prev_is_op = (i > 0 and self.is_op(items[i - 1]))
                        next_is_unit = (i < len(items) - 1 and self.is_unit(items[i + 1]))

                        # Check if we can assign a unit to a value (a value is followed by a unit)
                        if self.unit_assignment_op is not None and self.unit_assignment_op in prec and item_is_unit and i > 0 and not prev_is_op and not prev_is_unit:
                            items = self.execute_operator(self.unit_assignment_op, items, i, 0, original_items, flags)
                            break
                        # Check if we can multiply two units together (two units are next to each other)
                        if self.unit_multiply_op is not None and self.unit_multiply_op in prec and item_is_unit and prev_is_unit:
                            items = self.execute_operator(self.unit_multiply_op, items, i, 0, original_items, flags)
                            break
                        # Check if we can divide one unit by another (unit / unit)
                        if self.unit_divide_op is not None and self.unit_divide_op in prec and item_is_op and item.op == self.divide_op and prev_is_unit and next_is_unit:
                            items = self.execute_operator(self.unit_divide_op, items, i, 1, original_items, flags)
                            break
                        # Check if we can implicitly multiply two values together (two values are next to each other)
                        if self.implicit_multiply_op is not None and self.implicit_multiply_op in prec and not item_is_op and not item_is_unit and i > 0 and not prev_is_op:
                            items = self.execute_operator(self.implicit_multiply_op, items, i, 0, original_items, flags)
                            break
                        # All other operators
                        if item_is_op and item.op in prec and item.op not in (self.unit_multiply_op, self.unit_divide_op, self.implicit_multiply_op) and (not prev_is_unit or item.op != self.divide_op or not next_is_unit):
                            items = self.execute_operator(item.op, items, i, 1, original_items, flags)
                            break
                    else:
                        # If we stepped though the item list without an operator in this precedence level being executed, we go onto the next level
                        continue
                    # Otherwise, we start from the first precedence level again
                    break
                else:
                    # If we went through all precedence levels without an operator being executed, we should stop
                    break

            if len(items) == 0:
                raise Exception("Ended up with no items: {0}".format(original_items))
            if len(items) > 1:
                item_index = items[0]._INDEX
                ops = [i for i in items if isinstance(i, OperatorItem)]
                if len(ops) > 0:
                    item_index = ops[0]._INDEX
                    raise ExecuteException("Could not execute operator: {0}".format(ops[0].text), original_items[0:item_index], None)
                raise ExecuteException("Not one item left: {0}".format([str(item) for item in items]), original_items[0:item_index], None)
            if not isinstance(items[0], OperandResult):
                raise ExecuteException("Not a value: \"{0}\"".format(str(items[0])), original_items[0:items[0]._INDEX], None)

            if isinstance(items[0].value, CalculateException):
                items[0].value = self.restore_non_functional_items(items[0].value, original_items, very_original_items)
            return items[0]
        except CalculateException as err:
            raise self.restore_non_functional_items(err, original_items, very_original_items)

    def is_unit(self, item):
        return isinstance(item, OperandResult) and isinstance(item.value, UnitPowerList)

    def is_op(self, item):
        return isinstance(item, OperatorItem)

    def execute_operand(self, item, previous_items, flags):
        if isinstance(item, OperandItem):
            if 'fake_execution' in flags:
                if self.is_unit(item):
                    return OperandResult(UnitPowerList(), None, None)
                return OperandResult(None, None, None)
            try:
                item = item.result(flags)
            except ExecuteException as err:
                err.items = previous_items + err.items
                return OperandResult(err, None, None)
            except CalculatorException as err:
                return OperandResult(ExecuteException(err.message, previous_items, item.text), None, None)
        return item

    def execute_operator(self, sym, items, i, opwidth, original_items, flags):
        op_item = None
        if opwidth == 1:
            # If opwidth is 0, then it's an invisible operator
            op_item = items[i]
        op = self.ops_list[sym]
        linputs = op.linputs
        rinputs = op.rinputs
        item_index = items[i]._INDEX
        previous_items = original_items[0:item_index]

        # Using operator's expected left and right inputs, make a list of expected and actual inputs for the operator
        input_start = min(i - len(linputs), i)
        if input_start < 0:
            raise ExecuteException("Missing left operands for operator {0}".format(sym), previous_items, sym)
        input_end = i + len(rinputs) + opwidth
        if input_end > len(items):
            raise ExecuteException("Missing right operands for operator {0}".format(sym), previous_items, sym)
        actual_items = [items[index] for index in list(range(input_start, i)) + list(range(i + opwidth, input_end))]
        expected_items = linputs + rinputs

        # Validate the actual inputs match the expected inputs
        inputs = []
        for index, this_item in enumerate(actual_items):
            expected_item = expected_items[index]
            if isinstance(expected_item, str):
                if str(this_item) != expected_item:
                    raise ExecuteException("Invalid symbol '{0}' for operator {1}".format(str(this_item), sym), original_items[0:this_item._INDEX], str(this_item))
            else:
                if not isinstance(this_item, OperandResult):
                    raise ExecuteException("Invalid input for operator {0} - '{1}'".format(sym, str(this_item)), previous_items, sym)
                inputs.append(this_item)

        if 'fake_execution' in flags:
            op_result = inputs[0]
            op_result._INDEX = item_index
        else:
            # Execute the operator code with the inputs
            try:
                op_result = op.call(self, inputs, flags)
                op_result._INDEX = item_index
            except CalculatorException as err:
                itemtext = None
                if op_item is not None:
                    itemtext = op_item.text
                new_err = ExecuteException(err.message, previous_items, itemtext)
                op_result = OperandResult(new_err, None, None)
                op_result._INDEX = item_index

        # Return the list of items, with the operator and its input replaced with the operator result
        return items[0:input_start] + [op_result] + items[input_end:]

    def restore_non_functional_items(self, err, original_items, very_original_items):
        exception_items = []
        functional_items = 0
        i = 0
        maxi = len(err.items)
        while i < len(original_items) and functional_items <= maxi:
            if err.truncated and functional_items < maxi:
                if functional_items < maxi - 1:
                    exception_items.append(very_original_items[i])
                else:
                    exception_items.append(original_items[i])
            if original_items[i].functional():
                functional_items += 1
            if not err.truncated and functional_items <= maxi:
                exception_items.append(very_original_items[i])
            i += 1
        err.items = exception_items
        return err

    def finalize(self, answer):
        if answer is None:
            return None
        if type(answer.value) == list:
            # If answer is an array, apply finalization to each element
            for i, ans in enumerate(answer.value):
                answer.value[i] = self.finalize(ans)
        else:
            if self.unit_normaliser is not None and self.unit_simplification and answer.unit is not None and not answer.unit.no_simplify:
                # Simplify the answer's unit
                answer.value, answer.unit = self.unit_normaliser.simplify_units(answer.value, answer.unit)
            for finalizer in self.finalizers:
                answer = finalizer['ref'](self, answer)
        return answer

    def validate_exception(self, value, unit, ref):
        return isinstance(value, Exception)
