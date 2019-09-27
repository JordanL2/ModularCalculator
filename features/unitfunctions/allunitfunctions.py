#!/usr/bin/python3

from modularcalculator.features.feature import MetaFeature

class AllUnitFunctionsMetaFeature(MetaFeature):

    def id():
        return 'unitfunctions.allunitfunctions'

    def category():
        return 'Unit Functions'

    def title():
        return 'All Unit Functions'

    def desc():
        return 'Handy feature to install all functions involving units'

    def dependencies():
        return []

    def subfeatures():
        return [
            'unitfunctions.generalunitfunctions',
        ]
