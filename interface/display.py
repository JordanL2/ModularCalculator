#!/usr/bin/python3

from modularcalculator.interface.guitools import *
from modularcalculator.objects.units import *

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFontDatabase, QGuiApplication


class CalculatorDisplay(QTextEdit):

    def __init__(self):
        super().__init__()
        self.options = {}
        self.setReadOnly(True)
        self.defaultStyling()
        self.initStyling()
        self.initOutput()

    def defaultStyling(self):
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        qpalette = QGuiApplication.palette()
        self.colours = [ qpalette.base().color().name(), qpalette.alternateBase().color().name() ]
        self.cssHead = "span.question { font-size: 10pt; } span.answer { font-weight: bold; font-size: 14pt; }"
        self.cssRow = "div.row{0} {{ background-color: {1} }}"
        self.answerHtml = "<div class='row{0}'><span class='question'>{1}<br/></span><span class='answer'>{2}{3}</span></div>"

    def initStyling(self):
        self.css = '<style>' + self.cssHead
        for i, colour in enumerate(self.colours):
            self.css += self.cssRow.format(i, colour)
        self.css += '</style>'

    def initOutput(self):
        self.output = []
        self.rawOutput = []

    def addAnswer(self, question, answer, unit):
        self.rawOutput.append(((question, answer, unit)))
        answerline = self.renderAnswer(question, answer, unit, len(self.output))
        self.output.append(answerline)
        self.updateOutput()

    def renderAnswer(self, question, answer, unit, n):
        question = question.strip()
        question = question.rstrip(';')
        if isinstance(answer, UnitPowerList):
            if self.options['shortunits']:
                answer = answer.symbol()
            else:
                answer = answer.singular()
        if unit is not None:
            if self.options['shortunits']:
                unit = unit.symbol()
            else:
                unit = unit.get_name(Decimal(answer))
                unit = ' ' + unit
        else:
            unit = ''
        return self.answerHtml.format(n % len(self.colours), htmlSafe(question), htmlSafe(answer), htmlSafe(unit))

    def updateOutput(self):
        self.setHtml(self.css + str.join('', self.output))
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

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
