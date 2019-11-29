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
        array_inputs = []
        for i, inp in enumerate(inputs):
            if type(inp.value) == list and not self.input_can_be_type(i, 'array') and not (inp.ref is not None and self.input_can_be_type(i, 'variable')):
                array_inputs.append(i)

        if len(array_inputs) > 0:

            lengths = set()
            for i in array_inputs:
                lengths.add(len(inputs[i].value))
            if len(lengths) > 1:
                raise CalculatorException("All array inputs must all be same length")
            length = lengths.pop()

            results = []
            for i in range(0, length):
                input_row = []
                for ii, inp in enumerate(inputs):
                    if ii in array_inputs:
                        input_row.append(inp.value[i])
                    else:
                        input_row.append(inp)
                res = self.call(calculator, input_row, flags)
                results.append(res)

            return OperandResult(results, None, None)

        else:

            if not self.inputs_can_be_exceptions:
                for i in inputs:
                    if isinstance(i.value, Exception):
                        return i

            values = [i.value for i in inputs]
            units = [i.unit for i in inputs]
            refs = [i.ref for i in inputs]

            self.validate(calculator, values, units, refs)

            num_type = None
            if self.auto_convert_numerical_inputs:
                values, num_type = self.convert_numbers(calculator, values)

            result_value, result_unit, result_ref = None, None, None
            if calculator.unit_normaliser is not None and self.units_normalise:
                if len([i for i in range(0, len(values)) if not self.input_can_be_type(i, 'number') or not calculator.validate_number(values[i])]) == 0:
                    number_types = []
                    for i in range(0, len(values)):
                        values[i], this_type = calculator.number(values[i])
                        number_types.append(this_type)
                    values, units, result_unit = calculator.unit_normaliser.normalise_inputs(values, units, self.units_multi, self.units_relative)
                    for i in range(0, len(values)):
                        values[i] = calculator.restore_number_type(values[i], number_types[i])
                else:
                    for i in range(0, len(values)):
                        if type(values[i]) == list and self.input_must_be_type(i, 'array', 'number'):
                            this_values = [v.value for v in values[i]]
                            this_units = [v.unit for v in values[i]]

                            number_types = []
                            for ii in range(0, len(this_values)):
                                this_values[ii], this_type = calculator.number(this_values[ii])
                                number_types.append(this_type)
                            this_values, this_units, result_unit = calculator.unit_normaliser.normalise_inputs(this_values, this_units, self.units_multi, self.units_relative)
                            for ii in range(0, len(this_values)):
                                this_values[ii] = calculator.restore_number_type(this_values[ii], number_types[ii])

                            values[i] = values[i].copy()
                            for ii in range(0, len(this_values)):
                                values[i][ii] = OperandResult(this_values[ii], this_units[ii], values[i][ii].ref)

            try:
                result = self.ref(calculator, values, units, refs, flags.copy())
                result_value = result.value
                if self.auto_convert_numerical_result and isinstance(result_value, Decimal) and num_type:
                    result_value = calculator.restore_number_type(result_value, num_type)
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
        if self.minparams is not None and len(values) < self.minparams:
            raise CalculatorException("{0} requires at least {1} params, only given {2}".format(self.name, self.minparams, len(values)))
        if self.maxparams is not None and len(values) > self.maxparams:
            raise CalculatorException("{0} requires at most {1} params, was given {2}".format(self.name, self.maxparams, len(values)))
        
        for restriction in self.value_restrictions:
            fromparam = restriction['fromparam']
            toparam = len(units)
            if 'toparam' in restriction and restriction['toparam'] is not None:
                toparam = restriction['toparam'] + 1
            objtypes = restriction['objtypes']
            for i in range(fromparam, toparam):
                if i < len(values):
                    if len([o for o in objtypes if self.validate_input(o, calculator, values[i], units[i], refs[i])]) == 0:
                        raise CalculatorException("{0} parameter {1} must be of type(s) {2}".format(self.name, i + 1, str.join(', ', objtypes)))
        
        for restriction in self.unit_restrictions:
            fromparam = restriction['fromparam']
            toparam = len(units)
            if 'toparam' in restriction and restriction['toparam'] is not None:
                toparam = restriction['toparam'] + 1
            dimensions = restriction['dimensions']
            for i in range(fromparam, toparam):
                if i < len(units):
                    if not calculator.unit_normaliser.check_unit_dimensions(units[i], dimensions):
                        dimension_string = str.join(' ', ["{0}^{1}".format(dimensions[ii], str(dimensions[ii + 1])) for ii in range(0, len(dimensions), 2)])
                        raise CalculatorException("{0} parameter {1} must have unit dimensions: {2}".format(self.name, i + 1, dimension_string))

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

        for restriction in self.value_restrictions:
            objtypes = restriction['objtypes']
            if len(objtypes) == 1 and objtypes[0] == 'number':
                fromparam = restriction['fromparam']
                toparam = len(values)
                if 'toparam' in restriction and restriction['toparam'] is not None:
                    toparam = restriction['toparam'] + 1
                for i in range(fromparam, toparam):
                    if i < len(values):
                        num, num_type_res = calculator.number(values[i])
                        new_values[i] = num
                        if num_type is None:
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
