# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publicDialogBackground.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_maskWidgetBackground(object):
    def setupUi(self, maskWidgetBackground):
        maskWidgetBackground.setObjectName("maskWidgetBackground")
        maskWidgetBackground.resize(853, 556)
        self.horizontalLayout = QtWidgets.QHBoxLayout(maskWidgetBackground)
        self.horizontalLayout.setContentsMargins(-1, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(77, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(17, 77, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_title = QtWidgets.QLabel(maskWidgetBackground)
        self.label_title.setMinimumSize(QtCore.QSize(0, 45))
        self.label_title.setObjectName("label_title")
        self.verticalLayout.addWidget(self.label_title)
        self.widget = QtWidgets.QWidget(maskWidgetBackground)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(17, 77, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(77, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(maskWidgetBackground)
        QtCore.QMetaObject.connectSlotsByName(maskWidgetBackground)

    def retranslateUi(self, maskWidgetBackground):
        _translate = QtCore.QCoreApplication.translate
        maskWidgetBackground.setWindowTitle(_translate("maskWidgetBackground", "Form"))
        self.label_title.setText(_translate("maskWidgetBackground", "TextLabel"))
