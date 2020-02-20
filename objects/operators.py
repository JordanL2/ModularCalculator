#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.exceptions import *

import re


class OperationResult:

    def __init__(self, value):
        self.unit_override = False
        self.ref_override = False
        self.set_value(value)

    def set_value(self, value):
        self.value = value

    def set_unit(self, unit):
        self.unit = unit
        self.unit_override = True

    def set_ref(self, ref):
        self.ref = ref
        self.ref_override = True


class Operation:

    validator_type = re.compile(r'(.+)\[(.+)\]')

    def __init__(self, category, name, description, syntax, ref, minparams=None, maxparams=None, objtypes=None):
        self.category = category
        self.name = name
        self.description = description
        self.syntax = syntax
        self.ref = ref

        self.minparams = minparams
        self.maxparams = maxparams
        self.value_restrictions = []
        self.unit_restrictions = []
        if objtypes is not None:
            self.add_value_restriction(0, None, objtypes)
        
        self.units_relative = False
        self.units_multi = False
        self.units_normalise = True

        self.inputs_can_be_exceptions = False
        self.auto_convert_numerical_inputs = True
        self.auto_convert_numerical_result = True

    def add_value_restriction(self, fromparam, toparam, objtypes):
        if objtypes is not None:
            if not isinstance(objtypes, list):
                objtypes = [objtypes]
            self.value_restrictions.append({'fromparam': fromparam, 'toparam': toparam, 'objtypes': objtypes})

    def add_unit_restriction(self, fromparam, toparam, dimensions):
        self.unit_restrictions.append({'fromparam': fromparam, 'toparam': toparam, 'dimensions': dimensions})

    def call(self, calculator, inputs, flags):
        # Get a list of the indices of any inputs that are arrays, that aren't declared can be arrays
        array_inputs = []
        for i, inp in enumerate(inputs):
            if type(inp.value) == list and not self.input_can_be_type(i, 'array') and not (inp.ref is not None and self.input_can_be_type(i, 'variable')):
                array_inputs.append(i)

        if len(array_inputs) > 0:

            # If some inputs are arrays (and not meant to be) then call this operation once for each element in the arrays,
            # putting the results into an array. All array inputs are iterated on each call to the operation.

            # Ensure all arrays are same length
            lengths = set()
            for i in array_inputs:
                lengths.add(len(inputs[i].value))
            if len(lengths) > 1:
                raise CalculatorException("All array inputs must all be same length")
            length = lengths.pop()

            # Call operation once for each element in the arrays
            results = []
            for i in range(0, length):
                input_row = []
                for ii, inp in enumerate(inputs):
                    if ii in array_inputs:
                        # This input is an array, get the element for this iteration
                        input_row.append(inp.value[i])
                    else:
                        # This input is not an array, simply use the fixed value
                        input_row.append(inp)
                res = self.call(calculator, input_row, flags)
                results.append(res)

            return OperandResult(results, None, None)

        else:

            # If any inputs are an exception, and this operation isn't flagged as allowing them as inputs, then throw the exception
            if not self.inputs_can_be_exceptions:
                for i in inputs:
                    if isinstance(i.value, Exception):
                        return i

            # Validate the values and units for this operation
            values = [i.value for i in inputs]
            units = [i.unit for i in inputs]
            refs = [i.ref for i in inputs]
            self.validate(calculator, values, units, refs)

            # Auto-convert all numbers into decimal numbers. Store the original number type of the first input, this will be used
            # for the result.
            result_value, result_unit, result_ref, num_type = None, None, None, None
            if self.auto_convert_numerical_inputs:
                values, num_type = self.convert_numbers(calculator, values)

            # Normalise the units of all inputs if units_normalise flag is set
            if len([i for i in range(0, len(values)) if not self.input_can_be_type(i, 'number') or not calculator.validate_number(values[i])]) == 0:

                # All inputs are numbers, normalise them to be all be the same unit
                if calculator.unit_normaliser is not None and self.units_normalise:
                    values, units, result_unit = calculator.unit_normaliser.normalise_inputs(values, units, self.units_multi, self.units_relative)

            else:

                # Go through each input and check if it's an array of numbers
                for i in range(0, len(values)):
                    if type(values[i]) == list and self.input_must_be_type(i, 'array', 'number'):

                        # This is an array of numbers

                        # Normalise all elements to be decimal
                        this_values = [v.value for v in values[i]]
                        for ii in range(0, len(values[i])):
                            num, num_type_res = calculator.number(this_values[ii])
                            this_values[ii] = num
                            if num_type is None:
                                # Take the first number type we get as the one we should use for the final result
                                num_type = num_type_res

                        # Normalise all elements to be the same unit
                        this_units = [v.unit for v in values[i]]
                        if calculator.unit_normaliser is not None and self.units_normalise:
                            this_values, this_units, result_unit = calculator.unit_normaliser.normalise_inputs(this_values, this_units, self.units_multi, self.units_relative)

                        values[i] = values[i].copy()
                        for ii in range(0, len(this_values)):
                            # Replace the element with a normalised version, saving the original value and unit
                            original_value = values[i][ii].value
                            original_unit = values[i][ii].unit
                            values[i][ii] = OperandResult(this_values[ii], this_units[ii], values[i][ii].ref)
                            values[i][ii].original_value = original_value
                            values[i][ii].original_unit = original_unit

            try:
                result = self.ref(calculator, values, units, refs, flags.copy())
                result_value = result.value

                # Convert the number type of the result
                if self.auto_convert_numerical_result and isinstance(result_value, Decimal) and num_type:
                    result_value = calculator.restore_number_type(result_value, num_type)

                # If result is an array, restore each element back to its original value and unit
                if type(result_value) == list:
                    for i, val in enumerate(result_value):
                        if hasattr(val, 'original_value'):
                            val.value = val.original_value
                        if hasattr(val, 'original_unit'):
                            val.unit = val.original_unit

                # If the operation wants to override the result's unit or ref, use the override value
                if result.unit_override:
                    result_unit = result.unit
                if result.ref_override:
                    result_ref = result.ref
                return OperandResult(result_value, result_unit, result_ref)

            except CalculatorException as err:
                raise err
            except Exception as err:
                raise CalculatorException("Could not execute {0}".format(self.name))

    def validate(self, calculator, values, units, refs):
        # Check if we're been given at least the minimum number of params
        if self.minparams is not None and len(values) < self.minparams:
            raise CalculatorException("{0} requires at least {1} params, only given {2}".format(self.name, self.minparams, len(values)))
        
        # Check we've not been given more than the maximum
        if self.maxparams is not None and len(values) > self.maxparams:
            raise CalculatorException("{0} requires at most {1} params, was given {2}".format(self.name, self.maxparams, len(values)))

        # Check all restrictions on input values are true
        for restriction in self.value_restrictions:
            fromparam = restriction['fromparam']
            toparam = len(values)
            if 'toparam' in restriction and restriction['toparam'] is not None:
                toparam = min(len(values), restriction['toparam'] + 1)
            # Cycle through each param this restriction applies to, and make sure it matches at least one allowed type
            objtypes = restriction['objtypes']
            for i in range(fromparam, toparam):
                for objtype in objtypes:
                    if self.validate_input(objtype, calculator, values[i], units[i], refs[i]):
                        break
                else:
                    raise CalculatorException("{0} parameter {1} must be of type(s) {2}".format(self.name, i + 1, str.join(', ', objtypes)))

        # Check all restrictions on input units are true
        for restriction in self.unit_restrictions:
            fromparam = restriction['fromparam']
            toparam = len(units)
            if 'toparam' in restriction and restriction['toparam'] is not None:
                toparam = min(len(units), restriction['toparam'] + 1)
            # Cycle through each param this restriction applies to, and make sure the unit matches the required dimensions
            dimensions = restriction['dimensions']
            for i in range(fromparam, toparam):
                if not calculator.unit_normaliser.check_unit_dimensions(units[i], dimensions):
                    try:
                        dimension_string = str.join(' ', ["{0}^{1}".format(dimensions[ii], str(dimensions[ii + 1])) for ii in range(0, len(dimensions), 2)])
                        raise CalculatorException("{0} parameter {1} must have unit dimensions: {2}".format(self.name, i + 1, dimension_string))
                    except CalculatorException as e:
                        raise e
                    except Exception as e:
                        raise CalculatorException("{0} parameter {1} has an invalid unit dimension definition".format(self.name, i + 1))

    def validate_input(self, obj_type, calculator, value, unit, ref):
        if obj_type is None:
            return True
        obj_type, obj_sub_type = self.parse_sub_type(obj_type)
        if obj_sub_type is not None:
            return calculator.validators[obj_type](calculator, value, unit, ref, obj_sub_type)
        if obj_type in calculator.validators and calculator.validators[obj_type](calculator, value, unit, ref):
            return True
        return False

    def parse_sub_type(self, obj_type):
        if obj_type is None:
            return (None, None)
        validator_type_match = self.validator_type.match(obj_type)
        if validator_type_match:
            obj_main_type = validator_type_match.group(1)
            obj_sub_type = validator_type_match.group(2)
            return (obj_main_type, obj_sub_type)
        return (obj_type, None)

    def input_can_be_type(self, i, obj_type, sub_type=None):
        for restriction in self.value_restrictions:
            fromparam = restriction['fromparam']
            toparam = None
            if 'toparam' in restriction and restriction['toparam'] is not None:
                toparam = restriction['toparam']
            objtypes = [self.parse_sub_type(o)[0] for o in restriction['objtypes']]
            subtypes = [self.parse_sub_type(o)[1] for o in restriction['objtypes']]
            if i >= fromparam and (toparam is None or i <= toparam) and obj_type in objtypes and (sub_type is None or sub_type in subtypes):
                return True
        return False

    def input_must_be_type(self, i, obj_type, sub_type=None):
        found_type = False
        for restriction in self.value_restrictions:
            fromparam = restriction['fromparam']
            toparam = None
            if 'toparam' in restriction and restriction['toparam'] is not None:
                toparam = restriction['toparam']
            objtypes = [self.parse_sub_type(o)[0] for o in restriction['objtypes']]
            subtypes = [self.parse_sub_type(o)[1] for o in restriction['objtypes']]
            if i >= fromparam and (toparam is None or i <= toparam):
                if obj_type in objtypes and len(objtypes) == 1 and (sub_type is None or (sub_type in subtypes and len(subtypes) == 1)):
                    found_type = True
                else:
                    return False
        return found_type

    def convert_numbers(self, calculator, values):
        new_values = values.copy()
        num_type = None

        # If an input is declared it can be a number, and it contains a numerical value, convert it to decimal
        for restriction in self.value_restrictions:
            objtypes = restriction['objtypes']
            if 'number' in objtypes:
                fromparam = restriction['fromparam']
                toparam = len(values)
                if 'toparam' in restriction and restriction['toparam'] is not None:
                    toparam = restriction['toparam'] + 1
                for i in range(fromparam, toparam):
                    if i < len(values):
                        # This input is declared it can be a number, check it contains a number
                        if calculator.validate_number(values[i]):
                            num, num_type_res = calculator.number(values[i])
                            new_values[i] = num
                            if num_type is None:
                                # Take the first number type we get as the one we should use for the final result
                                num_type = num_type_res

        return new_values, num_type


class OperatorDefinition(Operation):

    def __init__(self, category, name, description, ref, linputs, rinputs, objtypes):
        self.symbol = name
        
        if linputs == 0:
            linputs = []
        elif linputs == 1:
            linputs = [1]
        self.linputs = linputs
        
        if rinputs == 0:
            rinputs = []
        elif rinputs == 1:
            rinputs = [1]
        self.rinputs = rinputs

        num_of_params = len([i for i in linputs + rinputs if not isinstance(i, str)])

        c = 64
        syntax = []
        for l in linputs + [name] + rinputs:
            if l == 1:
                c += 1
                syntax.append(chr(c))
            else:
                syntax.append(l)

        if isinstance(objtypes, list):
            if len(objtypes) != num_of_params:
                raise Exception("List of input allowed types must be same length as number of parameters")
            super().__init__(category, "Operator " + name, description, syntax, ref, num_of_params, num_of_params)
            for i, objtype in enumerate(objtypes):
                self.add_value_restriction(i, i, objtype)
        else:
            super().__init__(category, "Operator " + name, description, syntax, ref, num_of_params, num_of_params, objtypes)

        self.rtl = False
        self.hidden = False
