#!/usr/bin/python3

from modularcalculator.modularcalculator import *

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QGridLayout, QLabel, QPushButton, QLineEdit


class FeatureOptionsDialog(QDialog):
    
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        layout = QVBoxLayout()

        self.featureList = QListWidget(self)
        features = [f for f in self.parent.calculator.feature_list.values() if f.id() in self.parent.calculator.feature_options and f.id() in self.parent.calculator.installed_features]
        for feature in sorted(features, key=lambda f : f.title()):
            item = QListWidgetItem(feature.title(), self.featureList)
            item.setFlags(Qt.ItemIsEnabled)
            item.setData(Qt.UserRole, feature.id())
        self.featureList.itemClicked.connect(self.openFeature)
        layout.addWidget(self.featureList)

        self.setLayout(layout)
        self.setWindowTitle('Feature Options')
        self.setVisible(True)

    def sizeHint(self):
        return QSize(super().sizeHint() * 2)

    def openFeature(self, item):
        featureId = item.data(Qt.UserRole)
        ConfigureFeatureDialog(self, featureId)


class ConfigureFeatureDialog(QDialog):

    def __init__(self, parent, featureId):
        super().__init__(parent)

        self.parent = parent
        self.calculator = self.parent.parent.calculator
        self.feature = self.calculator.feature_list[featureId]
        self.featureOptions = self.calculator.feature_options[featureId]

        grid = QGridLayout()

        maxI = 0
        self.fieldEditBoxes = {}
        for i, fieldAndValue in enumerate(self.featureOptions.items()):
            fieldName = fieldAndValue[0]
            fieldValue = fieldAndValue[1]
            lineEdit = QLineEdit(fieldValue, self)
            self.fieldEditBoxes[fieldName] = lineEdit
            grid.addWidget(QLabel(fieldName), i, 0, 1, 1)
            grid.addWidget(lineEdit, i, 1, 1, 1)
            maxI = i

        button = QPushButton("OK", self)
        button.clicked.connect(self.ok)
        grid.addWidget(button, maxI + 1, 0, 1, 2)

        self.setLayout(grid)
        self.setWindowTitle("{} Options".format(self.feature.title()))
        self.setVisible(True)

    def ok(self):
        for field, lineEdit in self.fieldEditBoxes.items():
            value = lineEdit.text()
            self.featureOptions[field] = value
        self.parent.parent.entry.refresh()
        self.close()
