#!/usr/bin/python3

from modularcalculator.features.feature import MetaFeature


class AllUnitDefinitionsMetaFeature(MetaFeature):

    def id():
        return 'unitdefinitions.allunitdefinitions'

    def category():
        return 'Unit Definitions'

    def title():
        return 'All Unit Definitions'

    def desc():
        return 'Handy feature to install all unit definitions'

    def dependencies():
        return []

    def subfeatures():
        return [
            'unitdefinitions.absorbeddose',
            'unitdefinitions.acceleration',
            'unitdefinitions.angle',
            'unitdefinitions.area',
            'unitdefinitions.capacitance',
            'unitdefinitions.catalyticactivity',
            'unitdefinitions.data',
            'unitdefinitions.distance',
            'unitdefinitions.electricalconductance',
            'unitdefinitions.electricalpotential',
            'unitdefinitions.electriccharge',
            'unitdefinitions.electriccurrent',
            'unitdefinitions.energy',
            'unitdefinitions.equivalentdose',
            'unitdefinitions.force',
            'unitdefinitions.frequency',
            'unitdefinitions.illuminance',
            'unitdefinitions.inductance',
            'unitdefinitions.luminousflux',
            'unitdefinitions.luminousintensity',
            'unitdefinitions.magneticflux',
            'unitdefinitions.magneticfluxdensity',
            'unitdefinitions.mass',
            'unitdefinitions.power',
            'unitdefinitions.pressure',
            'unitdefinitions.radioactivity',
            'unitdefinitions.resistance',
            'unitdefinitions.solidangle',
            'unitdefinitions.substance',
            'unitdefinitions.temperature',
            'unitdefinitions.time',
            'unitdefinitions.velocity',
            'unitdefinitions.volume',
        ]
