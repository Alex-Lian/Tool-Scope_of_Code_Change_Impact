# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QTreeView

from jsonTreeView import JsonModel, final_mapping, mapping_test_old, mapping_test_new, mapping_test_select
from treeveiwUI import Ui_Form


class TreeView(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.setupUi(self) 

        self.view = QTreeView()
        model = JsonModel()
        self.view.setModel(model)
        self.verticalLayout_main.addWidget(self.view)
        self.view.setColumnHidden(1, True)

        model.load(mapping_test_select, )
        self.resize(800, 600)

    @pyqtSlot()
    def on_pushButton_search_clicked(self):
        model = self.view.model()
        model.set_selected(self.lineEdit_text.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    windo = TreeView()
    windo.show()
    sys.exit(app.exec_())
