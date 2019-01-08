#!/usr/bin/python3

from PyQt5.QtWidgets import QInputDialog, QWidgetAction, QSpinBox, QLabel, QHBoxLayout, QWidget


class SelectionDialog(QInputDialog):

    def __init__(self, parent, title, label, items, okFunction):
        super().__init__(parent)
        self.setInputMode(QInputDialog.TextInput)
        self.setComboBoxItems(items)
        self.setOption(QInputDialog.UseListViewForComboBoxItems, True)
        self.setWindowTitle(title)
        self.setLabelText(label)
        self.textValueSelected.connect(okFunction)
        self.setVisible(True)


class MenuSpinBox(QWidgetAction):

    def __init__(self, parent, label, minimum, maximum):
        super().__init__(parent)
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(minimum)
        self.spinbox.setMaximum(maximum)
        labelWidget = QLabel(label)
        layout = QHBoxLayout()
        layout.addWidget(labelWidget)
        layout.addWidget(self.spinbox)
        widget = QWidget()
        widget.setLayout(layout)
        self.setDefaultWidget(widget)
