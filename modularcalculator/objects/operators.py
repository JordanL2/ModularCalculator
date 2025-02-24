#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *

import re


class OperationResult:

    def __init__(self, value):
        self.unit_override = False
        self.ref_override = False
        self.set_value(value)

    def set_value(self, value):
        self.value = value
        return self

    def set_unit(self, unit):
        self.unit = unit
        self.unit_override = True
        return self

    def set_ref(self, ref):
        self.ref = ref
        self.ref_override = True
        return self


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
                try:
                    res = self.call(calculator, input_row, flags)
                except CalculatorException as err:
                    res = OperandResult(err, None, None)
                results.append(res)

            return OperandResult(results, None, None)

        elif (self.maxparams == 1 and self.input_must_be_type(0, 'array') and len(inputs) > 1):

            # Multiple inputs passed to a function that usually takes just one array input.
            # If one or more inputs are arrays:
            #   Step through all arrays, and pass each set of elements as individuals arrays to
            #   the function each time. Put all results into an array.
            # Else:
            #   Put all inputs into an array, pass to function, return result.

            # Ensure all arrays are same length
            lengths = set()
            for i in range(0, len(inputs)):
                if type(inputs[i].value) == list:
                    lengths.add(len(inputs[i].value))
            if len(lengths) > 1:
                raise CalculatorException("All array inputs must all be same length")
            length = 1
            array_inputs = False
            if len(lengths) > 0:
                length = lengths.pop()
                array_inputs = True

            # Call operation once for each element in the arrays
            results = []
            for i in range(0, length):
                input_row = []
                for ii, inp in enumerate(inputs):
                    if type(inp.value) == list:
                        # This input is an array, get the element for this iteration
                        input_row.append(inp.value[i])
                    else:
                        # This input is not an array, simply use the fixed value
                        input_row.append(inp)
                res = self.call(calculator, [OperandResult(input_row, None, None)], flags)
                if array_inputs:
                    if type(res.value) == list:
                        raise CalculatorException("Cannot pass multiple arrays to an operation that returns an array")
                    results.append(res)
                else:
                    return res

            return OperandResult(results, None, None)

        else:

            # If any inputs are an exception, and this operation isn't flagged as allowing them as inputs, then throw the exception
            if not self.inputs_can_be_exceptions:
                for i in inputs:
                    if isinstance(i.value, Exception):
                        return i

            try:

                # Validate the values and units for this operation
                values = [i.value for i in inputs]
                units = [i.unit for i in inputs]
                refs = [i.ref for i in inputs]
                self.validate(calculator, values, units, refs)

                # Auto-convert all numbers into decimal numbers. Store the original number type of the first input, this will be used
                # for the result.
                result_value, result_unit, result_ref, number_cast = None, None, None, None
                if self.auto_convert_numerical_inputs:
                    values, number_cast = self.convert_numbers(calculator, values)

                # Normalise the units of all inputs if units_normalise flag is set
                if len([i for i in range(0, len(values)) if not self.input_can_be_numerical_type(calculator, i) or not calculator.validate_number(values[i])]) == 0:

                    # All inputs are numbers, normalise them to be all be the same unit
                    if calculator.unit_normaliser is not None and self.units_normalise:
                        values, units, result_unit = calculator.unit_normaliser.normalise_inputs(values, units, self.units_multi, self.units_relative)

                else:

                    # Go through each input and check if it's an array of numbers
                    for i in range(0, len(values)):
                        if type(values[i]) == list and self.input_must_be_numerical_type(calculator, i, 'array'):

                            # This is an array of numbers

                            # Normalise all elements to be decimal
                            this_values = [v.value for v in values[i]]
                            for ii in range(0, len(values[i])):
                                num = calculator.number(this_values[ii])
                                this_values[ii] = num
                                if number_cast is None:
                                    # Take the first number type we get as the one we should use for the final result
                                    number_cast = num.number_cast

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

                result = self.ref(calculator, values, units, refs, flags.copy())
                result_value = result.value

                # Convert the number type of the result
                if self.auto_convert_numerical_result and isinstance(result_value, Number) and number_cast:
                    result_value.number_cast = number_cast

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
                if err.wrapped:
                    raise err
                values = str.join(', ', [op_input.to_string(calculator) for op_input in inputs])
                newerr = CalculatorException("Could not execute {0} with parameters: {1} - {2}".format(self.name, values, err.message))
                newerr.wrapped = True
                raise newerr
            except Exception as err:
                values = str.join(', ', [op_input.to_string(calculator) for op_input in inputs])
                raise CalculatorException("Could not execute {0} with parameters: {1}".format(self.name, values))

    def validate(self, calculator, values, units, refs):
        # Check if we're been given at least the minimum number of params
        if self.minparams is not None and len(values) < self.minparams:
            raise CalculatorException("{0} requires at least {1} parameters, only given {2}".format(self.name, self.minparams, len(values)))

        # Check we've not been given more than the maximum
        if self.maxparams is not None and len(values) > self.maxparams:
            raise CalculatorException("{0} requires at most {1} parameters, was given {2}".format(self.name, self.maxparams, len(values)))

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
                    raise CalculatorException("{0} parameter {1} must be of type(s) {2}".format(self.name, i + 1, str.join(', ', [self.get_validator_type_name(calculator, o) for o in objtypes])))

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
            return calculator.validators[obj_type]['ref'](calculator, value, unit, ref, obj_sub_type)
        if obj_type in calculator.validators and calculator.validators[obj_type]['ref'](calculator, value, unit, ref):
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

    def get_validator_type_name(self, calculator, name):
        if name in calculator.validators:
            return calculator.validators[name]['desc']
        obj_type, obj_sub_type = self.parse_sub_type(name)
        if obj_type not in calculator.validators:
            raise Exception("Validator type {} not valid".format(name))
        if obj_sub_type not in calculator.validators:
            raise Exception("Validator type {} not valid".format(name))
        if obj_sub_type is None:
            raise Exception("Validator type {} not valid".format(name))
        return "{} of type {}".format(calculator.validators[obj_type]['desc'], calculator.validators[obj_sub_type]['desc'])

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

    def input_can_be_numerical_type(self, calculator, i, obj_type=None):
        for numerical_type in calculator.numerical_validators:
            if obj_type is None:
                if self.input_can_be_type(i, numerical_type):
                    return True
            else:
                if self.input_can_be_type(i, obj_type, numerical_type):
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

    def input_must_be_numerical_type(self, calculator, i, obj_type=None):
        for numerical_type in calculator.numerical_validators:
            if obj_type is None:
                if self.input_must_be_type(i, numerical_type):
                    return True
            else:
                if self.input_must_be_type(i, obj_type, numerical_type):
                    return True
        return False

    def convert_numbers(self, calculator, values):
        new_values = values.copy()
        number_cast = None
        set_number_cast = False

        # If an input is declared it can be a number, and it contains a numerical value, convert it to a number
        for restriction in self.value_restrictions:
            objtypes = restriction['objtypes']
            # Check if any of the object types are a type of number
            if len([n for n in calculator.numerical_validators for o in objtypes if n == o]) > 0:
                fromparam = restriction['fromparam']
                toparam = len(values)
                if 'toparam' in restriction and restriction['toparam'] is not None:
                    toparam = restriction['toparam'] + 1
                for i in range(fromparam, toparam):
                    if i < len(values):
                        # This input is declared it can be a number, check it contains a number
                        if calculator.validate_number(values[i]):
                            num = calculator.number(values[i])
                            if set_number_cast is False:
                                number_cast = num.number_cast
                                set_number_cast = True
                            new_values[i] = num

        return new_values, number_cast


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
            super().__init__(category, "operator " + name, description, syntax, ref, num_of_params, num_of_params)
            for i, objtype in enumerate(objtypes):
                self.add_value_restriction(i, i, objtype)
        else:
            super().__init__(category, "operator " + name, description, syntax, ref, num_of_params, num_of_params, objtypes)

        self.rtl = False
        self.hidden = False
