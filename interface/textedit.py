#!/usr/bin/python3

from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.interface.guitools import *

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFontDatabase, QTextCursor


class CalculatorTextEdit(QTextEdit):

    def __init__(self, interface):
        super().__init__()

        self.calculator = None

        editFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        editFont.setBold(True)
        editFont.setPointSize(12)
        self.setFont(editFont)

        self.interface = interface
        self.highlighter = SyntaxHighlighter()
        self.setTheme()
        self.initStyling()
        self.oldText = None

        self.autoExecute = True

    def setCalculator(self, calculator):
        self.calculator = calculator

    def setTheme(self):
        self.syntax = {
            'Light': {
                'error': "color: '#bc0000'",
                'default': "color: '#bc0000'",
                'literal': "color: '#097e00'",
                'unit': "color: '#805f00'",
                'unitsystem': "color: '#805f00'",
                'op': "color: '#0c0c0c'",
                'terminator': "color: '#0c0c0c'",
                'inner_expr_start': "color: '#0c0c0c'",
                'inner_expr_end': "color: '#0c0c0c'",
                'function_name': "color: '#00297f'",
                'function_start': "color: '#0c0c0c'",
                'function_param': "color: '#0c0c0c'",
                'function_end': "color: '#0c0c0c'",
                'ext_function_name': "color: '#00297f'",
                'variable': "color: '#480081'",
                'constant': "color: '#812500'",
                'comment': "color: '#007d80'",
            },
            'Dark': {
                'error': "color: '#cd0d0d'",
                'default': "color: '#cd2727'",
                'literal': "color: '#3ae42d'",
                'unit': "color: '#d7a40e'",
                'unitsystem': "color: '#d7a40e'",
                'op': "color: '#f2f2f2'",
                'terminator': "color: '#f2f2f2'",
                'inner_expr_start': "color: '#f2f2f2'",
                'inner_expr_end': "color: '#f2f2f2'",
                'function_name': "color: '#3577ff'",
                'function_start': "color: '#f2f2f2'",
                'function_param': "color: '#f2f2f2'",
                'function_end': "color: '#f2f2f2'",
                'ext_function_name': "color: '#3577ff'",
                'variable': "color: '#a839ff'",
                'constant': "color: '#ff6629'",
                'comment': "color: '#2ee5e9'",
            },
        }
        value = (self.interface.palette().base().color().value())
        if value < 128:
            self.theme = 'Dark'
        else:
            self.theme = 'Light'

    def initStyling(self):
        self.css = "<style>"
        for itemtype, css in self.syntax[self.theme].items():
            self.css += "span.{0} {{ {1} }}".format(itemtype, css)
        self.css += '</style>'

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Tab:
            spaces = 4 - (self.textCursor().columnNumber() % 4)
            self.insert(' ' * spaces)
        else:
            super().keyPressEvent(e)
        self.checkSyntax()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.checkSyntax()

    def checkSyntax(self, force=False):
        if self.calculator is not None and (self.oldText is None or self.oldText != self.toHtml() or force):
            expr = self.getContents()
            
            self.calculator.vars = {}
            try:
                response = self.calculator.calculate(expr, {'parse_only': not self.autoExecute})
                statements = [r.items for r in response.results]
                i = len(expr)
            except CalculatingException as err:
                statements = err.statements
                i = err.find_pos(expr)
            except CalculatorException as err:
                statements = [[]]
                i = 0

            newhtml = self.css
            highlightItems = self.highlighter.highlight_statements(statements)
            for item in highlightItems:
                style = item[0]
                text = item[1]
                newhtml += "<span class='{0}'>{1}</span>".format(style, htmlSafe(text))
            if i < len(expr):
                newhtml += "<span class='{0}'>{1}</span>".format('error', htmlSafe(expr[i:]))
            self.updateHtml(newhtml)
            
            if not self.interface.filemanager.currentFileModified() and not force:
                self.interface.filemanager.setCurrentFileAndModified(self.interface.filemanager.currentFile(), True)
        self.oldText = self.toHtml()

    def refresh(self):
        self.initStyling()
        self.checkSyntax(True)

    def updateHtml(self, html):
        cursorpos = self.textCursor().position()
        sliderpos = self.verticalScrollBar().sliderPosition()
        self.setHtml(self.css + html)
        cursor = self.textCursor()
        cursor.setPosition(cursorpos)
        self.setTextCursor(cursor)
        self.verticalScrollBar().setSliderPosition(sliderpos)

    def insert(self, text):
        self.insertPlainText(text)
        self.checkSyntax()

    def getContents(self):
        return self.toPlainText()

    def setContents(self, text):
        self.setPlainText(text)
        self.checkSyntax()

    def clearContents(self):
        self.setContents('')

    def saveState(self):
        return {
            'text': self.getContents(),
            'cursorSelectionStart': self.textCursor().selectionStart(),
            'cursorSelectionEnd': self.textCursor().selectionEnd(),
            'sliderPosition': self.verticalScrollBar().sliderPosition(),
        }

    def restoreState(self, state):
        if 'text' in state:
            self.setPlainText(state['text'])
        else:
            self.setPlainText('')
        self.refresh()

        if 'cursorSelectionStart' in state:
            cursor = self.textCursor()
            cursor.setPosition(state['cursorSelectionStart'], QTextCursor.MoveAnchor)
            if 'cursorSelectionEnd' in state:
                cursor.setPosition(state['cursorSelectionEnd'], QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)

        if 'sliderPosition' in state:
            self.verticalScrollBar().setSliderPosition(state['sliderPosition'])
