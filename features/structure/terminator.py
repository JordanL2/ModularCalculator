#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.features.feature import Feature


class TerminatorFeature(Feature):

    def id():
        return 'structure.terminator'

    def category():
        return 'Structure'

    def title():
        return 'Terminators'

    def desc():
        return 'Enables multi-part statements, separated by semi-colons'

    def dependencies():
        return []

    def default_options():
        return {
            'Symbol': "\n"
        }

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('terminator', TerminatorFeature.parse_terminator)

        calculator.feature_options['structure.terminator'] = cls.default_options()

    def parse_terminator(self, expr, i, items, flags):
        if 'ignore_terminators' in flags and flags['ignore_terminators']:
            return None, None, None

        next = expr[i:]
        symbol = self.feature_options['structure.terminator']['Symbol']
        if next[0:len(symbol)] == symbol:
            func_items = functional_items(items)
            for n in range(0, 3):
                if len(func_items) - n > 0:
                    prev = func_items[len(func_items) - n - 1]
                    if prev is not None and prev.isop():
                        op = prev.op
                        if op in self.ops_list:
                            op_info = self.ops_list[op]
                            if len(op_info.rinputs) > n:
                                return None, None, None

            return [TerminatorItem(symbol)], len(symbol), {'end': True}

        return None, None, None


class TerminatorItem(NonFunctionalItem):

	def __init__(self, text):
		super().__init__(text)

	def desc(self):
		return 'terminator'
