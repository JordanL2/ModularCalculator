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
            categoryFont = QFontDatabase.systemFont(QFontDatabase.TitleFont)
            categoryFont.setBold(True)
            categoryItem.setFont(categoryFont)
            categoryItem.setFlags(Qt.NoItemFlags)

            for feature in sorted(features, key=lambda f : f.title()):
                featureId = feature.id()
                featureTitle = feature.title()
                featureInstalled = featureId in parent.calculator.installed_features

                item = QListWidgetItem(featureTitle, self.featureList)
                item.setCheckState(featureInstalled * 2)
                item.setFlags(Qt.ItemIsEnabled)
                self.featureItems[featureId] = item

            spacerItem = QListWidgetItem('', self.featureList)
            spacerItem.setFlags(Qt.NoItemFlags)
        layout.addWidget(self.featureList)
        self.featureList.itemClicked.connect(self.itemClicked)
        self.featureList.itemChanged.connect(self.itemChanged)

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

    def itemClicked(self, item):
        if item.checkState() == 2:
            item.setCheckState(0)
        else:
            item.setCheckState(2)

    def itemChanged(self, item):
        print(item.text(), 'changed')
