#!/usr/bin/python3

from modularcalculator.modularcalculator import *

#from PyQt5.QtCore import Qt, QStringListModel, QSize
#from PyQt5.QtWidgets import QListWidget, QWidgetAction, QSpinBox, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QListView, QDialog, QAbstractItemView, QPushButton, QCalendarWidget, QTimeEdit, QComboBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFontDatabase


class FeatureConfigDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.importedFeatures = parent.importedFeatures
        self.calculator = self.buildCalculator(self.importedFeatures, [])
        self.selectedFeatures = parent.calculator.installed_features

        layout = QVBoxLayout()

        self.featureList = QListWidget(self)
        self.refreshFeatureList()
        layout.addWidget(self.featureList)
        self.featureList.itemClicked.connect(self.itemClicked)
        self.featureList.itemChanged.connect(self.itemChanged)

        button = QPushButton("OK", self)
        button.clicked.connect(self.ok)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowTitle('Feature Configuration')
        self.setVisible(True)

    def refreshFeatureList(self):
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
                featureTitle = feature.title()
                featureInstalled = featureId in self.selectedFeatures and not issubclass(feature, MetaFeature)

                item = QListWidgetItem(featureTitle, self.featureList)
                item.setCheckState(featureInstalled * 2)
                item.setFlags(Qt.ItemIsEnabled)
                item.setData(Qt.UserRole, featureId)
                self.featureItems[featureId] = item

            spacerItem = QListWidgetItem('', self.featureList)
            spacerItem.setFlags(Qt.NoItemFlags)

    def buildCalculator(self, importedFeatures, features):
        calculator = ModularCalculator()
        for importedFeature in importedFeatures:
            calculator.import_feature_file(importedFeature)
        calculator.install_features(features, True)
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
        return QSize(super().sizeHint() * 4)

    def itemClicked(self, item):
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    def getItemsFeature(self, item):
        return self.calculator.feature_list[item.data(Qt.UserRole)]

    def itemChanged(self, item):
        feature = self.getItemsFeature(item)
        featureId = feature.id()
        print(feature.title(), 'changed')
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
                
