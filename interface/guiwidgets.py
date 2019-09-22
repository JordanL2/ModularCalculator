#!/usr/bin/python3

from PyQt5.QtCore import Qt, QStringListModel, QSize
from PyQt5.QtWidgets import QInputDialog, QWidgetAction, QSpinBox, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QListView, QDialog, QAbstractItemView, QPushButton, QCalendarWidget


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

    def sizeHint(self):
        return QSize(super().sizeHint() * 2)


class SortableListModel(QStringListModel):

    def flags(self, index):
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        return super().flags(index)


class SortableListView(QListView):

    def sizeHint(self):
        return QSize(self.width(), self.sizeHintForRow(0) * self.model().rowCount() + 10)


class SortableListDialog(QDialog):

    def __init__(self, parent, title, label, items, okFunction):
        super().__init__(parent)

        self.okFunction = okFunction

        layout = QVBoxLayout()

        labelWidget = QLabel(label)
        layout.addWidget(labelWidget)

        self.stringModel = SortableListModel()
        self.stringModel.setStringList(items)

        listView = SortableListView(self)
        listView.setModel(self.stringModel)
        listView.setDragDropMode(QAbstractItemView.InternalMove)
        layout.addWidget(listView)

        button = QPushButton("OK", self)
        button.clicked.connect(self.ok)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowTitle(title)
        self.setVisible(True)

    def ok(self):
        self.okFunction(self.stringModel.stringList())
        self.close()


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


class DatePicker(QDialog):

    def __init__(self, parent, title, okFunction):
        super().__init__(parent)

        self.okFunction = okFunction

        layout = QVBoxLayout()

        self.datePicker = QCalendarWidget(self)
        layout.addWidget(self.datePicker)

        button = QPushButton("OK", self)
        button.clicked.connect(self.ok)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowTitle(title)
        self.setVisible(True)

    def ok(self):
        self.okFunction(self.datePicker.selectedDate())
        self.close()
