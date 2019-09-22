#!/usr/bin/python3

from modularcalculator.modularcalculator import *
from modularcalculator.interface.display import *
from modularcalculator.interface.guitools import *
from modularcalculator.interface.guiwidgets import *
from modularcalculator.interface.statefulapplication import *
from modularcalculator.interface.textedit import *

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QSplitter, QAction, QFileDialog

import functools
import os.path
import string
import sys


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

    def initMenu(self):
        menubar = self.menuBar()
        
        self.fileMenu = menubar.addMenu('File')
        
        fileNew = QAction('New', self)
        fileNew.triggered.connect(self.new)
        fileNew.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_N))
        self.fileMenu.addAction(fileNew)
        
        fileOpen = QAction('Open', self)
        fileOpen.triggered.connect(self.open)
        fileOpen.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_O))
        self.fileMenu.addAction(fileOpen)
        
        self.fileSave = QAction('Save', self)
        self.fileSave.triggered.connect(self.save)
        self.fileSave.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))
        self.fileMenu.addAction(self.fileSave)
        
        fileSaveAs = QAction('Save as...', self)
        fileSaveAs.triggered.connect(self.saveAs)
        fileSaveAs.setShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_S))
        self.fileMenu.addAction(fileSaveAs)

        viewMenu = menubar.addMenu('View')
        
        self.viewShortUnits = QAction('Units in short form', self, checkable=True)
        self.viewShortUnits.triggered.connect(self.setShortUnits)
        viewMenu.addAction(self.viewShortUnits)
        
        self.viewSyntaxParsingAutoExecutes = QAction('Syntax parsing performs evaluation', self, checkable=True)
        self.viewSyntaxParsingAutoExecutes.triggered.connect(self.setAutoExecute)
        viewMenu.addAction(self.viewSyntaxParsingAutoExecutes)

        actionMenu = menubar.addMenu('Action')

        self.executeAction = QAction('Execute', self)
        self.executeAction.triggered.connect(self.calc)
        actionMenu.addAction(self.executeAction)
        self.executeAction.setShortcuts([QKeySequence(Qt.CTRL + Qt.Key_Enter), QKeySequence(Qt.CTRL + Qt.Key_Return)])

        actionMenu.addSeparator()
        
        insertConstant = QAction('Insert constant', self)
        insertConstant.triggered.connect(self.insertConstant)
        actionMenu.addAction(insertConstant)
        
        insertDate = QAction('Insert date && time', self)
        insertDate.triggered.connect(self.insertDate)
        actionMenu.addAction(insertDate)
        
        insertUnit = QAction('Insert unit', self)
        insertUnit.triggered.connect(self.insertUnit)
        actionMenu.addAction(insertUnit)
        
        insertOperator = QAction('Insert operator', self)
        insertOperator.triggered.connect(self.insertOperator)
        actionMenu.addAction(insertOperator)
        
        insertFunction = QAction('Insert function', self)
        insertFunction.triggered.connect(self.insertFunction)
        actionMenu.addAction(insertFunction)
        
        insertUserDefinedFunction = QAction('Insert user-defined function', self)
        insertUserDefinedFunction.triggered.connect(self.insertUserDefinedFunction)
        actionMenu.addAction(insertUserDefinedFunction)

        optionsMenu = menubar.addMenu('Options')
        
        self.precisionSpinBox = MenuSpinBox(self, 'Precision', 1, 50)
        self.precisionSpinBox.spinbox.valueChanged.connect(self.setPrecision)
        optionsMenu.addAction(self.precisionSpinBox)

        self.optionsSimplifyUnits = QAction('Simplify units', self, checkable=True)
        self.optionsSimplifyUnits.triggered.connect(self.setUnitSimplification)
        optionsMenu.addAction(self.optionsSimplifyUnits)

        self.optionsUnitSystemPreference = QAction('Unit system preference', self)
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
        try:
            self.restoreGeometry(self.fetchState("mainWindowGeometry"))
            self.restoreState(self.fetchState("mainWindowState"))
            self.splitter.restoreState(self.fetchState("splitterSizes"))

            self.display.restoreState(self.fetchStateMap("displayOutput"))
            self.entry.restoreState(self.fetchStateText("textContent"))
            
            self.setCurrentFile(self.fetchStateText("currentFile"), self.fetchStateBoolean("currentFileModified", False))
            
            self.setAutoExecute(self.fetchStateBoolean("viewSyntaxParsingAutoExecutes", True))

            self.setShortUnits(self.fetchStateBoolean("viewShortUnits", False))
        except Exception as e:
            print("Exception when trying to restore state")
            print(e)

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
        
        self.storeStateText("currentFile", self.currentFile)
        self.storeStateBoolean("currentFileModified", self.currentFileModified)
        
        self.storeStateBoolean("viewShortUnits", self.viewShortUnits.isChecked())
        self.storeStateBoolean("viewSyntaxParsingAutoExecutes", self.viewSyntaxParsingAutoExecutes.isChecked())

        self.storeStateNumber("precision", self.precisionSpinBox.spinbox.value())
        self.storeStateBoolean("simplifyUnits", self.optionsSimplifyUnits.isChecked())

        self.storeStateArray("unitSystemsPreference", self.calculator.unit_normaliser.systems_preference)

    def calc(self):
        question = self.entry.getContents().rstrip()
        try:
            self.calculator.vars = {}
            response = self.calculator.calculate(question)
            if len(response.results) > 1:
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

    def new(self):
        if self.checkIfNeedToSave():
            return
        self.entry.clearContents()
        self.display.clear()
        self.setCurrentFile(None)

    def open(self):
        if self.checkIfNeedToSave():
            return
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if filePath:
            fh = open(filePath, 'r')
            text = str.join("", fh.readlines())
            self.entry.setContents(text)
            self.setCurrentFile(filePath, False)

    def save(self):
        if self.currentFile is None:
            self.saveAs()
            return
        fh = open(self.currentFile, 'w')
        fh.write(self.entry.getContents())
        self.setCurrentFile(self.currentFile, False)

    def saveAs(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        if filePath:
            fh = open(filePath, 'w')
            fh.write(self.entry.getContents())
            self.setCurrentFile(filePath, False)

    def checkIfNeedToSave(self):
        if self.currentFile is not None and self.currentFileModified:
            response = QMessageBox.question(self, 'Unsaved File', "Save changes to {} before closing?".format(self.currentFile), QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if response == QMessageBox.Yes:
                self.save()
            elif response == QMessageBox.Cancel:
                return True
        return False

    def setCurrentFile(self, file, modified=False):
        self.currentFile = file
        self.currentFileModified = modified
        if self.currentFile is None:
            self.setWindowTitle('Modular Calculator')
        elif self.currentFileModified:
            self.setWindowTitle("Modular Calculator - {} *".format(self.currentFile))
        else:
            self.setWindowTitle("Modular Calculator - {}".format(self.currentFile))

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

    def insertConstant(self):
        constants = sorted(self.calculator.constants.keys(), key=str)
        SelectionDialog(self, 'Insert Constant', 'Select constant to insert', constants, self.selectConstant)

    def selectConstant(self, constant):
        self.entry.insert(constant)

    def insertDate(self):
        DatePicker(self, 'Select Date & Time', self.selectDate)

    def selectDate(self, date, time):
        self.entry.insert("'{0:04d}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}'".format(date.year(), date.month(), date.day(), time.hour(), time.minute(), time.second()))

    def insertFunction(self):
        funcs = sorted(self.calculator.funcs.keys(), key=str)
        SelectionDialog(self, 'Insert Function', 'Select function to insert', funcs, self.selectFunction)

    def selectFunction(self, func):
        self.entry.insert(func + '(')

    def insertUserDefinedFunction(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select user-defined function file", "", "All Files (*)")
        if filePath:
            funcname = os.path.basename(filePath)
            whitelist = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_')
            funcname = ''.join(c for c in funcname if c in whitelist)
            if funcname == '':
                funcname = 'userDefinedFunction'
            if funcname[0] in string.digits:
                funcname = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'][int(funcname[0])] + funcname[1:]
            self.entry.insert("{} = '{}';\n".format(funcname, filePath))

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
