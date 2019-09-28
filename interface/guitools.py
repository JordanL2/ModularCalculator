#!/usr/bin/python3

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

import cgi


def htmlSafe(text):
    return cgi.escape(str(text)).replace("\n", '<br/>').replace(' ', '&nbsp;')

def screenRelativeSize(width, height):
    size = QSize()
    size.setWidth(QApplication.desktop().screenGeometry().width() * 0.4)
    size.setHeight(QApplication.desktop().screenGeometry().height() * 0.6)
    return size
