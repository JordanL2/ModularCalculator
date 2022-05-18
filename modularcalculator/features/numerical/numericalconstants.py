#!/usr/bin/python3

from modularcalculator.features.feature import Feature
from modularcalculator.objects.number import *


class NumericalConstantsFeature(Feature):

    e = '2.71828182845904523536028747135266249775724709369995'
    pi = '3.14159265358979323846264338327950288419716939937511'
    tau = '6.28318530717958647692528676655900576839433879875022'

    def id():
        return 'numerical.numericalconstants'

    def category():
        return 'Numerical'

    def title():
        return 'Numerical Constants'

    def desc():
        return 'e, pi, tau'

    def dependencies():
        return ['state.constants']

    @classmethod
    def install(cls, calculator):
        calculator.constants['e'] = Number(NumericalConstantsFeature.e)
        calculator.constants['pi'] = Number(NumericalConstantsFeature.pi)
        calculator.constants['tau'] = Number(NumericalConstantsFeature.tau)
