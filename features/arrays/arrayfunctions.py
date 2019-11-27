#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.exceptions import *
from modularcalculator.features.feature import Feature


class ArrayFunctionsFeature(Feature):

    def id():
        return 'arrays.arrayfunctions'

    def category():
        return 'Arrays'

    def title():
        return 'Array Functions'

    def desc():
        return 'Functions for manipulating arrays'

    def dependencies():
        return ['arrays.arrays', 'structure.functions']

    @classmethod
    def install(cls, calculator):
        pass
