#!/usr/bin/python3

from modularcalculator.objects.operators import OperationResult, OperatorDefinition
from modularcalculator.features.strings.strings import StringsFeature
from modularcalculator.features.feature import Feature


class StringComparisonFeature(Feature):

    def id():
        return 'strings.stringcomparison'

    def category():
        return 'String'

    def title():
        return 'String Comparison Operators'

    def desc():
        return 'Eg: <=$, ==$, !=$'

    def dependencies():
        return ['strings.strings', 'boolean.booleans']

    @classmethod
    def install(cls, calculator):
        calculator.add_op(OperatorDefinition(
            'String', 
            '<$', 
            'Less than, alphabetical',
            StringComparisonFeature.op_string_lessthan, 
            1, 
            1, 
            'string'))
        calculator.add_op(OperatorDefinition(
            'String', 
            '>$', 
            'More than, alphabetical',
            StringComparisonFeature.op_string_morethan, 
            1, 
            1, 
            'string'))
        calculator.add_op(OperatorDefinition(
            'String', 
            '<=$', 
            'Less than or equal to, alphabetical',
            StringComparisonFeature.op_string_lessthanequal, 
            1, 
            1, 
            'string'))
        calculator.add_op(OperatorDefinition(
            'String', 
            '>=$', 
            'More than or equal to, alphabetical',
            StringComparisonFeature.op_string_morethanequal, 
            1, 
            1, 
            'string'))
        calculator.add_op(OperatorDefinition(
            'String', 
            '==$', 
            'Equal to, string-wise',
            StringComparisonFeature.op_string_equals, 
            1, 
            1, 
            'string'))
        calculator.add_op(OperatorDefinition(
            'String', 
            '!=$', 
            'Not equal to, string-wise',
            StringComparisonFeature.op_string_notequals, 
            1, 
            1, 
            'string'))
        
        calculator.add_op(OperatorDefinition(
            'String Case-Insensitive', 
            '<~', 
            'Less than, alphabetical, case-insensitive',
            StringComparisonFeature.op_stringcaseless_lessthan, 
            1, 
            1, 
            'string'))
        calculator.add_op(OperatorDefinition(
            'String Case-Insensitive', 
            '>~', 
            'More than, alphabetical, case-insensitive',
            StringComparisonFeature.op_stringcaseless_morethan, 
            1, 
            1, 
            'string'))
        calculator.add_op(OperatorDefinition(
            'String Case-Insensitive', 
            '<=~', 
            'Less than or equal to, alphabetical, case-insensitive',
            StringComparisonFeature.op_stringcaseless_lessthanequal, 
            1, 
            1, 
            'string'))
        calculator.add_op(OperatorDefinition(
            'String Case-Insensitive', 
            '>=~', 
            'More than or equal to, alphabetical, case-insensitive',
            StringComparisonFeature.op_stringcaseless_morethanequal, 
            1, 
            1, 
            'string'))
        calculator.add_op(OperatorDefinition(
            'String Case-Insensitive', 
            '==~', 
            'Equal to, string-wise, case-insensitive',
            StringComparisonFeature.op_stringcaseless_equals, 
            1, 
            1, 
            'string'))
        calculator.add_op(OperatorDefinition(
            'String Case-Insensitive', 
            '!=~', 
            'Not equal to, string-wise, case-insensitive',
            StringComparisonFeature.op_stringcaseless_notequals, 
            1, 
            1, 
            'string'))

    def op_string_lessthan(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]) < StringsFeature.string(self, vals[1]))

    def op_string_morethan(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]) > StringsFeature.string(self, vals[1]))

    def op_string_lessthanequal(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]) <= StringsFeature.string(self, vals[1]))

    def op_string_morethanequal(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]) >= StringsFeature.string(self, vals[1]))

    def op_string_equals(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]) == StringsFeature.string(self, vals[1]))

    def op_string_notequals(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]) != StringsFeature.string(self, vals[1]))

    def op_stringcaseless_lessthan(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).lower() < StringsFeature.string(self, vals[1]).lower())

    def op_stringcaseless_morethan(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).lower() > StringsFeature.string(self, vals[1]).lower())

    def op_stringcaseless_lessthanequal(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).lower() <= StringsFeature.string(self, vals[1]).lower())

    def op_stringcaseless_morethanequal(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).lower() >= StringsFeature.string(self, vals[1]).lower())

    def op_stringcaseless_equals(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).lower() == StringsFeature.string(self, vals[1]).lower())

    def op_stringcaseless_notequals(self, vals, units, refs, flags):
        return OperationResult(StringsFeature.string(self, vals[0]).lower() != StringsFeature.string(self, vals[1]).lower())
