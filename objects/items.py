#!usr/bin/python3

from modularcalculator.objects.exceptions import *

from decimal import *


def previous_functional_item(items, i=None):
    if i is None:
        i = len(items)
    i -= 1
    while i >= 0 and not items[i].functional():
        i -= 1
    if i >= 0:
        return items[i]
    return None

def functional_items(items):
    return [i for i in items if i.functional()]

def copy_items(items):
    return [i.copy() for i in items]


class Item:
    
    def __init__(self, text):
        self.text = text
        self.truncated = False

    def __str__(self):
        return self.text

    def isop(self):
        raise CalculatorException("Must override this method")

    def desc(self):
        raise CalculatorException("Must override this method")

    def functional(self):
        return True

    def copy(self, classtype=None):
        copy = (classtype or self.__class__).__new__(classtype or self.__class__)
        copy.text = self.text
        copy.truncated = self.truncated
        return copy


class OperatorItem(Item):

    def __init__(self,  op):
        super().__init__(op)
        self.op = op

    def isop(self):
        return True

    def desc(self):
        return 'op'

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.op = self.op
        return copy


class OperandItem(Item):

    unit = None
    
    def __init__(self,  text):
        super().__init__(text)

    def isop(self):
        return False

    def value(self, flags):
        raise CalculatorException("Must override this method")

    def result(self, flags):
        return OperandResult(self.value(flags), self.unit, self)

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.unit = self.unit
        return copy


class LiteralItem(OperandItem):

    def __init__(self, text, val):
        super().__init__(text)
        self.val = val

    def desc(self):
        return 'literal'

    def value(self, flags):
        return self.val

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.val = self.val
        return copy


class RecursiveOperandItem(OperandItem):

    def __init__(self, text, items, calculator):
        super().__init__(text)
        self.items = items
        self.calculator = calculator

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        copy.items = self.items.copy()
        copy.calculator = self.calculator
        return copy


class NonFunctionalItem(Item):

    def isop(self):
        return False

    def functional(self):
        return False

    def value(self, flags):
        raise Exception("value() called on non-functional item")

    def copy(self, classtype=None):
        copy = super().copy(classtype or self.__class__)
        return copy


class OperandResult:

    def __init__(self, value, unit, ref):
        self.value = value
        self.unit = unit
        self.ref = ref

    def __str__(self):
        if self.unit is not None:
            return str(self.value) + ' ' + str(self.unit)
        return str(self.value)
