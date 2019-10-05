#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.features.feature import Feature

import re


class SpaceFeature(Feature):

    def id():
        return 'nonfunctional.space'

    def category():
        return 'Non-Functional'

    def title():
        return 'White-Space'

    def desc():
        return 'Spaces, tabs, new lines'

    def dependencies():
        return []

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('space', SpaceFeature.parse_space)

    space_regex = re.compile(r'(\s)')

    def parse_space(self, expr, i, items, flags):
        next = expr[i:]
        space_match = SpaceFeature.space_regex.match(next)
        if (space_match):
            space = space_match.group(1)
            return [SpaceItem(space)], len(space), None
        return None, None, None


class SpaceItem(NonFunctionalItem):

	def desc(self):
		return 'space'
