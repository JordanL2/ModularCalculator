#!/usr/bin/python3

from modularcalculator.modularcalculator import *
from modularcalculator.interface.display import *
from modularcalculator.interface.guitools import *
from modularcalculator.interface.guiwidgets import *
from modularcalculator.interface.statefulapplication import *
from modularcalculator.interface.textedit import *

import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QSplitter, QAction, QFileDialog
import functools


class ModularCalculatorInterface(StatefulApplication):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initMenu()
        self.restoreAllState()
        self.entry.setFocus()
        self.show()
        self.calcTimer = QTimer()
        self.calcTimer.setSingleShot(True)
        self.calcTimer.timeout.connect(self.initCalculator)
        self.calcTimer.start(0)

    def initUI(self):
        self.display = CalculatorDisplay()

        self.entry = CalculatorTextEdit(self)

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.display)
        self.splitter.addWidget(self.entry)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 0)

        grid = QGridLayout()
        grid.addWidget(self.splitter, 0, 0, 1, 1)
        
        mainWidget = QWidget()
        mainWidget.setLayout(grid)
        self.setCentralWidget(mainWidget)
        self.setWindowTitle('Modular Calculator')

    def initMenu(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('File')
        
        fileOpen = QAction('Open', self)
        fileOpen.triggered.connect(self.open)
        fileMenu.addAction(fileOpen)
        
        fileSave = QAction('Save', self)
        fileSave.triggered.connect(self.save)
        fileMenu.addAction(fileSave)

        viewMenu = menubar.addMenu('View')
        
        viewClear = QAction('Clear', self)
        viewClear.triggered.connect(self.display.clear)
        viewMenu.addAction(viewClear)

        self.viewSingleAction = QAction('Single Mode', self, checkable=True)
        viewMenu.addAction(self.viewSingleAction)
        self.viewSingleAction.triggered.connect(self.setSingleMode)
        self.viewMultiAction = QAction('Multi Mode', self, checkable=True)
        self.viewMultiAction.triggered.connect(self.setMultiMode)
        viewMenu.addAction(self.viewMultiAction)
        
        viewThemeMenu = viewMenu.addMenu('Theme')
        self.themeActions = {}
        for theme in sorted(self.entry.syntax.keys(), key=str.lower):
            themeAction = QAction(theme, self, checkable=True)
            self.themeActions[themeAction] = theme
            themeAction.triggered.connect(functools.partial(self.setTheme, theme))
            viewThemeMenu.addAction(themeAction)
        
        self.viewShortUnits = QAction('Units in Short Form', self, checkable=True)
        self.viewShortUnits.triggered.connect(self.setShortUnits)
        viewMenu.addAction(self.viewShortUnits)
        
        self.viewSyntaxParsingAutoExecutes = QAction('Syntax Parsing Performs Evaluation', self, checkable=True)
        self.viewSyntaxParsingAutoExecutes.triggered.connect(self.setAutoExecute)
        viewMenu.addAction(self.viewSyntaxParsingAutoExecutes)

        insertMenu = menubar.addMenu('Insert')
        
        insertConstant = QAction('Constant', self)
        insertConstant.triggered.connect(self.insertConstant)
        insertMenu.addAction(insertConstant)
        
        insertFunction = QAction('Function', self)
        insertFunction.triggered.connect(self.insertFunction)
        insertMenu.addAction(insertFunction)
        
        insertOperator = QAction('Operator', self)
        insertOperator.triggered.connect(self.insertOperator)
        insertMenu.addAction(insertOperator)
        
        insertUnit = QAction('Unit', self)
        insertUnit.triggered.connect(self.insertUnit)
        insertMenu.addAction(insertUnit)

        optionsMenu = menubar.addMenu('Options')
        
        self.precisionSpinBox = MenuSpinBox(self, 'Precision', 1, 50)
        self.precisionSpinBox.spinbox.valueChanged.connect(self.setPrecision)
        optionsMenu.addAction(self.precisionSpinBox)
        
        self.optionsSimplifyUnits = QAction('Simplify Units', self, checkable=True)
        self.optionsSimplifyUnits.triggered.connect(self.setUnitSimplification)
        optionsMenu.addAction(self.optionsSimplifyUnits)

        self.optionsUnitSystemPreference = QAction('Unit System Preference', self)
        self.optionsUnitSystemPreference.triggered.connect(self.setUnitSystemPreference)
        optionsMenu.addAction(self.optionsUnitSystemPreference)

    def initCalculator(self):
        self.setCalculator(ModularCalculator('Computing'))
        self.restoreCalculatorState()

    def setCalculator(self, calculator):
        self.calculator = calculator
        self.entry.setCalculator(self.calculator)
        self.entry.refresh()

    def restoreAllState(self):
        self.restoreGeometry(self.fetchState("mainWindowGeometry"))
        self.restoreState(self.fetchState("mainWindowState"))
        self.splitter.restoreState(self.fetchState("splitterSizes"))

        self.display.restoreState(self.fetchStateMap("displayOutput"))

        self.multiMode = (self.fetchStateBoolean("multiMode", False))
        self.viewSingleAction.setChecked(not self.multiMode)
        self.viewMultiAction.setChecked(self.multiMode)
        
        self.entry.restoreState(self.fetchStateText("textContent"))
        self.setTheme(self.fetchStateText("theme"))
        
        self.setAutoExecute(self.fetchStateBoolean("viewSyntaxParsingAutoExecutes", True))

        self.setShortUnits(self.fetchStateBoolean("viewShortUnits", False))

    def restoreCalculatorState(self):
        self.setPrecision(self.fetchStateNumber("precision", 30))
        self.setUnitSimplification(self.fetchStateBoolean("simplifyUnits", True))
        unitSystems = self.fetchStateArray("unitSystemsPreference")
        if unitSystems is not None and len(unitSystems) > 0:
            self.calculator.unit_normaliser.systems_preference = unitSystems

    def storeAllState(self):
        self.storeState("mainWindowGeometry", self.saveGeometry())
        self.storeState("mainWindowState", self.saveState())
        self.storeState("splitterSizes", self.splitter.saveState())

        self.storeStateMap("displayOutput", self.display.saveState())
        self.storeStateText("textContent", self.entry.saveState())
        
        self.storeStateBoolean("multiMode", self.multiMode)
        self.storeStateText("theme", self.entry.theme)
        self.storeStateBoolean("viewShortUnits", self.viewShortUnits.isChecked())
        self.storeStateBoolean("viewSyntaxParsingAutoExecutes", self.viewSyntaxParsingAutoExecutes.isChecked())

        self.storeStateNumber("precision", self.precisionSpinBox.spinbox.value())
        self.storeStateBoolean("simplifyUnits", self.optionsSimplifyUnits.isChecked())

        self.storeStateArray("unitSystemsPreference", self.calculator.unit_normaliser.systems_preference)

    def calc(self):
        question = self.entry.getContents().rstrip()
        try:
            if self.multiMode:
                self.calculator.vars = {}
            response = self.calculator.calculate(question)
            if self.multiMode:
                self.display.clear()
            for i, result in enumerate(response.results):
                if hasattr(result, 'value'):
                    self.display.addAnswer(result.expression, self.calculator.number_to_string(result.value), result.unit)
        except CalculatingException as err:
            i = err.find_pos(question)
            row, column = self.rowsColumns(question, i)
            QMessageBox.critical(self, "ERROR", "{0} at row {1}, column {2}".format(err.message, row, column))
        except CalculatorException as err:
            QMessageBox.critical(self, "ERROR", "{0}".format(err.message))

    def rowsColumns(self, text, pos):
        row = 1
        column = 0
        for i in range(0, pos):
            if text[i] == "\n":
                row += 1
                column = 0
            column += 1
        return row, column

    def open(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if filename:
            fh = open(filename, 'r')
            text = str.join("", fh.readlines())
            self.entry.setContents(text)

    def save(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        if filename:
            fh = open(filename, 'w')
            fh.write(self.entry.getContents())

    def setSingleMode(self):
        self.multiMode = False
        self.viewSingleAction.setChecked(True)
        self.viewMultiAction.setChecked(False)

    def setMultiMode(self):
        self.multiMode = True
        self.viewSingleAction.setChecked(False)
        self.viewMultiAction.setChecked(True)

    def setUnitSimplification(self, value):
        self.optionsSimplifyUnits.setChecked(value)
        self.calculator.unit_simplification_set(value)

    def setPrecision(self, value):
        self.precisionSpinBox.spinbox.setValue(value)
        self.calculator.number_prec_set(value)

    def setShortUnits(self, value):
        self.viewShortUnits.setChecked(value)
        self.display.options['shortunits'] = value
        self.display.refresh()

    def setAutoExecute(self, value):
        self.viewSyntaxParsingAutoExecutes.setChecked(value)
        self.entry.autoExecute = value
        self.entry.refresh()

    def setTheme(self, theme):
        if theme in self.entry.syntax:
            self.entry.theme = theme
        self.entry.refresh()
        for themeAction, themeActionTheme in self.themeActions.items():
            themeAction.setChecked(themeActionTheme == self.entry.theme)

    def insertConstant(self):
        constants = sorted(self.calculator.constants.keys(), key=str)
        SelectionDialog(self, 'Insert Constant', 'Select constant to insert', constants, self.selectConstant)

    def selectConstant(self, constant):
        self.entry.insert(constant)

    def insertFunction(self):
        funcs = sorted(self.calculator.funcs.keys(), key=str)
        SelectionDialog(self, 'Insert Function', 'Select function to insert', funcs, self.selectFunction)

    def selectFunction(self, func):
        self.entry.insert(func + '(')

    def insertOperator(self):
        operators = sorted([op for op, opInfo in self.calculator.ops_list.items() if not opInfo.hidden], key=str)
        SelectionDialog(self, 'Insert Operator', 'Select operator to insert', operators, self.selectOperator)

    def selectOperator(self, operator):
        self.entry.insert(operator)

    def insertUnit(self):
        units = sorted([u.singular() for a in self.calculator.unit_normaliser.units.values() for u in a], key=lambda u: u.lower())
        SelectionDialog(self, 'Insert Unit', 'Select unit to insert', units, self.selectUnit)

    def selectUnit(self, unit):
        self.entry.insert(unit)

    def setUnitSystemPreference(self):
        SortableListDialog(self, 
            'Unit System Preference', 
            'Order unit systems by preference, most prefered at top', 
            [self.calculator.unit_normaliser.systems[s].name for s in self.calculator.unit_normaliser.systems_preference], 
            self.updateUnitSystemPreference)

    def updateUnitSystemPreference(self, systemNames):
        self.calculator.unit_normaliser.systems_preference = [s for n in systemNames for s in [s for s in self.calculator.unit_normaliser.systems if self.calculator.unit_normaliser.systems[s].name == n]]


if __name__ == '__main__':
	app = QApplication(sys.argv)
	calc = ModularCalculatorInterface()
	sys.exit(app.exec_())
