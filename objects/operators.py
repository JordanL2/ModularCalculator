#!/usr/bin/python3

from modularcalculator.objects.items import *


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

    def add_value_restriction(self, fromparam, toparam, objtypes):
        if objtypes is not None:
            if not isinstance(objtypes, list):
                objtypes = [objtypes]
            self.value_restrictions.append({'fromparam': fromparam, 'toparam': toparam, 'objtypes': objtypes})

    def add_unit_restriction(self, fromparam, toparam, dimensions):
        self.unit_restrictions.append({'fromparam': fromparam, 'toparam': toparam, 'dimensions': dimensions})

    def call(self, calculator, inputs, flags):
        if not self.inputs_can_be_exceptions:
            for i in inputs:
                if isinstance(i.value, Exception):
                    return i

        values = [i.value for i in inputs]
        units = [i.unit for i in inputs]
        refs = [i.ref for i in inputs]

        self.validate(calculator, values, units, refs)

        result_value, result_unit, result_ref = None, None, None
        if calculator.unit_normaliser is not None and self.units_normalise:
            values, units, result_unit = calculator.unit_normaliser.normalise_inputs(values, units, self.units_multi, self.units_relative)
        
        try:
            result = self.ref(calculator, values, units, refs, flags.copy())
            result_value = result.value
            if result.unit_override:
                result_unit = result.unit
            if result.ref_override:
                result_ref = result.ref
            operandResult = OperandResult(result_value, result_unit, result_ref)
            if calculator.number_auto_func is not None and calculator.number_auto_func != self and calculator.validate_number(result_value, None, None):
                operandResult = calculator.number_auto_func.call(calculator, [operandResult], flags)
            return operandResult

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
                    if len([o for o in objtypes if o in calculator.validators and calculator.validators[o](calculator, values[i], units[i], refs[i])]) == 0:
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
