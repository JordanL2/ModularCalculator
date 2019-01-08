#!/usr/bin/python3

from modularcalculator.objects.units import *
from modularcalculator.features.feature import Feature


class AbstractUnitFeature(Feature):

    def category():
        return 'Unit Definitions'

    def dependencies():
        return ['units.units', 'units.systems']

    def after():
        return ['units.basicunitprefixes', 'units.advancedunitprefixes']
