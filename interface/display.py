#!/usr/bin/python3

from modularcalculator.interface.guitools import *
from modularcalculator.objects.units import *

from PyQt5.QtGui import QFontDatabase, QGuiApplication
from PyQt5.QtWidgets import QTextEdit, QWidget, QGridLayout, QLabel, QVBoxLayout


class CalculatorDisplay(QWidget):

    def __init__(self, interface):
        super().__init__()
        self.layout = QVBoxLayout()
        self.interface = interface
        self.options = {}
        #self.setReadOnly(True)
        self.defaultStyling()
        #self.initStyling()
        self.initOutput()
        self.setLayout(self.layout)

    def defaultStyling(self):
        #self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        qpalette = QGuiApplication.palette()
        self.colours = [ qpalette.base().color().name(), qpalette.alternateBase().color().name() ]
        #self.cssHead = "span.question { font-size: 10pt; } span.answer { font-weight: bold; font-size: 14pt; }"
        #self.cssRow = "div.row{0} {{ background-color: {1} }}"
        #self.answerHtml = "<div class='row{0}'><span class='question'>{1}<br/></span><span class='answer'>{2}{3}</span></div>"

    # def initStyling(self):
    #     self.css = '<style>' + self.cssHead
    #     for i, colour in enumerate(self.colours):
    #         self.css += self.cssRow.format(i, colour)
    #     self.css += '</style>'

    def initOutput(self):
        self.output = []
        self.rawOutput = []

    def addAnswer(self, question, answer, unit):
        self.rawOutput.append(((question, answer, unit)))
        #answerline = self.renderAnswer(question, answer, unit, len(self.output))
        #self.output.append(answerline)
        self.refresh()

    def renderAnswer(self, question, answer, unit, n):
        question = question.strip()
        questionHtml = self.questionHtml(question)
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
        #return self.answerHtml.format(n % len(self.colours), questionHtml, htmlSafe(answer), htmlSafe(unit))
        questionDiv = "<div background-color: \"{}\">{}</div>".format(self.colours[n % len(self.colours)], questionHtml)

        layout = QGridLayout()

        questionWidget = QTextEdit()
        questionWidget.setReadOnly(True)
        questionFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        questionFont.setPointSize(10)
        questionWidget.setFont(questionFont)
        questionWidget.setHtml(questionDiv)
        layout.addWidget(questionWidget, 0, 0, 1, 1)

        answerWidget = QLabel(str(answer))
        answerFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        answerFont.setPointSize(14)
        answerWidget.setFont(answerFont)
        layout.addWidget(answerWidget, 1, 0, 1, 1)
        
        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def questionHtml(self, expr):
        statements, _, _ = self.interface.calculatormanager.calculator.parse(expr, {})
        html, _ = self.interface.entry.makeHtml(statements, '')
        return html

    def updateOutput(self):
        self.clearLayout(self.layout)

        for widget in self.output:
            self.layout.addWidget(widget)

        #self.setLayout(layout)
        #self.setHtml(self.css + str.join('', self.output))
        #self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

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
            #item.deleteLater()
            #item.
            #del item
            #layout.removeItem(item)

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
