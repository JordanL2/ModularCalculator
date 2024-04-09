#!/usr/bin/python3

from modularcalculator.objects.api import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.operators import *
from modularcalculator.features.feature import Feature
from modularcalculator.features.structure.functions import *

from functools import partial
import os.path
import re


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
        return ['structure.functionpointers', 'strings.strings', 'structure.terminator']

    @classmethod
    def install(cls, calculator):
        calculator.function_pointer_handlers.append(ExternalFunctionsPointerHandler)


class ExternalFunctionsPointerHandler:

    @staticmethod
    def should_handle(ref):
        return type(ref) == str

    @staticmethod
    def handle(calculator, ref):
        path = os.path.expanduser(ref)

        # Extract the content of the external function file, add to the end of the argument list
        try:
            with open(path, 'r') as fh:
                func_content = str.join("", fh.readlines())
        except:
            raise ExecuteException("Could not read file '{}'".format(path), [], None)

        # External function definition to execute
        func = FunctionDefinition(
            'EXTERNAL',
            'external function',
            path,
            [],
            partial(ExternalFunctionsPointerHandler.do_function, func_content))

        # Disable any kind of auto conversion of inputs
        func.units_normalise = False
        func.auto_convert_numerical_inputs = False
        func.auto_convert_numerical_result = False

        # If function content has a top line declaring the input type, parse it
        topline = func_content.split('\n', 1)[0]
        input_line_regex = re.compile(r'^' + calculator.feature_options['nonfunctional.comments']['Symbol'] + r'INPUT((\s+\S+)+)')
        input_line_regex_match = input_line_regex.match(topline)
        if input_line_regex_match:
            i = 0
            for value in input_line_regex_match.group(1).split():

                units = None
                power = None

                # If type has a colon, first part is value type, second is unit dimensions
                if ':' in value:
                    value, units_string = value.split(':')

                    # Multiple unit[^power] dimensions can be provided for an input, comma separated
                    units = []
                    for unit in units_string.split(','):
                        # If unit dimension has a power, parse it, otherwise power defaults to 1
                        if unit is not None and '^' in unit:
                            unit_unit, unit_power = unit.split('^')
                            units.append(unit_unit)
                            units.append(int(unit_power))
                        else:
                            units.append(unit)
                            units.append(1)
                else:
                    value, units = value, None

                # Apply value and unit restrictions to the function definition
                func.add_value_restriction(i, i, [value])
                if units is not None:
                    func.add_unit_restriction(i, i, units)
                i += 1

        return func

    @staticmethod
    def do_function(func_content, calculator, vals, units, refs, flags):
        # Back up the calculator state, then clear it
        backup_vars = calculator.vars
        calculator.vars = {}

        # For each input, set it in the calculator state as a variable called "PARAM" + n
        for i in range(0, len(vals)):
            calculator.vars["PARAM{}".format(i + 1)] = (vals[i], units[i])

        # Execute the function content
        try:
            result = calculator.calculate(func_content)
        except Exception as err:
            calculator.vars = backup_vars
            raise err

        # Restore calculator state
        calculator.vars = backup_vars

        # The last result of the function is the return value
        last_result = get_last_result(result.results)
        res = OperationResult(last_result.value)
        res.set_unit(last_result.unit)
        return res
