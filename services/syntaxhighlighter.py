#!/usr/bin/python3

from modularcalculator.objects.exceptions import *
from modularcalculator.objects.items import *

import re


class SyntaxHighlighter:
    
    defaulttype = 'default'

    def highlight_statements(self, statements):
        highlightItems = []
        for items in statements:
            statementtext = ''.join([item.text for item in items])
            highlightItems.extend(self.highlight(statementtext, items))
        return highlightItems

    def highlight(self, text, items):
        highlight = []

        i = 0
        prev_item = None
        for item in items:
            itemtext = item.text
            ii = text.find(itemtext, i)
            if ii == -1:
                raise CalculatorException("Could not find {0} in {1} after character {2}".format(itemtext, text, i))
            if i != ii:
                if prev_item is None or not prev_item.truncated:
                    print("Error in", text, "- Unexpected characters at", i, "- (" + text[i:ii] + ")")
                    for item2 in items:
                        print("Item:", "|" + item2.text + "|")
                    print("End of items.\n")
                highlight.append((self.defaulttype, text[i:ii]))
                i = ii
            itemtype = item.desc()
            if isinstance(item, RecursiveOperandItem):
                inner_highlight = self.highlight(itemtext, item.items)
                highlight.extend(inner_highlight)
            else:
                highlight.append((itemtype, itemtext))
            i += len(itemtext)
            prev_item = item
        if i < len(text):
            print("Error in", text, "- Unexpected characters at", i, "- (" + text[i:] + ")")
            highlight.append((self.defaulttype, text[i:]))

        return highlight
