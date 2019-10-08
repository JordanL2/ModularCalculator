#!/usr/bin/python3


class CalculatorException(Exception):

    def __init__(self, message):
        self.message = message


class CalculatingException(CalculatorException):

    def __init__(self, message, items, next, truncated=False):
        self.message = message
        self.items = items
        self.next = next
        self.truncated = truncated

    def find_pos(self, text):
        i = 0
        prev_item = None
        for items in self.items:
            for item in items:
                ii = text.find(item.text, i)
                if ii == -1:
                    raise Exception("Could not find item |{}| in text |{}| after position {}".format(item.text, text, i))
                if ii != i:
                    if prev_item is None or not prev_item.truncated:
                        print("Error in", "|" + text + "|", "- Unexpected characters at", i, "- |" + text[i:ii] + "|")
                        for item2 in self.items:
                            print("Item:", "|" + item2.text + "|")
                        print("End of items.\n")
                i = ii + len(item.text)
                prev_item = item
        if self.next is not None:
            ii = text.find(self.next, i)
            if ii == -1:
                raise Exception("Could not find '{0}' in '{1}' after character {2}".format(self.next, text, i))
            i = ii
        return i

    def truncate(self, text):
        i = self.find_pos(text)
        return text[0:i]
    

class ParsingException(CalculatingException):

    pass


class ExecutionException(CalculatingException):

    pass
