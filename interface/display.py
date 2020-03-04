#!/usr/bin/python3

from modularcalculator.interface.guitools import *
from modularcalculator.interface.guiwidgets import *
from modularcalculator.objects.units import *

from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QFontDatabase, QPalette
from PyQt5.QtWidgets import QTextEdit, QWidget, QGridLayout, QSizePolicy, QSpacerItem


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
        self.rawOutput = []

    def clear(self):
        self.initOutput()
        self.refresh()

    def addAnswer(self, question, answer, unit):
        self.rawOutput.append(CalculatorDisplayAnswer(question, answer, unit))

    def addError(self, err, i, question):
        self.rawOutput.append(CalculatorDisplayError(err, i, question))

    def refresh(self):
        self.clearLayout(self.layout)

        for n, row in enumerate(self.rawOutput):
            questionWidget, answerWidget = self.renderAnswer(row, n)
            questionWidget.setPartner(answerWidget)
            answerWidget.setPartner(questionWidget)

            self.layout.addWidget(questionWidget, n, 0, 1, 1)
            self.layout.addWidget(answerWidget, n, 1, 1, 1)

        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Ignored, QSizePolicy.Expanding)
        self.layout.addItem(verticalSpacer, len(self.rawOutput), 0, 1, 2, Qt.AlignTop)

        self.layout.update()

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

    def renderAnswer(self, row, n):
        if isinstance(row, CalculatorDisplayAnswer):
            question = row.question.strip()
            questionHtml = self.questionHtml(question)

            if type(row.answer) == list:
                answerHtml = '['
                answerHtml += ', '.join([self.renderAnswerRow(r.value, r.unit) for r in row.answer])
                answerHtml += ']'
            else:
                answerHtml = self.renderAnswerRow(row.answer, row.unit)

        elif isinstance(row, CalculatorDisplayError):
            questionHtml, _ = self.interface.entry.makeHtml([row.err.statements[-1]], row.question[row.i:])
            answerHtml = makeSpan(htmlSafe(row.err.message), 'error')

        else:
            raise Exception("Unrecognised type in renderAnswer: {}".format(type(row)))

        return self.makeQuestionWidget(questionHtml, n), self.makeAnswerWidget(answerHtml, n)

    def renderAnswerRow(self, answer, unit):
        answer_rendered = None
        if isinstance(answer, UnitPowerList):
            if self.options['shortunits'] and answer.has_symbols():
                unit_parts = answer.symbol(False)
            else:
                unit_parts = answer.singular(False, False)
            answer_rendered = ''.join([makeSpan(htmlSafe(u[0]), u[1]) for u in unit_parts])
        else:
            answer_rendered = makeSpan(htmlSafe(answer), 'literal')
        if unit is not None:
            if self.options['shortunits'] and unit.has_symbols():
                unit_parts = unit.symbol(False)
            else:
                answer_number = self.interface.calculatormanager.calculator.number(answer)[0]
                unit_parts = unit.get_name(answer_number, False)
                unit_parts = [(' ', 'space')] + unit_parts
            unit = ''.join([makeSpan(htmlSafe(u[0]), u[1]) for u in unit_parts])
        else:
            unit = ''
        return self.interface.entry.css + answer_rendered + unit

    def makeQuestionWidget(self, questionHtml, n):
        questionWidget = DisplayLabel2(questionHtml, n, self)
        questionFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        questionFont.setPointSize(10)
        questionWidget.setFont(questionFont)
        return questionWidget

    def makeAnswerWidget(self, answerHtml, n):
        answerWidget = DisplayLabel2(answerHtml, n, self, CalculatorDisplay.insertAnswer)
        answerFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        answerFont.setPointSize(14)
        answerFont.setBold(True)
        answerWidget.setFont(answerFont)
        return answerWidget

    def questionHtml(self, expr):
        statements, _, _ = self.interface.calculatormanager.calculator.parse(expr, {})
        html, _ = self.interface.entry.makeHtml(statements, '')
        return html

    def insertAnswer(self, widget, e):
        self.interface.entry.insert(widget.toPlainText())
        self.interface.entry.setFocus()

    def restoreState(self, state):
        if isinstance(state, dict):
            if 'rawOutput' in state.keys():
                self.rawOutput = state['rawOutput']
        self.refresh()

    def saveState(self):
        return {'rawOutput': self.rawOutput}


class CalculatorDisplayAnswer():

    def __init__(self, question, answer, unit):
        self.question = question
        self.answer = answer
        self.unit = unit


class CalculatorDisplayError():

    def __init__(self, err, i, question):
        self.err = err
        self.i = i
        self.question = question
