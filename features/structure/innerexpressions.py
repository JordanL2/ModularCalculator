#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.engine import *
from modularcalculator.features.feature import Feature


class InnerExpressionsFeature(Feature):

    def id():
        return 'structure.innerexpressions'

    def category():
        return 'Structure'

    def title():
        return 'Enables inner expressions'

    def desc():
        return 'Inner expressions / brackets, eg: 2 * (3 + 4)'

    def dependencies():
        return []

    @classmethod
    def install(cls, calculator):
        calculator.add_parser('inner_expr', InnerExpressionsFeature.parse_inner_expr)
        calculator.add_parser('inner_expr_end', InnerExpressionsFeature.parse_close_inner_expr)

    def parse_inner_expr(self, expr, i, items, flags):
        next = expr[i:]
        if next.startswith('('):
            flags['inner_expr'] = True
            flags['ignore_terminators'] = True
            inner_items, length, return_flags = None, None, None
            try:
                inner_items, length, return_flags = self.parse(next[1:], flags)
                inner_items = inner_items[0]
            except ParsingException as err:
                err.items[-1].insert(0, InnerExpressionStartItem())
                raise ParsingException(err.message, [InnerExpressionItem(err.truncate(next), err.items[0], self)], err.next, True)
            inner_items.insert(0, InnerExpressionStartItem())
            if 'end_inner_expr' not in return_flags:
                raise ParsingException('Inner expression missing close symbol', [], next)
            return [InnerExpressionItem(next[0:length + 2], inner_items, self)], length + 2, None
        return None, None, None

    def parse_close_inner_expr(self, expr, i, items, flags):
        next = expr[i:]
        inner = ('inner_expr' in flags.keys() and flags['inner_expr'])
        if next.startswith(')'):
            if (inner):
                return [InnerExpressionEndItem()], None, {'end': True, 'end_inner_expr': True}
            raise ParsingException('Unexpected inner expression close symbol found', [], next)
        return None, None, None


class InnerExpressionItem(RecursiveOperandItem):

    def __init__(self, text, items, calculator):
        super().__init__(text, items, calculator)
    
    def desc(self):
        return 'inner_expr'

    def value(self, flags):
        try:
            val = self.calculator.execute(copy_items(self.items), flags.copy())
            if isinstance(val.value, Exception):
                raise val.value
            return OperandResult(val.value, val.unit, val.ref)
        except ExecutionException as err:
            self.items = err.items
            err.items = [err.items.copy()]
            self.text = err.truncate(self.text)
            self.truncated = True
            raise ExecutionException(err.message, [[self]], err.next, True)

    def result(self, flags):
        return self.value(flags)

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy


class InnerExpressionStartItem(NonFunctionalItem):

    def __init__(self):
        super().__init__('(')

    def desc(self):
        return 'inner_expr_start'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy


class InnerExpressionEndItem(NonFunctionalItem):

    def __init__(self):
        super().__init__(')')

    def desc(self):
        return 'inner_expr_end'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy
