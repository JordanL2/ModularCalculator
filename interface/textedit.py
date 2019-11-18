#!/usr/bin/python3

from modularcalculator.objects.api import *
from modularcalculator.services.syntaxhighlighter import *
from modularcalculator.interface.guitools import *

from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QRunnable
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFontDatabase, QTextCursor, QTextCharFormat, QGuiApplication, QTextFormat

import time
import uuid


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

        self.cached_response = None

        self.history = []
        self.historyPos = 0
        self.historySize = 1000

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
        if len(self.history) > 0:
            self.history[self.historyPos - 1][1] = self.textCursor().position()
        if e.key() == Qt.Key_Tab:
            spaces = 4 - (self.textCursor().columnNumber() % 4)
            self.insert(' ' * spaces)
        elif e.key() == Qt.Key_Z and e.modifiers() & Qt.CTRL:
            self.undo()
        elif e.key() == Qt.Key_Y and e.modifiers() & Qt.CTRL:
            self.redo()
        else:
            super().keyPressEvent(e)
        self.checkSyntax()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.checkSyntax()

    def checkSyntax(self, force=False, undo=False):
        if self.calculator is not None and (force or undo or self.oldText is None or self.oldText != self.toHtml()):
            expr = self.getContents()

            if not undo and (self.oldText is None or self.oldText != self.toHtml()):
                if self.historyPos < len(self.history):
                    del self.history[self.historyPos:]
                self.history.append([expr, None])
                if len(self.history) > self.historySize:
                    self.history.pop(0)
                self.historyPos = len(self.history)

            if len(expr) > 0 and expr[-1] != "\n":
                expr += "\n"

            newResponse = CalculatorResponse()
            i = 0
            ii = None
            if self.cached_response is not None and not force:
                for result in self.cached_response.results:
                    if expr[i:].startswith(result.expression):
                        newResponse.results.append(result)
                        i += len(result.expression)
                    else:
                        break
                if len(newResponse.results) > 0 and len(newResponse.results) == len(self.cached_response.results):
                    i -= len(newResponse.results[-1].expression)
                    del newResponse.results[-1]

            self.last_uuid = uuid.uuid4()
            worker = SyntaxHighlighterWorker(self.calculator, self.autoExecute, expr, newResponse, i, ii, self.last_uuid)
            worker.signals.result.connect(self.finishSyntaxHighlighting)
            worker.setAutoDelete(True)
            self.interface.threadpool.clear()
            self.interface.threadpool.start(worker)

    def finishSyntaxHighlighting(self, result):
        expr = result['expr']
        newResponse = result['response']
        error_statements = result['error_statements']
        ii = result['ii']

        if result['uuid'] != self.last_uuid:
            return

        self.cached_response = newResponse

        statements = [r.items for r in newResponse.results] + error_statements
        errorExpr = expr[ii:]
        newhtml, highlightPositions = self.makeHtml(statements, errorExpr)
        self.updateHtml(newhtml)

        extraSelections = []
        for pos in highlightPositions:
            selection = QTextEdit.ExtraSelection()

            selection.cursor = QTextCursor(self.document())
            selection.cursor.setPosition(pos[0])
            selection.cursor.setPosition(pos[1], QTextCursor.KeepAnchor)

            background = QGuiApplication.palette().alternateBase().color()
            selection.format.setBackground(background)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)

            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

        self.interface.filemanager.setCurrentFileAndModified(self.interface.filemanager.currentFile(), self.isModified())

        self.oldText = self.toHtml()

    def makeHtml(self, statements, errorExpr):
        splitStatements = []
        for items in statements:
            funcItems = [i for i, item in enumerate(items) if item.functional() and not item.text.strip() == '']
            if len(funcItems) == 0:
                splitStatements.append(items)
            else:
                nonEmptyItems = [i for i, item in enumerate(items) if not item.text.strip() == '']
                firstNonEmptyItem = min(nonEmptyItems)
                if firstNonEmptyItem > 0:
                    splitStatements.append(items[0:firstNonEmptyItem])
                splitStatements.append(items[firstNonEmptyItem:])

        compactedStatements = []
        foundFunctional = False
        for items in splitStatements:
            functional = len(functional_items(items)) > 0
            isEmpty = len([i for i in items if i.text.strip() != '']) == 0
            if not isEmpty and foundFunctional:
                foundFunctional = False
                compactedStatements.append([])
            if len(compactedStatements) == 0:
                compactedStatements.append([])
            compactedStatements[-1].extend(items)
            if functional:
                foundFunctional = True

        newhtml = self.css
        highlightStatements = self.highlighter.highlight_statements(compactedStatements)
        alternate = True
        p = 0
        highlightPositions = []
        for highlightItems in highlightStatements:
            alternate = not alternate
            p0 = p

            for item in highlightItems:
                style = item[0]
                text = item[1]
                newhtml += "<span class='{0}'>{1}</span>".format(style, htmlSafe(text))
                p += len(text)

            if alternate:
                highlightPositions.append((p0, p))

        if errorExpr != '':
            newhtml += "<span class='{0}'>{1}</span>".format('error', htmlSafe(errorExpr))

        return newhtml, highlightPositions

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

    def setContents(self, text, undo=False):
        self.setPlainText(text)
        self.checkSyntax(False, undo)

    def undo(self):
        if self.historyPos > 1:
            sliderpos = self.verticalScrollBar().sliderPosition()
            
            self.historyPos -= 1
            (expr, cursorpos) = self.history[self.historyPos - 1]
            if self.historyPos > 1:
                self.oldText = self.history[self.historyPos - 2]
            else:
                self.oldText = None
            self.setContents(expr, True)
            
            if cursorpos is not None:
                cursor = self.textCursor()
                cursor.setPosition(cursorpos)
                self.setTextCursor(cursor)
            self.verticalScrollBar().setSliderPosition(sliderpos)

    def redo(self):
        if self.historyPos < len(self.history):
            sliderpos = self.verticalScrollBar().sliderPosition()
            
            self.historyPos += 1
            (expr, cursorpos) = self.history[self.historyPos - 1]
            self.oldText = self.history[self.historyPos - 2]
            self.setContents(expr, True)
            
            if cursorpos is not None:
                cursor = self.textCursor()
                cursor.setPosition(cursorpos)
                self.setTextCursor(cursor)
            self.verticalScrollBar().setSliderPosition(sliderpos)

    def clearContents(self):
        self.setContents('')

    def setOriginal(self, original=None):
        if original is None:
            original = self.getContents()
        self.original = original

    def isModified(self):
        return self.getContents() != self.original

    def saveState(self):
        return {
            'text': self.getContents(),
            'original': self.original,
            'cursorSelectionStart': self.textCursor().selectionStart(),
            'cursorSelectionEnd': self.textCursor().selectionEnd(),
            'sliderPosition': self.verticalScrollBar().sliderPosition(),
        }

    def restoreState(self, state):
        if 'text' in state:
            self.setPlainText(state['text'])
        else:
            self.setPlainText('')
        if 'original' in state:
            self.setOriginal(state['original'])
        else:
            self.setOriginal()
        self.refresh()

        if 'cursorSelectionStart' in state:
            cursor = self.textCursor()
            cursor.setPosition(state['cursorSelectionStart'], QTextCursor.MoveAnchor)
            if 'cursorSelectionEnd' in state:
                cursor.setPosition(state['cursorSelectionEnd'], QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)

        if 'sliderPosition' in state:
            self.verticalScrollBar().setSliderPosition(state['sliderPosition'])


class SyntaxHighlighterSignals(QObject):

    result = pyqtSignal(dict)


class SyntaxHighlighterWorker(QRunnable):

    def __init__(self, calculator, autoExecute, expr, response, i, ii, uuid):
        super(SyntaxHighlighterWorker, self).__init__()
        
        self.signals = SyntaxHighlighterSignals() 

        self.calculator = calculator
        self.autoExecute = autoExecute
        self.expr = expr
        self.response = response
        self.i = i
        self.ii = ii
        self.uuid = uuid

    @pyqtSlot()
    def run(self):
        expr = self.expr
        response = self.response
        i = self.i
        ii = self.ii
        error_statements = []

        self.calculator.update_engine_prec()

        try:
            if len(response.results) > 0:
                self.calculator.vars = response.results[-1].state.copy()
            else:
                self.calculator.vars = {}
            calcResponse = self.calculator.calculate(expr[i:], {'parse_only': not self.autoExecute, 'include_state': True})
            response.results.extend(calcResponse.results)
            ii = len(expr)
        except CalculatingException as err:
            response.results.extend(err.response.results)
            error_statements = err.statements[len(err.response.results):]
            err.statements = [r.items for r in response.results] + error_statements
            ii = err.find_pos(expr)
        except CalculatorException as err:
            ii = i
        
        self.signals.result.emit({
            'expr': expr,
            'response': response,
            'error_statements': error_statements,
            'ii': ii,
            'uuid': self.uuid,
            })
