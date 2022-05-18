#!/usr/bin/python3

from modularcalculator.features.feature import Feature
from modularcalculator.objects.number import *
from modularcalculator.objects.units import *


class AbstractUnitFeature(Feature):

    def category():
        return 'Unit Definitions'

    def dependencies():
        return ['units.units', 'units.systems']

    def after():
        return ['units.basicunitprefixes', 'units.advancedunitprefixes']
