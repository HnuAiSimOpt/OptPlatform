# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OptimizationResults.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets


class Ui_OptimizationResults(object):
    def setupUi(self, OptimizationResults):
        OptimizationResults.setObjectName("OptimizationResults")
        OptimizationResults.resize(1099, 700)
        self.verticalLayout = QtWidgets.QVBoxLayout(OptimizationResults)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = myTableWidget(OptimizationResults)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.widget = myLineChart(OptimizationResults)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 5)

        self.retranslateUi(OptimizationResults)
        QtCore.QMetaObject.connectSlotsByName(OptimizationResults)

    def retranslateUi(self, OptimizationResults):
        _translate = QtCore.QCoreApplication.translate
        OptimizationResults.setWindowTitle(_translate("OptimizationResults", "Form"))
from PublicTool.myLineChart import myLineChart
from ui.paraSetting.myTableWidget import myTableWidget