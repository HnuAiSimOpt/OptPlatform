# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChooseFileType.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChooseResultFileType(object):
    def setupUi(self, ChooseResultFileType):
        ChooseResultFileType.setObjectName("ChooseResultFileType")
        ChooseResultFileType.resize(777, 140)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ChooseResultFileType)
        self.horizontalLayout.setContentsMargins(-1, 40, -1, 40)
        self.horizontalLayout.setSpacing(80)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Btn_d3plot = QtWidgets.QPushButton(ChooseResultFileType)
        self.Btn_d3plot.setMinimumSize(QtCore.QSize(120, 60))
        self.Btn_d3plot.setMaximumSize(QtCore.QSize(120, 60))
        self.Btn_d3plot.setObjectName("Btn_d3plot")
        self.horizontalLayout.addWidget(self.Btn_d3plot)
        self.Btn_rwforc = QtWidgets.QPushButton(ChooseResultFileType)
        self.Btn_rwforc.setMinimumSize(QtCore.QSize(120, 60))
        self.Btn_rwforc.setMaximumSize(QtCore.QSize(120, 60))
        self.Btn_rwforc.setObjectName("Btn_rwforc")
        self.horizontalLayout.addWidget(self.Btn_rwforc)
        self.Btn_multiFile = QtWidgets.QPushButton(ChooseResultFileType)
        self.Btn_multiFile.setMinimumSize(QtCore.QSize(120, 60))
        self.Btn_multiFile.setMaximumSize(QtCore.QSize(120, 60))
        self.Btn_multiFile.setObjectName("Btn_multiFile")
        self.horizontalLayout.addWidget(self.Btn_multiFile)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(ChooseResultFileType)
        QtCore.QMetaObject.connectSlotsByName(ChooseResultFileType)

    def retranslateUi(self, ChooseResultFileType):
        _translate = QtCore.QCoreApplication.translate
        ChooseResultFileType.setWindowTitle(_translate("ChooseResultFileType", "选取结果文件类型"))
        self.Btn_d3plot.setText(_translate("ChooseResultFileType", "D3plot"))
        self.Btn_rwforc.setText(_translate("ChooseResultFileType", "rwforc"))
        self.Btn_multiFile.setText(_translate("ChooseResultFileType", "MultiFile"))