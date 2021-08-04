# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'treeveiwUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout_main = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_text = QtWidgets.QLineEdit(Form)
        self.lineEdit_text.setObjectName("lineEdit_text")
        self.horizontalLayout.addWidget(self.lineEdit_text)
        self.pushButton_search = QtWidgets.QPushButton(Form)
        self.pushButton_search.setObjectName("pushButton_search")
        self.horizontalLayout.addWidget(self.pushButton_search)
        self.verticalLayout_main.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Tree"))
        self.pushButton_search.setText(_translate("Form", "Search"))
