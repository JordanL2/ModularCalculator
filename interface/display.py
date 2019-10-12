#!/usr/bin/python3

from modularcalculator.interface.guitools import *
from modularcalculator.objects.units import *

from PyQt5.QtGui import QFontDatabase, QPalette
from PyQt5.QtWidgets import QTextEdit, QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer


class CalculatorDisplay(QWidget):

    def __init__(self, interface):
        super().__init__()
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.interface = interface
        self.options = {}
        self.defaultStyling()
        self.initOutput()

    def defaultStyling(self):
        self.colours = [ QPalette.Base, QPalette.AlternateBase ]
        self.margin = 10

    def initOutput(self):
        self.output = []
        self.rawOutput = []

    def addAnswer(self, question, answer, unit):
        self.rawOutput.append(((question, answer, unit)))
        self.refresh()

    def renderAnswer(self, question, answer, unit, n):
        question = question.strip()
        questionHtml = self.questionHtml(question)
        questionDiv = "<div background-color: \"{}\">{}</div>".format(self.colours[n % len(self.colours)], questionHtml)

        if isinstance(answer, UnitPowerList):
            if self.options['shortunits']:
                answer = answer.symbol()
            else:
                answer = answer.singular()
        if unit is not None:
            if self.options['shortunits'] and unit.has_symbols():
                unit = unit.symbol()
            else:
                unit = unit.get_name(self.interface.calculatormanager.calculator.number(answer)[0])
                unit = ' ' + unit
        else:
            unit = ''

        questionWidget = QLabel(questionDiv)
        questionFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        questionFont.setPointSize(10)
        questionWidget.setFont(questionFont)
        questionWidget.setBackgroundRole(self.colours[n % len(self.colours)])
        questionWidget.setAutoFillBackground(True)
        questionWidget.setMargin(self.margin)

        answerWidget = QLabel(str(answer) + unit)
        answerFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        answerFont.setPointSize(14)
        answerFont.setBold(True)
        answerWidget.setFont(answerFont)
        answerWidget.setBackgroundRole(self.colours[n % len(self.colours)])
        answerWidget.setAutoFillBackground(True)
        answerWidget.setMargin(self.margin)

        return (questionWidget, answerWidget)

    def countLines(self, text):
        return text.count("\n") + 1

    def questionHtml(self, expr):
        statements, _, _ = self.interface.calculatormanager.calculator.parse(expr, {})
        html, _ = self.interface.entry.makeHtml(statements, '')
        return html

    def updateOutput(self):
        self.clearLayout(self.layout)

        for n, widget in enumerate(self.output):
            self.layout.addWidget(widget[0], n, 0, 1, 1)
            self.layout.addWidget(widget[1], n, 1, 1, 1)

        QTimer.singleShot(1, self.scrollToBottom)

    def clearLayout(self, layout):
        while True:
            item = layout.takeAt(0)
            if item is None:
                break
            if item.widget() is not None:
                widget = item.widget()
                widget.deleteLater()
            if item.layout() is not None:
                childLayout = item.layout()
                self.clearLayout(childLayout)
            del item

    def scrollToBottom(self):
        scrollbar = self.interface.displayScroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear(self):
        self.initOutput()
        self.updateOutput()

    def restoreState(self, state):
        if isinstance(state, dict):
            if 'rawOutput' in state.keys():
                self.rawOutput = state['rawOutput']
        self.updateOutput()

    def saveState(self):
        return {'rawOutput': self.rawOutput}

    def refresh(self):
        self.output = [self.renderAnswer(r[0], r[1], r[2], n) for n, r in enumerate(self.rawOutput)]
        self.updateOutput()
