#!/usr/bin/python3

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

import html


def htmlSafe(text, breaking=False):
    htmlText = ''

    i = 0
    text_escape = html.escape(str(text))
    for c in text_escape:
        if c == ' ':
            # If this text should line-wrap, replace every other non-breaking space with a normal space
            # so the line wraps, but multiple spaces don't get compacted down to one
            i += 1
            if not breaking or i % 2 == 0:
                c = '&nbsp;'
        else:
            i = 0
            if c == "\n":
                c = '<br/>'
        htmlText += c

    return htmlText

def screenRelativeSize(width, height):
    size = QSize()
    size.setWidth(QApplication.desktop().screenGeometry().width() * width)
    size.setHeight(QApplication.desktop().screenGeometry().height() * height)
    return size

def makeSpan(text, style):
    return "<span class='{0}'>{1}</span>".format(style, text)
