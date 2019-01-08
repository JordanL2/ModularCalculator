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

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('terminator', TerminatorFeature.parse_terminator)

        calculator.feature_options['structure.terminator'] = {
            'Symbol': ';'
        }

    def parse_terminator(self, expr, i, items, flags):
        next = expr[i:]
        if next[0] == self.feature_options['structure.terminator']['Symbol']:
            return [TerminatorItem()], 1, {'end': True}
        return None, None, None


class TerminatorItem(NonFunctionalItem):

	def __init__(self):
		super().__init__(';')

	def desc(self):
		return 'terminator'
