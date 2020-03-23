#!/usr/bin/python3


from modularcalculator.objects.items import *


def find_pos(self, text, statements):
    i = 0
    prev_item = None
    for items in statements:
        for item in items:
            ii = text.find(item.text, i)
            if ii == -1:
                raise Exception("Could not find item |{}| in text |{}| after position {}".format(item.text, text, i))
            if ii != i:
                if prev_item is None or not prev_item.truncated:
                    print("Error in", "|" + text + "|", "- Unexpected characters at", i, "- |" + text[i:ii] + "|")
                    for item2 in items:
                        print("Item:", "|" + item2.text + "|")
                    print("End of items.\n")
            i = ii + len(item.text)
            prev_item = item
    if self.next is not None:
        ii = text.find(self.next, i)
        if ii == -1:
            raise Exception("Could not find '{0}' in '{1}' after character {2} [{3}]".format(self.next, text, i, text[i:]))
        i = ii
    return i


class CalculatorException(Exception):

    def __init__(self, message):
        self.message = message


class CalculatingException(CalculatorException):

    def __init__(self, message, statements, next, truncated=False):
        self.message = message
        if statements is not None:
            for s in statements:
                if not isinstance(s, list):
                    raise Exception("Created CalculatingException with non-lists in statements field")
        self.statements = statements
        self.next = next
        self.truncated = truncated

    def find_pos(self, text):
        return find_pos(self, text, self.statements)

    def truncate(self, text):
        i = self.find_pos(text)
        return text[0:i]

    def set_response(self, response):
        self.response = response
    
    def has_response(self):
        return hasattr(self, 'response')


class ParsingException(CalculatingException):

    pass


class ExecutionException(CalculatingException):
  
    pass


class CalculateException(CalculatorException):

    def __init__(self, message, items, next, truncated=False):
        self.message = message
        if items is not None:
            for i in items:
                if not isinstance(i, Item):
                    raise Exception("Created CalculateException with non-Items in items field")
        self.items = items
        self.next = next
        self.truncated = truncated

    def find_pos(self, text):
        return find_pos(self, text, [self.items])

    def truncate(self, text):
        i = self.find_pos(text)
        return text[0:i]
    

class ParseException(CalculateException):

    pass


class ExecuteException(CalculateException):
  
    pass
