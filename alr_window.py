from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialogButtonBox, QDialog, QLabel, QVBoxLayout, QCheckBox, QLineEdit


class Alarm_window(QDialog):
    def __init__(self):
        super(Alarm_window, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 300, 350, 250)
        self.setWindowTitle("Будильник")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        name_l = QLabel("Наименование")
        self.name_edit = QLineEdit()
        time_l = QLabel("Время")
        self.time_edit = QLineEdit()
        # active_l = QLabel("Установлено")
        self.active_check = QCheckBox("Активен")

        self.layout.addWidget(name_l)
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(time_l)
        self.layout.addWidget(self.time_edit)
        # self.layout.addWidget(active_l)
        self.layout.addWidget(self.active_check)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
