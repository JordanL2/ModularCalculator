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
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QSplitter, QAction, QFileDialog, QToolTip, QTabBar, QShortcut

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
        self.initShortcuts()
        self.entry.setFocus()
        self.show()

    def initUI(self):
        self.tabbar = QTabBar(self)
        self.tabbar.setTabsClosable(True)
        self.tabs = []
        self.selectedTab = None

        self.display = CalculatorDisplay(self)

        self.entry = CalculatorTextEdit(self)

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.display)
        self.splitter.addWidget(self.entry)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 0)

        grid = QGridLayout()
        grid.addWidget(self.tabbar, 0, 0, 1, 1)
        grid.addWidget(self.splitter, 1, 0, 1, 1)
        
        mainWidget = QWidget()
        mainWidget.setLayout(grid)
        self.setCentralWidget(mainWidget)

    def initMenu(self):
        menubar = self.menuBar()
        
        self.fileMenu = menubar.addMenu('File')
        
        fileNew = QAction('New Tab', self)
        fileNew.triggered.connect(self.addTab)
        fileNew.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_N))
        self.fileMenu.addAction(fileNew)
        
        fileClose = QAction('Close Tab', self)
        fileClose.triggered.connect(self.closeCurrentTab)
        fileClose.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_W))
        self.fileMenu.addAction(fileClose)

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

    def initShortcuts(self):
        previousTab = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_PageUp), self)
        previousTab.activated.connect(self.previousTab)
        nextTab = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_PageDown), self)
        nextTab.activated.connect(self.nextTab)


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
        for featureId, featureOptions in self.calculator.feature_options.items():
            if featureId in calculator.feature_options:
                calculator.feature_options[featureId] = featureOptions
        self.setCalculator(calculator)


    def restoreAllState(self):
        try:
            self.importedFeatures = self.fetchStateArray("importedFeatures")
            self.restoreCalculatorState()

            self.restoreGeometry(self.fetchState("mainWindowGeometry"))
            self.restoreState(self.fetchState("mainWindowState"))
            self.splitter.restoreState(self.fetchState("splitterSizes"))
            
            self.setAutoExecute(self.fetchStateBoolean("viewSyntaxParsingAutoExecutes", True), False)
            self.setShortUnits(self.fetchStateBoolean("viewShortUnits", False), False)

            self.restoreTabs()
        except Exception as e:
            print("Exception when trying to restore state")
            print(traceback.format_exc())

    def restoreTabs(self):
        self.tabs = self.fetchStateArray("tabs")
        if len(self.tabs) > 0:
            for tab in self.tabs:
                tabfile = self.getTabName(tab['currentFile'], tab['currentFileModified'])
                self.tabbar.addTab(tabfile)
            self.selectedTab = self.fetchStateNumber("selectedTab")
            if self.selectedTab is None:
                self.loadTab(0)
            else:
                self.loadTab(self.selectedTab)
                self.tabbar.setCurrentIndex(self.selectedTab)
        else:
            self.addTab()
            self.loadTab(0)
        self.tabbar.currentChanged.connect(self.selectTab)
        self.tabbar.tabCloseRequested.connect(self.closeTab)

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

        featureOptions = self.fetchStateMap("calculatorFeatureOptions")
        for featureId, featuresOptions in featureOptions.items():
            for field, value in featuresOptions.items():
                if field in self.calculator.feature_list[featureId].default_options():
                    self.calculator.feature_options[featureId][field] = value

    def storeAllState(self):
        self.storeStateArray("importedFeatures", list(set(self.importedFeatures)))
        self.storeCalculatorState()

        self.storeState("mainWindowGeometry", self.saveGeometry())
        self.storeState("mainWindowState", self.saveState())
        self.storeState("splitterSizes", self.splitter.saveState())

        self.storeSelectedTab()
        self.storeStateArray("tabs", self.tabs)
        self.storeStateNumber("selectedTab", self.selectedTab)
        
        self.storeStateBoolean("viewShortUnits", self.viewShortUnits.isChecked())
        self.storeStateBoolean("viewSyntaxParsingAutoExecutes", self.viewSyntaxParsingAutoExecutes.isChecked())

    def storeCalculatorState(self):
        self.storeStateArray("calculatorFeatures", self.calculator.installed_features)
        self.storeStateNumber("precision", self.precisionSpinBox.spinbox.value())
        self.storeStateBoolean("simplifyUnits", self.optionsSimplifyUnits.isChecked())
        self.storeStateArray("unitSystemsPreference", self.calculator.unit_normaliser.systems_preference)

        self.storeStateMap("calculatorFeatureOptions", self.calculator.feature_options)


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


    def getTabName(self, currentFile, currentFileModified):
        if currentFile is None:
            return '(untitled)'
        tabName = currentFile
        if currentFileModified:
            tabName += ' *'
        return tabName

    def addTab(self):
        self.tabs.append({
            'entry': {}, 
            'display': {'rawOutput': []}, 
            'currentFile': None, 
            'currentFileModified': False
        })
        self.tabbar.addTab(self.getTabName(None, None))
        self.tabbar.setCurrentIndex(len(self.tabs) - 1)

    def storeSelectedTab(self):
        if self.selectedTab is not None:
            i = self.selectedTab
            self.tabs[i]['entry'] = self.entry.saveState()
            self.tabs[i]['display'] = self.display.saveState()

    def selectTab(self, i):
        self.storeSelectedTab()
        self.loadTab(i)

    def loadTab(self, i):
        self.selectedTab = i
        self.entry.restoreState(self.tabs[i]['entry'])
        self.display.restoreState(self.tabs[i]['display'])
        self.display.refresh()
        self.setCurrentFileAndModified(self.tabs[i]['currentFile'], self.tabs[i]['currentFileModified'])

    def closeTab(self, i):
        if self.checkIfNeedToSave(i):
            return
        
        self.storeSelectedTab()
        self.tabbar.blockSignals(True)

        self.tabs.pop(i)
        self.tabbar.removeTab(i)
        if self.selectedTab >= i:
            self.selectedTab -= 1
            if self.selectedTab < 0:
                self.selectedTab = 0
            if len(self.tabs) == 0:
                self.addTab()
            self.loadTab(self.selectedTab)

        self.tabbar.setCurrentIndex(self.selectedTab)
        self.tabbar.blockSignals(False)

    def closeCurrentTab(self):
        self.closeTab(self.selectedTab)

    def previousTab(self):
        i = self.selectedTab
        if i == 0:
            i = len(self.tabs)
        i -= 1
        self.selectTab(i)
        self.tabbar.setCurrentIndex(i)

    def nextTab(self):
        i = self.selectedTab
        i += 1
        if i == len(self.tabs):
            i = 0
        self.selectTab(i)
        self.tabbar.setCurrentIndex(i)


    def currentFile(self, i=None):
        if i is None:
            i = self.selectedTab
        return self.tabs[i]['currentFile']

    def currentFileModified(self, i=None):
        if i is None:
            i = self.selectedTab
        return self.tabs[i]['currentFileModified']

    def setCurrentFile(self, currentFile, i=None):
        if i is None:
            i = self.selectedTab
        self.tabs[i]['currentFile'] = currentFile

    def setCurrentFileModified(self, currentFileModified, i=None):
        if i is None:
            i = self.selectedTab
        self.tabs[i]['currentFileModified'] = currentFileModified

    def setCurrentFileAndModified(self, file, modified=False, i=None):
        self.setCurrentFile(file, i)
        self.setCurrentFileModified(modified, i)
        if i is None or i == self.selectedTab:
            if self.currentFile() is None:
                self.setWindowTitle('Modular Calculator')
            else:
                fileName = self.currentFile()
                if self.currentFileModified():
                    fileName += ' *'
                self.setWindowTitle("Modular Calculator - {}".format(fileName))
                self.tabbar.setTabText(self.selectedTab, fileName)

    def open(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if filePath:
            self.addTab()
            fh = open(filePath, 'r')
            text = str.join("", fh.readlines())
            self.entry.setContents(text)
            self.setCurrentFileAndModified(filePath, False)

    def save(self, i=None):
        if i == False:
            i = None
        if self.currentFile(i) is None:
            self.saveAs(i)
            return
        fh = open(self.currentFile(i), 'w')
        fh.write(self.getEntryContents(i))
        self.setCurrentFileAndModified(self.currentFile(), False, i)

    def saveAs(self, i=None):
        if i == False:
            i = None
        filePath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        if filePath:
            fh = open(filePath, 'w')
            fh.write(self.getEntryContents(i))
            self.setCurrentFileAndModified(filePath, False, i)

    def checkIfNeedToSave(self, i=None):
        if self.currentFile(i) is not None and self.currentFileModified(i):
            response = QMessageBox.question(self, 'Unsaved File', "Save changes to {} before closing?".format(self.currentFile()), QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if response == QMessageBox.Yes:
                self.save(i)
            elif response == QMessageBox.Cancel:
                return True
        return False

    def getEntryContents(self, i=None):
        self.storeSelectedTab()
        if i is None:
            i = self.selectedTab
        return self.tabs[i]['entry']['text']


    def setUnitSimplification(self, value):
        self.optionsSimplifyUnits.setChecked(value)
        self.calculator.unit_simplification_set(value)

    def setPrecision(self, value):
        self.precisionSpinBox.spinbox.setValue(value)
        self.calculator.number_prec_set(value)

    def setShortUnits(self, value, refresh=True):
        self.viewShortUnits.setChecked(value)
        self.display.options['shortunits'] = value
        if refresh:
            self.display.refresh()

    def setAutoExecute(self, value, refresh=True):
        self.viewSyntaxParsingAutoExecutes.setChecked(value)
        self.entry.autoExecute = value
        if refresh:
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
