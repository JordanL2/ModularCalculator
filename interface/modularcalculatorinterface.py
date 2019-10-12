#!/usr/bin/python3

from modularcalculator.interface.calculatormanager import *
from modularcalculator.interface.display import *
from modularcalculator.interface.featureconfig import *
from modularcalculator.interface.featureoptions import *
from modularcalculator.interface.filemanager import *
from modularcalculator.interface.guiwidgets import *
from modularcalculator.interface.statefulapplication import *
from modularcalculator.interface.tabmanager import *
from modularcalculator.interface.textedit import *

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QCursor, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QSplitter, QAction, QFileDialog, QToolTip, QShortcut, QMessageBox, QScrollArea, QSizePolicy

import os.path
import string
import sys
import traceback


class ModularCalculatorInterface(StatefulApplication):

    def __init__(self):
        super().__init__()

        self.initUI()

        self.calculatormanager = CalculatorManager(self)
        self.filemanager = FileManager(self)
        self.tabmanager = TabManager(self)
        self.filemanager.tabmanager = self.tabmanager

        self.initMenu()
        self.restoreAllState()
        self.initShortcuts()

        self.entry.setFocus()
        self.show()

    def initUI(self):
        self.tabbar = MiddleClickCloseableTabBar(self)

        self.display = CalculatorDisplay(self)
        self.displayScroll = QScrollArea()
        self.displayScroll.setBackgroundRole(QPalette.Base)
        self.displayScroll.setWidgetResizable(True)
        self.displayScroll.setWidget(self.display)
        self.displayScroll.widget().setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Maximum))

        self.entry = CalculatorTextEdit(self)

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Horizontal)

        self.splitter.addWidget(self.makeSection(self.entry, 'Input'))
        self.splitter.addWidget(self.makeSection(self.displayScroll, 'Output'))

        grid = QGridLayout()
        grid.addWidget(self.tabbar, 0, 0, 1, 1)
        grid.addWidget(self.splitter, 1, 0, 1, 1)
        
        mainWidget = QWidget()
        mainWidget.setLayout(grid)
        self.setCentralWidget(mainWidget)

    def makeSection(self, widget, labelText):
        layout = QGridLayout()
        label = QLabel(labelText)
        font = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        font.setBold(True)
        label.setFont(font)
        layout.addWidget(label, 0, 0, 1, 1)
        layout.addWidget(widget, 1, 0, 1, 1)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def initMenu(self):
        menubar = self.menuBar()
        
        self.fileMenu = menubar.addMenu('File')
        
        fileNew = QAction('New Tab', self)
        fileNew.triggered.connect(self.tabmanager.addTab)
        fileNew.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_N))
        self.fileMenu.addAction(fileNew)
        
        fileClose = QAction('Close Tab', self)
        fileClose.triggered.connect(self.tabmanager.closeCurrentTab)
        fileClose.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_W))
        self.fileMenu.addAction(fileClose)

        fileOpen = QAction('Open', self)
        fileOpen.triggered.connect(self.filemanager.open)
        fileOpen.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_O))
        self.fileMenu.addAction(fileOpen)
        
        self.fileSave = QAction('Save', self)
        self.fileSave.triggered.connect(self.filemanager.save)
        self.fileSave.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))
        self.fileMenu.addAction(self.fileSave)
        
        fileSaveAs = QAction('Save As...', self)
        fileSaveAs.triggered.connect(self.filemanager.saveAs)
        fileSaveAs.setShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_S))
        self.fileMenu.addAction(fileSaveAs)

        viewMenu = menubar.addMenu('View')

        self.viewShortUnits = QAction('Units in Short Form', self, checkable=True)
        self.viewShortUnits.triggered.connect(self.calculatormanager.setShortUnits)
        viewMenu.addAction(self.viewShortUnits)

        self.viewSyntaxParsingAutoExecutes = QAction('Syntax Parsing Performs Evaluation', self, checkable=True)
        self.viewSyntaxParsingAutoExecutes.triggered.connect(self.calculatormanager.setAutoExecute)
        viewMenu.addAction(self.viewSyntaxParsingAutoExecutes)

        self.viewClearOutput = QAction('Clear Output', self)
        self.viewClearOutput.triggered.connect(self.display.clear)
        self.viewClearOutput.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_L))
        viewMenu.addAction(self.viewClearOutput)

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
        self.precisionSpinBox.spinbox.valueChanged.connect(self.calculatormanager.setPrecision)
        optionsMenu.addAction(self.precisionSpinBox)

        self.optionsSimplifyUnits = QAction('Simplify Units', self, checkable=True)
        self.optionsSimplifyUnits.triggered.connect(self.calculatormanager.setUnitSimplification)
        optionsMenu.addAction(self.optionsSimplifyUnits)

        self.optionsUnitSystemPreference = QAction('Unit System Preference', self)
        self.optionsUnitSystemPreference.triggered.connect(self.openUnitSystemPreference)
        optionsMenu.addAction(self.optionsUnitSystemPreference)

        self.optionsFeatureConfig = QAction('Install/Remove Features', self)
        self.optionsFeatureConfig.triggered.connect(self.openFeatureConfig)
        optionsMenu.addAction(self.optionsFeatureConfig)

        self.optionsFeatureOptions = QAction('Feature Options', self)
        self.optionsFeatureOptions.triggered.connect(self.openFeatureOptions)
        optionsMenu.addAction(self.optionsFeatureOptions)

        self.executeAction = QAction('Execute', self)
        self.executeAction.triggered.connect(self.calculatormanager.calc)
        self.executeAction.hovered.connect(self.showExecuteToolTip)
        menubar.addAction(self.executeAction)
        self.executeAction.setShortcuts([QKeySequence(Qt.CTRL + Qt.Key_Enter), QKeySequence(Qt.CTRL + Qt.Key_Return)])

    def showExecuteToolTip(self):
        QToolTip.showText(QCursor.pos(), "Ctrl+Enter", self)

    def initShortcuts(self):
        previousTab = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_PageUp), self)
        previousTab.activated.connect(self.tabmanager.previousTab)
        nextTab = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_PageDown), self)
        nextTab.activated.connect(self.tabmanager.nextTab)


    def restoreAllState(self):
        try:
            self.calculatormanager.restoreCalculatorState()

            self.restoreGeometry(self.fetchState("mainWindowGeometry"))
            self.restoreState(self.fetchState("mainWindowState"))
            self.splitter.restoreState(self.fetchState("splitterSizes"))

            self.tabmanager.restoreTabs()
        except Exception as e:
            print("Exception when trying to restore state")
            print(traceback.format_exc())

    def storeAllState(self):
        self.calculatormanager.storeCalculatorState()

        self.storeState("mainWindowGeometry", self.saveGeometry())
        self.storeState("mainWindowState", self.saveState())
        self.storeState("splitterSizes", self.splitter.saveState())

        self.tabmanager.storeSelectedTab()
        self.storeStateArray("tabs", self.tabmanager.tabs)
        self.storeStateNumber("selectedTab", self.tabmanager.selectedTab)

    def insertConstant(self):
        constants = sorted(self.calculatormanager.calculator.constants.keys(), key=str)
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
        for func, funcInfo in self.calculatormanager.calculator.funcs.items():
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
        funcInfo = self.calculatormanager.calculator.funcs[func]
        self.entry.insert("{}({})".format(func, ', '.join(funcInfo.syntax)))

    def insertUserDefinedFunction(self):
        if 'structure.externalfunctions' not in self.calculatormanager.calculator.installed_features:
            QMessageBox.critical(self, "ERROR", "User Defined Functions feature not enabled.")
        else:
            filePath, _ = QFileDialog.getOpenFileName(self, "Select user-defined function file", "", "All Files (*)")
            if filePath:
                funcname = os.path.basename(filePath)
                whitelist = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_')
                funcname = ''.join(c for c in funcname if c in whitelist)
                if funcname == '':
                    funcname = 'userDefinedFunction'
                if funcname[0] in string.digits:
                    funcname = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'][int(funcname[0])] + funcname[1:]
                terminator = self.calculatormanager.calculator.feature_options['structure.terminator']['Symbol']
                quote = self.calculatormanager.calculator.feature_options['strings.strings']['Symbol']
                whitespace = ' '
                if 'nonfunctional.space' not in self.calculatormanager.calculator.installed_features:
                    whitespace = ''
                self.entry.insert("{}{}={}{}{}{}{}".format(funcname, whitespace, whitespace, quote, filePath, quote, terminator))

    def insertOperator(self):
        operators = {}
        descriptions = {}
        for op, opInfo in self.calculatormanager.calculator.ops_list.items():
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
        for dimension in self.calculatormanager.calculator.unit_normaliser.units:
            dimensionTitle = self.calculatormanager.calculator.unit_normaliser.dimensions[dimension]
            units[dimensionTitle] = []
            for unit in self.calculatormanager.calculator.unit_normaliser.units[dimension]:
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
                    unitsystem = self.calculatormanager.calculator.unit_normaliser.systems[self.calculatormanager.calculator.unit_normaliser.get_preferred_system(unit.systems)].name
                descriptions[unitName] = "{}.\nAlternative names: {}".format(unitsystem, altnames)
        CategorisedSelectionDialog(self, 'Insert Unit', 'Select unit to insert', units, descriptions, self.selectUnit)

    def selectUnit(self, unit):
        self.entry.insert(unit)

    def openUnitSystemPreference(self):
        SortableListDialog(self, 
            'Unit System Preference', 
            'Order unit systems by preference, most prefered at top', 
            [self.calculatormanager.calculator.unit_normaliser.systems[s].name for s in self.calculatormanager.calculator.unit_normaliser.systems_preference if s in self.calculatormanager.calculator.unit_normaliser.systems]
            + [self.calculatormanager.calculator.unit_normaliser.systems[s].name for s in self.calculatormanager.calculator.unit_normaliser.systems if s not in self.calculatormanager.calculator.unit_normaliser.systems_preference], 
            self.calculatormanager.updateUnitSystemPreference)

    def openFeatureConfig(self):
        FeatureConfigDialog(self)

    def openFeatureOptions(self):
        FeatureOptionsDialog(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = ModularCalculatorInterface()
    sys.exit(app.exec_())
