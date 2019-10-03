#!/usr/bin/python3

from modularcalculator.modularcalculator import *
from modularcalculator.objects.exceptions import *

from PyQt5.QtWidgets import  QMessageBox


class CalculatorManager():

    def __init__(self, interface):
        self.interface = interface
        self.entry = self.interface.entry
        self.display = self.interface.display


    def restoreCalculatorState(self):
        self.importedFeatures = self.interface.fetchStateArray("importedFeatures")

        foundImportedFeatures = []
        for featureFile in self.importedFeatures:
            try:
                self.calculator.import_feature_file(featureFile)
                foundImportedFeatures.append(featureFile)
            except Exception as err:
                print("!!! Couldn't import {} - {} !!!".format(featureFile, err))
        self.importedFeatures = foundImportedFeatures

        features = self.interface.fetchStateArray("calculatorFeatures")
        if features is not None and len(features) > 0:
            self.calculator.install_features(features, False, True)
        else:
            self.calculator.load_preset('Computing')

        self.setPrecision(self.interface.fetchStateNumber("precision", 30))
        self.setUnitSimplification(self.interface.fetchStateBoolean("simplifyUnits", True))
        unitSystems = self.interface.fetchStateArray("unitSystemsPreference")
        if unitSystems is not None and len(unitSystems) > 0:
            self.calculator.unit_normaliser.systems_preference = unitSystems

        featureOptions = self.interface.fetchStateMap("calculatorFeatureOptions")
        for featureId, featuresOptions in featureOptions.items():
            for field, value in featuresOptions.items():
                if field in self.calculator.feature_list[featureId].default_options():
                    self.calculator.feature_options[featureId][field] = value
            
        self.setAutoExecute(self.interface.fetchStateBoolean("viewSyntaxParsingAutoExecutes", True), False)
        self.setShortUnits(self.interface.fetchStateBoolean("viewShortUnits", False), False)

    def storeCalculatorState(self):
        self.interface.storeStateArray("importedFeatures", list(set(self.importedFeatures)))

        self.interface.storeStateArray("calculatorFeatures", self.calculator.installed_features)
        self.interface.storeStateNumber("precision", self.interface.precisionSpinBox.spinbox.value())
        self.interface.storeStateBoolean("simplifyUnits", self.interface.optionsSimplifyUnits.isChecked())
        self.interface.storeStateArray("unitSystemsPreference", self.calculator.unit_normaliser.systems_preference)

        self.interface.storeStateMap("calculatorFeatureOptions", self.calculator.feature_options)
        
        self.interface.storeStateBoolean("viewShortUnits", self.interface.viewShortUnits.isChecked())
        self.interface.storeStateBoolean("viewSyntaxParsingAutoExecutes", self.interface.viewSyntaxParsingAutoExecutes.isChecked())


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
            QMessageBox.critical(self.interface, "ERROR", "{0} at row {1}, column {2}".format(err.message, row, column))
        except CalculatorException as err:
            QMessageBox.critical(self.interface, "ERROR", "{0}".format(err.message))

    def rowsColumns(self, text, pos):
        row = 1
        column = 0
        for i in range(0, pos):
            if text[i] == "\n":
                row += 1
                column = 0
            column += 1
        return row, column


    def setUnitSimplification(self, value):
        self.interface.optionsSimplifyUnits.setChecked(value)
        self.calculator.unit_simplification_set(value)

    def setPrecision(self, value):
        self.interface.precisionSpinBox.spinbox.setValue(value)
        self.calculator.number_prec_set(value)

    def setShortUnits(self, value, refresh=True):
        self.interface.viewShortUnits.setChecked(value)
        self.display.options['shortunits'] = value
        if refresh:
            self.display.refresh()

    def setAutoExecute(self, value, refresh=True):
        self.interface.viewSyntaxParsingAutoExecutes.setChecked(value)
        self.entry.autoExecute = value
        if refresh:
            self.entry.refresh()

    def updateUnitSystemPreference(self, systemNames):
        self.calculator.unit_normaliser.systems_preference = [s for n in systemNames for s in [s for s in self.calculator.unit_normaliser.systems if self.calculator.unit_normaliser.systems[s].name == n]]

    def commitFeatureConfig(self, calculator, importedFeatures):
        try:
            self.replaceCalculator(calculator)
            self.importedFeatures = importedFeatures
        except Exception:
            errorMessage = QMessageBox(self.interface)
            errorMessage.setText("Could not instantiate calculator with selected features")
            errorMessage.exec()
            print(traceback.format_exc())
        self.entry.refresh()
