# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'procedures_fit.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(856, 545)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 132, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_7 = QtWidgets.QPushButton(self.widget)
        self.pushButton_7.setMinimumSize(QtCore.QSize(85, 77))
        self.pushButton_7.setMaximumSize(QtCore.QSize(85, 77))
        self.pushButton_7.setStyleSheet("")
        self.pushButton_7.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_训练数据.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon)
        self.pushButton_7.setIconSize(QtCore.QSize(94, 85))
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_2.addWidget(self.pushButton_7)
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setMinimumSize(QtCore.QSize(77, 24))
        self.label_9.setMaximumSize(QtCore.QSize(77, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_8 = QtWidgets.QPushButton(self.widget)
        self.pushButton_8.setMinimumSize(QtCore.QSize(85, 77))
        self.pushButton_8.setMaximumSize(QtCore.QSize(85, 77))
        self.pushButton_8.setStyleSheet("")
        self.pushButton_8.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_验证数据.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon1)
        self.pushButton_8.setIconSize(QtCore.QSize(94, 85))
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout.addWidget(self.pushButton_8)
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setMinimumSize(QtCore.QSize(77, 24))
        self.label_10.setMaximumSize(QtCore.QSize(77, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(20, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setMinimumSize(QtCore.QSize(39, 10))
        self.pushButton_5.setMaximumSize(QtCore.QSize(39, 10))
        self.pushButton_5.setStyleSheet("background-color:transparent;\n"
"border:None;")
        self.pushButton_5.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_大向右箭头.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon2)
        self.pushButton_5.setIconSize(QtCore.QSize(39, 10))
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_4.addWidget(self.pushButton_5)
        spacerItem3 = QtWidgets.QSpacerItem(20, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setMinimumSize(QtCore.QSize(94, 77))
        self.pushButton_6.setMaximumSize(QtCore.QSize(94, 77))
        self.pushButton_6.setStyleSheet("")
        self.pushButton_6.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_代理模型.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon3)
        self.pushButton_6.setIconSize(QtCore.QSize(94, 85))
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 0, 1, 2, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(20, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.pushButton_10 = QtWidgets.QPushButton(Form)
        self.pushButton_10.setMinimumSize(QtCore.QSize(39, 10))
        self.pushButton_10.setMaximumSize(QtCore.QSize(39, 10))
        self.pushButton_10.setStyleSheet("background-color:transparent;\n"
"border:None;")
        self.pushButton_10.setText("")
        self.pushButton_10.setIcon(icon2)
        self.pushButton_10.setIconSize(QtCore.QSize(39, 10))
        self.pushButton_10.setObjectName("pushButton_10")
        self.verticalLayout_5.addWidget(self.pushButton_10)
        spacerItem5 = QtWidgets.QSpacerItem(20, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem5)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 2, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setMinimumSize(QtCore.QSize(94, 77))
        self.pushButton_9.setMaximumSize(QtCore.QSize(94, 77))
        self.pushButton_9.setStyleSheet("")
        self.pushButton_9.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_拟合模型.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon4)
        self.pushButton_9.setIconSize(QtCore.QSize(94, 85))
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 0, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setMinimumSize(QtCore.QSize(90, 24))
        self.label_6.setMaximumSize(QtCore.QSize(90, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 3, 2, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setMinimumSize(QtCore.QSize(90, 24))
        self.label_5.setMaximumSize(QtCore.QSize(90, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 1, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout)
        spacerItem6 = QtWidgets.QSpacerItem(20, 38, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem6)
        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 1, 2, 1)
        spacerItem7 = QtWidgets.QSpacerItem(219, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem7, 1, 2, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(220, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem8, 2, 0, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 131, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem9, 3, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_9.setText(_translate("Form", "训练数据"))
        self.label_10.setText(_translate("Form", "验证数据"))
        self.label_6.setText(_translate("Form", "拟合模型"))
        self.label_5.setText(_translate("Form", "代理模型"))
import icons_rc
