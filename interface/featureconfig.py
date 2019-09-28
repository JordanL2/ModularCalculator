#!/usr/bin/python3

from modularcalculator.modularcalculator import *

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QDialog, QWidget, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QComboBox, QFileDialog, QSplitter, QGridLayout, QLabel


class FeatureConfigDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.importedFeatures = parent.importedFeatures
        self.calculator = self.buildCalculator(self.importedFeatures, [])
        self.selectedFeatures = parent.calculator.installed_features

        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)

        self.presetList = QComboBox(self)
        self.presetList.addItem('- Presets -')
        self.presetList.addItem('Select All')
        self.presetList.addItem('Select None')
        self.presetList.addItems(self.calculator.preset_list.keys())
        self.presetList.currentTextChanged.connect(self.selectPreset)
        splitter.addWidget(self.presetList)
        splitter.setStretchFactor(0, 0)

        self.featureList = QListWidget(self)
        self.refreshFeatureList()
        self.featureList.setMinimumWidth(self.featureList.sizeHintForColumn(0))
        self.featureList.itemClicked.connect(self.itemClicked)
        self.featureList.itemChanged.connect(self.itemChanged)
        splitter.addWidget(self.featureList)
        splitter.setStretchFactor(1, 1)

        importedFileLabel = QLabel("External Feature Files")
        importedFileLabelFont = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        importedFileLabelFont.setBold(True)
        importedFileLabel.setFont(importedFileLabelFont)
        importedFileLabel.setAlignment(Qt.AlignHCenter)
        splitter.addWidget(importedFileLabel)
        splitter.setStretchFactor(2, 0)

        importedFileButtonsLayout = QHBoxLayout()
        addFileButton = QPushButton("Add", self)
        addFileButton.clicked.connect(self.addFile)
        importedFileButtonsLayout.addWidget(addFileButton)
        removeFileButton = QPushButton("Remove", self)
        removeFileButton.clicked.connect(self.removeFile)
        importedFileButtonsLayout.addWidget(removeFileButton)
        importedFiles = QWidget()
        importedFiles.setLayout(importedFileButtonsLayout)
        splitter.addWidget(importedFiles)
        splitter.setStretchFactor(3, 0)

        self.importedFileList = QListWidget(self)
        self.refreshImportedFiles()
        splitter.addWidget(self.importedFileList)
        splitter.setStretchFactor(4, 0)

        okButton = QPushButton("OK", self)
        okButton.clicked.connect(self.ok)
        splitter.addWidget(okButton)
        splitter.setStretchFactor(5, 0)

        for i in range(0, splitter.count()):
            splitter.handle(i).setEnabled(False)
        grid = QGridLayout()
        grid.addWidget(splitter, 0, 0, 6, 1)
        self.setLayout(grid)

        self.setWindowTitle('Feature Configuration')
        self.setVisible(True)

    def refreshFeatureList(self):
        self.featureList.blockSignals(True)

        featuresByCategory = {}
        for featureId, feature in self.calculator.feature_list.items():
            featureCategory = feature.category()
            if featureCategory not in featuresByCategory:
                featuresByCategory[featureCategory] = []
            featuresByCategory[featureCategory].append(feature)
        
        self.featureItems = {}
        self.featureList.clear()
        for featureCategory, features in featuresByCategory.items():
            categoryItem = QListWidgetItem(featureCategory, self.featureList)
            categoryFont = QFontDatabase.systemFont(QFontDatabase.TitleFont)
            categoryFont.setBold(True)
            categoryItem.setFont(categoryFont)
            categoryItem.setFlags(Qt.NoItemFlags)

            for feature in sorted(features, key=lambda f : f.title()):
                featureId = feature.id()
                if feature.desc() != '':
                    featureText = "{} - {}".format(feature.title(), feature.desc())
                else:
                    featureText = feature.title()
                featureInstalled = featureId in self.selectedFeatures and not issubclass(feature, MetaFeature)

                item = QListWidgetItem(featureText, self.featureList)
                item.setCheckState(featureInstalled * 2)
                item.setFlags(Qt.ItemIsEnabled)
                item.setData(Qt.UserRole, featureId)
                self.featureItems[featureId] = item

            spacerItem = QListWidgetItem('', self.featureList)
            spacerItem.setFlags(Qt.NoItemFlags)

        self.featureList.blockSignals(False)

    def refreshImportedFiles(self):
        self.importedFileList.clear()
        self.importedFileList.addItems(self.importedFeatures)

    def buildCalculator(self, importedFeatures, features):
        calculator = ModularCalculator()
        calculator.enable_units()
        for importedFeature in importedFeatures:
            calculator.import_feature_file(importedFeature)
        calculator.install_features(features, False)
        return calculator

    def ok(self):
        featuresToInstall = []
        for featureId, item in self.featureItems.items():
            if item.checkState() == Qt.Checked:
                featuresToInstall.append(featureId)
        calculator = self.buildCalculator(self.importedFeatures, featuresToInstall)
        self.parent.commitFeatureConfig(calculator, self.importedFeatures)
        self.close()

    def sizeHint(self):
        size = super().sizeHint()
        size.setHeight(size.height() * 2)
        return size

    def itemClicked(self, item):
        if item.data(Qt.UserRole) is None:
            return
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    def getItemsFeature(self, item):
        featureId = item.data(Qt.UserRole)
        if featureId is not None:
            return self.calculator.feature_list[featureId]
        return None

    def itemChanged(self, item):
        feature = self.getItemsFeature(item)
        featureId = feature.id()
        if item.checkState() == Qt.Checked:
            if issubclass(feature, MetaFeature):
                for subfeatureId in feature.subfeatures():
                    subFeatureItem = self.featureItems[subfeatureId]
                    if subFeatureItem.checkState() == Qt.Unchecked:
                        subFeatureItem.setCheckState(Qt.Checked)
                item.setCheckState(Qt.Unchecked)
            else:
                for dependencyFeatureId in feature.dependencies():
                    dependencyFeatureItem = self.featureItems[dependencyFeatureId]
                    if dependencyFeatureItem.checkState() == Qt.Unchecked:
                        dependencyFeatureItem.setCheckState(Qt.Checked)
        else:
            for checkFeatureId, checkFeature in self.calculator.feature_list.items():
                if featureId in checkFeature.dependencies():
                    checkFeatureItem = self.featureItems[checkFeatureId]
                    if checkFeatureItem.checkState() == Qt.Checked:
                        checkFeatureItem.setCheckState(0)
                
    def selectPreset(self, text):
        if text == 'Select All':
            for item in self.featureItems.values():
                if item.checkState() == Qt.Unchecked:
                    item.setCheckState(Qt.Checked)
        elif text == 'Select None':
            for item in self.featureItems.values():
                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
        elif text in self.calculator.preset_list:
            for item in self.featureItems.values():
                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
            for featureId in self.calculator.preset_list[text]:
                item = self.featureItems[featureId]
                if item.checkState() == Qt.Unchecked:
                    item.setCheckState(Qt.Checked)
        self.presetList.setCurrentIndex(0)

    def addFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Feature File", "", "All Files (*)")
        if filePath:
            self.importedFeatures.append(filePath)
            self.refreshImportedFiles()
            self.refreshAvailableFeatures()

    def removeFile(self):
        for selectedItem in self.importedFileList.selectedItems():
            self.importedFeatures.remove(selectedItem.text())
        self.refreshImportedFiles()
        self.refreshAvailableFeatures()

    def refreshAvailableFeatures(self):
        self.selectedFeatures = []
        for featureId, item in self.featureItems.items():
            if item.checkState() == Qt.Checked:
                self.selectedFeatures.append(featureId)
        self.calculator = self.buildCalculator(self.importedFeatures, [])
        self.refreshFeatureList()
