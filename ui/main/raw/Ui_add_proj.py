# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'g:\pycode\new_OptPlatform\ui\main\raw\add_proj.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_add_new(object):
    def setupUi(self, Dialog_add_new):
        Dialog_add_new.setObjectName("Dialog_add_new")
        Dialog_add_new.resize(484, 162)
        self.gridLayout = QtWidgets.QGridLayout(Dialog_add_new)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog_add_new)
        self.label_2.setMinimumSize(QtCore.QSize(60, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(Dialog_add_new)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Dialog_add_new)
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(Dialog_add_new)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.toolButton = QtWidgets.QToolButton(Dialog_add_new)
        self.toolButton.setMinimumSize(QtCore.QSize(30, 30))
        self.toolButton.setMaximumSize(QtCore.QSize(32, 32))
        self.toolButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/icons/打开文件.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(32, 32))
        self.toolButton.setAutoRaise(False)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_add_new)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(Dialog_add_new)
        self.buttonBox.accepted.connect(Dialog_add_new.accept)
        self.buttonBox.rejected.connect(Dialog_add_new.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_add_new)

    def retranslateUi(self, Dialog_add_new):
        _translate = QtCore.QCoreApplication.translate
        Dialog_add_new.setWindowTitle(_translate("Dialog_add_new", "新建项目"))
        self.label_2.setText(_translate("Dialog_add_new", "项目名:"))
        self.lineEdit.setText(_translate("Dialog_add_new", "项目_0"))
        self.label.setText(_translate("Dialog_add_new", "路   径:"))
import icons_rc
