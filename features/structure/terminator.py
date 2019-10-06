#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.features.feature import Feature

import copy


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
            backup_vars = copy.deepcopy(self.vars)
            try:
                self.execute(copy_items(items), {})
            except ExecutionException as e:
                if str(e.message).startswith('Missing right operands for operator '):
                    self.vars = backup_vars
                    return None, None, None
            except Exception:
                pass
            finally:
                self.vars = backup_vars

            return [TerminatorItem(symbol)], len(symbol), {'end': True}

        return None, None, None


class TerminatorItem(NonFunctionalItem):

    def __init__(self, text):
        super().__init__(text)

    def desc(self):
        return 'terminator'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy
