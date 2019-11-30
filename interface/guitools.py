#!/usr/bin/python3

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

import html


def htmlSafe(text):
    return html.escape(str(text)).replace("\n", '<br/>').replace(' ', '&nbsp;')

def screenRelativeSize(width, height):
    size = QSize()
    size.setWidth(QApplication.desktop().screenGeometry().width() * width)
    size.setHeight(QApplication.desktop().screenGeometry().height() * height)
    return size

def makeSpan(text, style, breaking=False):
    html = []
    i = 0
    for c in str(text):
        c = htmlSafe(c)
        if breaking and c == '&nbsp;':
            # If this text should line-wrap, replace every other non-breaking space with a normal space
            # so the line wraps, but multiple spaces don't get compacted down to one
            i += 1
            if i % 2 == 0:
                c = ' '
        html.append("<span class='{0}'>{1}</span>".format(style, c))
    return ''.join(html)
