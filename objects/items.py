#!usr/bin/python3

from modularcalculator.objects.exceptions import *

from decimal import *


def previous_functional_item(items, i):
    i -= 1
    while i >= 0 and not items[i].functional():
        i -= 1
    if i >= 0:
        return items[i]
    return None

def functional_items(items):
    return [i for i in items if i.functional()]


class Item:
    
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def isop(self):
        raise CalculatorException("Must override this method")

    def desc(self):
        raise CalculatorException("Must override this method")

    def functional(self):
        return True


class OperatorItem(Item):

    def __init__(self,  op):
        super().__init__(op)
        self.op = op

    def isop(self):
        return True

    def desc(self):
        return 'op'


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


class LiteralItem(OperandItem):

    def __init__(self, text, val):
        super().__init__(text)
        self.val = val

    def desc(self):
        return 'literal'

    def value(self, flags):
        return self.val


class RecursiveOperandItem(OperandItem):

    def __init__(self, text, items, calculator):
        super().__init__(text)
        self.items = items
        self.calculator = calculator


class NonFunctionalItem(Item):

    def isop(self):
        return False

    def functional(self):
        return False

    def value(self, flags):
        raise Exception("value() called on non-functional item")


class OperandResult:

    def __init__(self, value, unit, ref):
        if unit is not None and not isinstance(value, Decimal):
            raise CalculatorException("Values must be numerical when unit is set")
        self.value = value
        self.unit = unit
        self.ref = ref

    def __str__(self):
        if self.unit is not None:
            return str(self.value) + ' ' + str(self.unit)
        return str(self.value)


class ExceptionOperandResult(OperandResult):

    def __init__(self, err):
        super().__init__(err, None, None)
