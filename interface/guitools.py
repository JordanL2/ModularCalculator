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
