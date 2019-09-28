#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.features.feature import Feature

import re


class OperatorsFeature(Feature):

    def id():
        return "structure.operators"

    def category():
        return "Structure"

    def title():
        return "Operators"

    def desc():
        return "Enables operators"

    def dependencies():
        return []

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('operator', OperatorsFeature.parse_operator)

    def parse_operator(self, expr, i, items, flags):
        next = expr[i:]
        for op in sorted([op for op in self.ops_symbols if next.startswith(op)], key=len, reverse=True):
            if op.isalpha():
                op_regex = re.compile("({0})(\W|$)".format(op))
                op_match = op_regex.match(next)
                if op_match:
                	return [OperatorItem(op)], len(op), None
            else:
                return [OperatorItem(op)], len(op), None
        return None, None, None
