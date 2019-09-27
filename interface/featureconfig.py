#!/usr/bin/python3

from modularcalculator.modularcalculator import *

#from PyQt5.QtCore import Qt, QStringListModel, QSize
#from PyQt5.QtWidgets import QListWidget, QWidgetAction, QSpinBox, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QListView, QDialog, QAbstractItemView, QPushButton, QCalendarWidget, QTimeEdit, QComboBox
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem


class FeatureConfigDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.importedFeatures = parent.importedFeatures

        layout = QVBoxLayout()

        featuresByCategory = {}
        for featureId, feature in parent.calculator.feature_list.items():
            featureCategory = feature.category()
            if featureCategory not in featuresByCategory:
                featuresByCategory[featureCategory] = []
            featuresByCategory[featureCategory].append(feature)

        self.featureItems = {}
        self.featureList = QListWidget(self)
        for featureCategory, features in featuresByCategory.items():
            categoryItem = QListWidgetItem(featureCategory, self.featureList)
            for feature in sorted(features, key=lambda f : f.title()):
                featureId = feature.id()
                featureTitle = feature.title()
                featureInstalled = featureId in parent.calculator.installed_features

                item = QListWidgetItem(featureTitle, self.featureList)
                item.setCheckState(featureInstalled * 2)
                self.featureItems[featureId] = item
        layout.addWidget(self.featureList)

        button = QPushButton("OK", self)
        button.clicked.connect(self.ok)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowTitle('Feature Configuration')
        self.setVisible(True)

    def ok(self):
        calculator = ModularCalculator()
        featuresToInstall = []
        for featureId, item in self.featureItems.items():
            if item.checkState() == 2:
                featuresToInstall.append(featureId)
        calculator.install_features(featuresToInstall, True)
        self.parent.commitFeatureConfig(calculator, self.importedFeatures)
        self.close()

    def sizeHint(self):
        return QSize(super().sizeHint() * 4)
