#!/usr/bin/python3

from modularcalculator.objects.items import *
from modularcalculator.objects.exceptions import *
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

        calculator.last_failed_terminator = None

    def parse_terminator(self, expr, i, items, flags):
        if 'ignore_terminators' in flags and flags['ignore_terminators']:
            return None, None, None

        next = expr[i:]
        symbol = self.feature_options['structure.terminator']['Symbol']
        if next[0:len(symbol)] == symbol:
            func_items = functional_items(items)
            func_item_text = items_text(func_items)
            if func_item_text == self.last_failed_terminator:
                return None, None, None

            backup_vars = self.vars.copy()

            try:
                self.execute(func_items, {'fake_execution': True})
            except ExecuteException as e:
                if str(e.message).startswith('Missing right operands for operator '):
                    self.vars = backup_vars
                    self.last_failed_terminator = func_item_text
                    return None, None, None
            except Exception:
                pass
            finally:
                self.vars = backup_vars

            return [TerminatorItem(symbol)], len(symbol), {'end_statement': True}

        return None, None, None


class TerminatorItem(NonFunctionalItem):

    def __init__(self, text):
        super().__init__(text)

    def desc(self):
        return 'terminator'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy
