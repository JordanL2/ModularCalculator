#!/usr/bin/python3

from modularcalculator.features.feature import Feature
from modularcalculator.features.strings.strings import StringsFeature
from modularcalculator.features.structure.functions import FunctionDefinition
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *
from modularcalculator.objects.number import *
from modularcalculator.objects.operators import OperationResult, OperatorDefinition

import re


class RegexFeature(Feature):

    def id():
        return 'strings.regex'

    def category():
        return 'String'

    def title():
        return 'Regular Expressions'

    def desc():
        return 'Functions for regular expressions'

    def dependencies():
        return ['strings.strings','structure.functions','arrays.arrays']

    @classmethod
    def install(cls, calculator):
        calculator.add_op(OperatorDefinition(
            'Regular Expression',
            '=~',
            'Return true if value matches regex',
            RegexFeature.op_regex,
            1,
            1,
            'string'))

        calculator.add_op(OperatorDefinition(
            'Regular Expression',
            '!~',
            'Return true if value doesn\'t match regex',
            RegexFeature.op_regexnot,
            1,
            1,
            'string'))

        calculator.funcs['regexget'] = FunctionDefinition(
            'Regular Expression',
            'regexget',
            'Return either all or a specific occurrence of a pattern in a string',
            ['string', 'pattern', '[group]'],
            RegexFeature.func_regexget,
            2,
            3)
        calculator.funcs['regexget'].add_value_restriction(0, 1, 'string')
        calculator.funcs['regexget'].add_value_restriction(2, 2, 'number')

        calculator.funcs['regexsplit'] = FunctionDefinition(
            'Regular Expression',
            'regexsplit',
            'Split a string on a regular expression and return as an array',
            ['string', 'pattern'],
            RegexFeature.func_regexsplit,
            2,
            2,
            'string')

        calculator.funcs['regexsub'] = FunctionDefinition(
            'Regular Expression',
            'regexsub',
            'Replace all or a specific occurrence of a pattern with a replacement',
            ['string', 'pattern', 'replacement', '[group]'],
            RegexFeature.func_regexsub,
            3,
            4)
        calculator.funcs['regexsub'].add_value_restriction(0, 2, 'string')
        calculator.funcs['regexsub'].add_value_restriction(3, 3, 'number')

        calculator.funcs['regexcount'] = FunctionDefinition(
            'Regular Expression',
            'regexcount',
            'Count the number of times a pattern appears in a string',
            ['string', 'pattern'],
            RegexFeature.func_regexcount,
            2,
            2)
        calculator.funcs['regexcount'].add_value_restriction(0, 1, 'string')

    def op_regex(self, vals, units, refs, flags):
        return OperationResult((re.search(StringsFeature.string(self, vals[1]), StringsFeature.string(self, vals[0])) is not None))

    def op_regexnot(self, vals, units, refs, flags):
        return OperationResult((re.search(StringsFeature.string(self, vals[1]), StringsFeature.string(self, vals[0])) is None))

    def func_regexget(self, vals, units, refs, flags):
        found = re.findall(StringsFeature.string(self, vals[1]), StringsFeature.string(self, vals[0]))
        if len(vals) == 3:
            group = int(vals[2]) - 1
            return OperationResult(found[int(group)])
        found = [OperandResult(f, None, None) for f in found]
        return OperationResult(found)

    def func_regexsplit(self, vals, units, refs, flags):
        found = re.split(StringsFeature.string(self, vals[1]), StringsFeature.string(self, vals[0]))
        found = [OperandResult(f, None, None) for f in found]
        return OperationResult(found)

    def func_regexsub(self, vals, units, refs, flags):
        if len(vals) == 4:
            return OperationResult(re.subn(StringsFeature.string(self, vals[1]), StringsFeature.string(self, vals[2]), StringsFeature.string(self, vals[0]), int(vals[3]))[0])
        elif len(vals) == 3:
            return OperationResult(re.sub(StringsFeature.string(self, vals[1]), StringsFeature.string(self, vals[2]), StringsFeature.string(self, vals[0])))
        else:
            raise CalculatorException("regexsub requires 3 or 4 arguments, found {0}".format(len(vals)))

    def func_regexcount(self, vals, units, refs, flags):
        return OperationResult(Number(len(re.findall(StringsFeature.string(self, vals[1]), StringsFeature.string(self, vals[0])))))
