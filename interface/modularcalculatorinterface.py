#!/usr/bin/python3

from modularcalculator.modularcalculator import *
from modularcalculator.interface.display import *
from modularcalculator.interface.featureconfig import *
from modularcalculator.interface.featureoptions import *
from modularcalculator.interface.guitools import *
from modularcalculator.interface.guiwidgets import *
from modularcalculator.interface.statefulapplication import *
from modularcalculator.interface.textedit import *

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeySequence, QCursor
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QSplitter, QAction, QFileDialog, QToolTip

import functools
import os.path
import string
import sys
import traceback


class ModularCalculatorInterface(StatefulApplication):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initMenu()
        self.initCalculator()
        self.restoreAllState()
        self.entry.setFocus()
        self.show()

    def initUI(self):
        self.display = CalculatorDisplay(self)

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
        
        fileSaveAs = QAction('Save As...', self)
        fileSaveAs.triggered.connect(self.saveAs)
        fileSaveAs.setShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_S))
        self.fileMenu.addAction(fileSaveAs)

        viewMenu = menubar.addMenu('View')
        
        self.viewShortUnits = QAction('Units in Short Form', self, checkable=True)
        self.viewShortUnits.triggered.connect(self.setShortUnits)
        viewMenu.addAction(self.viewShortUnits)
        
        self.viewSyntaxParsingAutoExecutes = QAction('Syntax Parsing Performs Evaluation', self, checkable=True)
        self.viewSyntaxParsingAutoExecutes.triggered.connect(self.setAutoExecute)
        viewMenu.addAction(self.viewSyntaxParsingAutoExecutes)

        actionMenu = menubar.addMenu('Insert')
        
        insertConstant = QAction('Constant', self)
        insertConstant.triggered.connect(self.insertConstant)
        actionMenu.addAction(insertConstant)
        
        insertDate = QAction('Date && Time', self)
        insertDate.triggered.connect(self.insertDate)
        actionMenu.addAction(insertDate)
        
        insertUnit = QAction('Unit', self)
        insertUnit.triggered.connect(self.insertUnit)
        actionMenu.addAction(insertUnit)
        
        insertOperator = QAction('Operator', self)
        insertOperator.triggered.connect(self.insertOperator)
        actionMenu.addAction(insertOperator)
        
        insertFunction = QAction('Function', self)
        insertFunction.triggered.connect(self.insertFunction)
        actionMenu.addAction(insertFunction)
        
        insertUserDefinedFunction = QAction('User-Defined Function', self)
        insertUserDefinedFunction.triggered.connect(self.insertUserDefinedFunction)
        actionMenu.addAction(insertUserDefinedFunction)

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

        self.optionsNumericalAnswerFormat = QAction('Numerical Result Format', self)
        self.optionsNumericalAnswerFormat.triggered.connect(self.setNumericalAnswerFormat)
        optionsMenu.addAction(self.optionsNumericalAnswerFormat)

        self.optionsResetNumericalAnswerFormat = QAction('', self)
        self.optionsResetNumericalAnswerFormat.triggered.connect(self.setNumberFormatFunction)
        self.optionsResetNumericalAnswerFormat.setVisible(False)
        optionsMenu.addAction(self.optionsResetNumericalAnswerFormat)

        self.optionsFeatureConfig = QAction('Install/Remove Features', self)
        self.optionsFeatureConfig.triggered.connect(self.openFeatureConfig)
        optionsMenu.addAction(self.optionsFeatureConfig)

        self.optionsFeatureOptions = QAction('Feature Options', self)
        self.optionsFeatureOptions.triggered.connect(self.openFeatureOptions)
        optionsMenu.addAction(self.optionsFeatureOptions)

        self.executeAction = QAction('Execute', self)
        self.executeAction.triggered.connect(self.calc)
        self.executeAction.hovered.connect(self.showExecuteToolTip)
        menubar.addAction(self.executeAction)
        self.executeAction.setShortcuts([QKeySequence(Qt.CTRL + Qt.Key_Enter), QKeySequence(Qt.CTRL + Qt.Key_Return)])

    def showExecuteToolTip(self):
        QToolTip.showText(QCursor.pos(), "Ctrl+Enter", self)

    def initCalculator(self):
        calculator = ModularCalculator()
        calculator.enable_units()
        self.setCalculator(calculator)

    def setCalculator(self, calculator):
        self.calculator = calculator
        self.entry.setCalculator(self.calculator)

    def importFeature(self, filePath):
        try:
            featureIds = self.calculator.import_feature_file(filePath)
            self.importedFeatures.append(filePath)
        except Exception as err:
            return e

    def replaceCalculator(self, calculator):
        calculator.number_prec_set(self.calculator.number_prec_get())
        calculator.unit_simplification_set(self.calculator.unit_simplification_get())
        calculator.unit_normaliser.systems_preference = self.calculator.unit_normaliser.systems_preference
        if self.calculator.number_auto_func is not None:
            calculator.number_auto_func_set(calculator.funcs[self.calculator.number_auto_func.func])
        self.setCalculator(calculator)

    def setNumberFormatFunction(self, func=None):
        if func is None or func == False or func == '':
            self.calculator.number_auto_func_set(None)
            self.optionsNumericalAnswerFormat.setVisible(True)
            self.optionsResetNumericalAnswerFormat.setVisible(False)
        else:
            self.calculator.number_auto_func_set(self.calculator.funcs[func])
            self.optionsNumericalAnswerFormat.setVisible(False)
            self.optionsResetNumericalAnswerFormat.setVisible(True)
            self.optionsResetNumericalAnswerFormat.setText("Reset Numerical Result Format ({})".format(func))

    def restoreAllState(self):
        try:
            self.importedFeatures = self.fetchStateArray("importedFeatures")
            self.restoreCalculatorState()

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
            print(traceback.format_exc())

    def restoreCalculatorState(self):
        foundImportedFeatures = []
        for featureFile in self.importedFeatures:
            try:
                self.calculator.import_feature_file(featureFile)
                foundImportedFeatures.append(featureFile)
            except Exception as err:
                print("!!! Couldn't import {} - {} !!!".format(featureFile, err))
        self.importedFeatures = foundImportedFeatures

        features = self.fetchStateArray("calculatorFeatures")
        if features is not None and len(features) > 0:
            self.calculator.install_features(features, False, True)
        else:
            self.calculator.load_preset('Computing')

        self.setPrecision(self.fetchStateNumber("precision", 30))
        self.setUnitSimplification(self.fetchStateBoolean("simplifyUnits", True))
        unitSystems = self.fetchStateArray("unitSystemsPreference")
        if unitSystems is not None and len(unitSystems) > 0:
            self.calculator.unit_normaliser.systems_preference = unitSystems
        self.setNumberFormatFunction(self.fetchStateText("numericalAnswerFormat"))

    def storeAllState(self):
        self.storeStateArray("importedFeatures", list(set(self.importedFeatures)))
        self.storeCalculatorState()

        self.storeState("mainWindowGeometry", self.saveGeometry())
        self.storeState("mainWindowState", self.saveState())
        self.storeState("splitterSizes", self.splitter.saveState())

        self.storeStateMap("displayOutput", self.display.saveState())
        self.storeStateText("textContent", self.entry.saveState())
        
        self.storeStateText("currentFile", self.currentFile)
        self.storeStateBoolean("currentFileModified", self.currentFileModified)
        
        self.storeStateBoolean("viewShortUnits", self.viewShortUnits.isChecked())
        self.storeStateBoolean("viewSyntaxParsingAutoExecutes", self.viewSyntaxParsingAutoExecutes.isChecked())

    def storeCalculatorState(self):
        self.storeStateArray("calculatorFeatures", self.calculator.installed_features)
        self.storeStateNumber("precision", self.precisionSpinBox.spinbox.value())
        self.storeStateBoolean("simplifyUnits", self.optionsSimplifyUnits.isChecked())
        self.storeStateArray("unitSystemsPreference", self.calculator.unit_normaliser.systems_preference)
        if self.calculator.number_auto_func is not None:
            self.storeStateText("numericalAnswerFormat", self.calculator.number_auto_func.func)
        else:
            self.storeStateText("numericalAnswerFormat", None)

    def calc(self):
        question = self.entry.getContents().rstrip()
        try:
            self.calculator.vars = {}
            response = self.calculator.calculate(question)
            if len(response.results) > 1:
                self.display.clear()
            for i, result in enumerate(response.results):
                if hasattr(result, 'value'):
                    result_value = result.value
                    result_value = self.calculator.number_to_string(result_value)
                    self.display.addAnswer(result.expression, result_value, result.unit)
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

    def getAllFunctions(self, condition=None):
        funcs = {}
        descriptions = {}
        for func, funcInfo in self.calculator.funcs.items():
            if condition is None or condition(funcInfo):
                category = funcInfo.category
                if category not in funcs:
                    funcs[category] = []
                funcs[category].append(func)
                descriptions[func] = "{}\n{}({})".format(funcInfo.description, func, ', '.join(funcInfo.syntax))
        return funcs, descriptions

    def insertFunction(self):
        funcs, descriptions = self.getAllFunctions()
        CategorisedSelectionDialog(self, 'Insert Function', 'Select function to insert', funcs, descriptions, self.selectFunction)

    def selectFunction(self, func):
        funcInfo = self.calculator.funcs[func]
        self.entry.insert("{}({})".format(func, ', '.join(funcInfo.syntax)))

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
        operators = {}
        descriptions = {}
        for op, opInfo in self.calculator.ops_list.items():
            if not opInfo.hidden:
                category = opInfo.category
                if category not in operators:
                    operators[category] = []
                operators[category].append(op)
                descriptions[op] = "{}\n{}".format(opInfo.description, ' '.join(opInfo.syntax))
        CategorisedSelectionDialog(self, 'Insert Operator', 'Select operator to insert', operators, descriptions, self.selectOperator)

    def selectOperator(self, operator):
        self.entry.insert(operator)

    def insertUnit(self):
        units = {}
        descriptions = {}
        for dimension in self.calculator.unit_normaliser.units:
            dimensionTitle = self.calculator.unit_normaliser.dimensions[dimension]
            units[dimensionTitle] = []
            for unit in self.calculator.unit_normaliser.units[dimension]:
                unitName = unit.singular()
                units[dimensionTitle].append(unitName)
                altnames = []
                for name in unit.names() + unit.symbols():
                    if name not in altnames and name != unitName:
                        altnames.append(name)
                altnames = ', '.join(altnames)
                if unit.systems is None or len(unit.systems) == 0:
                    unitsystem = 'No unit system'
                else:
                    unitsystem = self.calculator.unit_normaliser.systems[self.calculator.unit_normaliser.get_preferred_system(unit.systems)].name
                descriptions[unitName] = "{}.\nAlternative names: {}".format(unitsystem, altnames)
        CategorisedSelectionDialog(self, 'Insert Unit', 'Select unit to insert', units, descriptions, self.selectUnit)

    def selectUnit(self, unit):
        self.entry.insert(unit)

    def setUnitSystemPreference(self):
        SortableListDialog(self, 
            'Unit System Preference', 
            'Order unit systems by preference, most prefered at top', 
            [self.calculator.unit_normaliser.systems[s].name for s in self.calculator.unit_normaliser.systems_preference if s in self.calculator.unit_normaliser.systems]
            + [self.calculator.unit_normaliser.systems[s].name for s in self.calculator.unit_normaliser.systems if s not in self.calculator.unit_normaliser.systems_preference], 
            self.updateUnitSystemPreference)

    def updateUnitSystemPreference(self, systemNames):
        self.calculator.unit_normaliser.systems_preference = [s for n in systemNames for s in [s for s in self.calculator.unit_normaliser.systems if self.calculator.unit_normaliser.systems[s].name == n]]

    def setNumericalAnswerFormat(self):
        funcs, descriptions = self.getAllFunctions(lambda f : f.minparams == 1 and len(f.value_restrictions) > 0 and 'number' in f.value_restrictions[0]['objtypes'])
        CategorisedSelectionDialog(self, 'Select Result Format', 'Select function to format numerical results', funcs, descriptions, self.setNumberFormatFunction)

    def openFeatureConfig(self):
        FeatureConfigDialog(self)

    def commitFeatureConfig(self, calculator, importedFeatures):
        try:
            self.replaceCalculator(calculator)
            self.importedFeatures = importedFeatures
        except Exception:
            errorMessage = QMessageBox(self)
            errorMessage.setText("Could not instantiate calculator with selected features")
            errorMessage.exec()
            print(traceback.format_exc())
        self.entry.refresh()

    def openFeatureOptions(self):
        FeatureOptionsDialog(self)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	calc = ModularCalculatorInterface()
	sys.exit(app.exec_())
