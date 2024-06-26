# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'procedures_opt_CAE.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(911, 530)
        Form.setAutoFillBackground(False)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setContentsMargins(-1, -1, 9, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 133, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(154, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_10 = QtWidgets.QPushButton(Form)
        self.pushButton_10.setMinimumSize(QtCore.QSize(94, 77))
        self.pushButton_10.setMaximumSize(QtCore.QSize(94, 77))
        self.pushButton_10.setStyleSheet("")
        self.pushButton_10.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_优化算法.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_10.setIcon(icon)
        self.pushButton_10.setIconSize(QtCore.QSize(94, 85))
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 6, 6, 1, 1)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setMinimumSize(QtCore.QSize(22, 10))
        self.pushButton_7.setMaximumSize(QtCore.QSize(22, 10))
        self.pushButton_7.setStyleSheet("background-color:transparent;\n"
"border:None;")
        self.pushButton_7.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_向右箭头.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon1)
        self.pushButton_7.setIconSize(QtCore.QSize(22, 10))
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_7.addWidget(self.pushButton_7)
        self.gridLayout.addLayout(self.verticalLayout_7, 1, 5, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setMinimumSize(QtCore.QSize(94, 77))
        self.pushButton_2.setMaximumSize(QtCore.QSize(94, 77))
        self.pushButton_2.setStyleSheet("")
        self.pushButton_2.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_DOE.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setIconSize(QtCore.QSize(94, 85))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 2, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setMinimumSize(QtCore.QSize(22, 10))
        self.pushButton_5.setMaximumSize(QtCore.QSize(22, 10))
        self.pushButton_5.setStyleSheet("background-color:transparent;\n"
"border:None;")
        self.pushButton_5.setText("")
        self.pushButton_5.setIcon(icon1)
        self.pushButton_5.setIconSize(QtCore.QSize(22, 10))
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_5.addWidget(self.pushButton_5)
        self.gridLayout.addLayout(self.verticalLayout_5, 1, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setMinimumSize(QtCore.QSize(90, 24))
        self.label_6.setMaximumSize(QtCore.QSize(90, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 10, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(90, 24))
        self.label_3.setMaximumSize(QtCore.QSize(90, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 2, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(Form)
        self.pushButton_11.setMinimumSize(QtCore.QSize(94, 77))
        self.pushButton_11.setMaximumSize(QtCore.QSize(94, 77))
        self.pushButton_11.setStyleSheet("")
        self.pushButton_11.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_最优解.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_11.setIcon(icon3)
        self.pushButton_11.setIconSize(QtCore.QSize(94, 85))
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout.addWidget(self.pushButton_11, 6, 10, 1, 1)
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
        self.gridLayout.addWidget(self.pushButton_9, 1, 10, 2, 1)
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setMinimumSize(QtCore.QSize(94, 77))
        self.pushButton_6.setMaximumSize(QtCore.QSize(94, 77))
        self.pushButton_6.setStyleSheet("")
        self.pushButton_6.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_代理模型.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon5)
        self.pushButton_6.setIconSize(QtCore.QSize(94, 85))
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 1, 6, 1, 1)
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setMinimumSize(QtCore.QSize(90, 24))
        self.label_8.setMaximumSize(QtCore.QSize(90, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 7, 10, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setMinimumSize(QtCore.QSize(90, 24))
        self.label_4.setMaximumSize(QtCore.QSize(90, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 4, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setMinimumSize(QtCore.QSize(94, 77))
        self.pushButton.setMaximumSize(QtCore.QSize(94, 77))
        self.pushButton.setAutoFillBackground(True)
        self.pushButton.setStyleSheet("")
        self.pushButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_CAE求解文件.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon6)
        self.pushButton.setIconSize(QtCore.QSize(94, 85))
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 2, 1)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.pushButton_12 = QtWidgets.QPushButton(Form)
        self.pushButton_12.setMinimumSize(QtCore.QSize(22, 10))
        self.pushButton_12.setMaximumSize(QtCore.QSize(22, 10))
        self.pushButton_12.setStyleSheet("background-color:transparent;\n"
"border:None;")
        self.pushButton_12.setText("")
        self.pushButton_12.setIcon(icon1)
        self.pushButton_12.setIconSize(QtCore.QSize(22, 10))
        self.pushButton_12.setObjectName("pushButton_12")
        self.verticalLayout_12.addWidget(self.pushButton_12)
        self.gridLayout.addLayout(self.verticalLayout_12, 6, 9, 1, 1)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setMinimumSize(QtCore.QSize(22, 10))
        self.pushButton_8.setMaximumSize(QtCore.QSize(22, 10))
        self.pushButton_8.setStyleSheet("background-color:transparent;\n"
"border:None;")
        self.pushButton_8.setText("")
        self.pushButton_8.setIcon(icon1)
        self.pushButton_8.setIconSize(QtCore.QSize(22, 10))
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout_8.addWidget(self.pushButton_8)
        self.gridLayout.addLayout(self.verticalLayout_8, 0, 9, 3, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(90, 24))
        self.label.setMaximumSize(QtCore.QSize(90, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setMinimumSize(QtCore.QSize(22, 10))
        self.pushButton_3.setMaximumSize(QtCore.QSize(22, 10))
        self.pushButton_3.setStyleSheet("background-color:transparent;\n"
"border:None;")
        self.pushButton_3.setText("")
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(22, 10))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_3.addWidget(self.pushButton_3)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 3, 1)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setMinimumSize(QtCore.QSize(90, 24))
        self.label_7.setMaximumSize(QtCore.QSize(90, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 7, 6, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setMinimumSize(QtCore.QSize(94, 77))
        self.pushButton_4.setMaximumSize(QtCore.QSize(94, 77))
        self.pushButton_4.setStyleSheet("")
        self.pushButton_4.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_仿真.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon7)
        self.pushButton_4.setIconSize(QtCore.QSize(94, 85))
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setMinimumSize(QtCore.QSize(90, 24))
        self.label_5.setMaximumSize(QtCore.QSize(90, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 6, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_13 = QtWidgets.QPushButton(Form)
        self.pushButton_13.setMinimumSize(QtCore.QSize(10, 22))
        self.pushButton_13.setMaximumSize(QtCore.QSize(10, 222))
        self.pushButton_13.setStyleSheet("background-color:transparent;\n"
"border:None;")
        self.pushButton_13.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/pic/icons/示意图_向下箭头.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_13.setIcon(icon8)
        self.pushButton_13.setIconSize(QtCore.QSize(10, 22))
        self.pushButton_13.setObjectName("pushButton_13")
        self.horizontalLayout.addWidget(self.pushButton_13)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 6, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(153, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 133, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_6.setText(_translate("Form", "拟合模型"))
        self.label_3.setText(_translate("Form", "DOE"))
        self.label_8.setText(_translate("Form", "最优解"))
        self.label_4.setText(_translate("Form", "仿真"))
        self.label.setText(_translate("Form", "CAE求解文件"))
        self.label_7.setText(_translate("Form", "优化算法"))
        self.label_5.setText(_translate("Form", "代理模型"))
import icons_rc
