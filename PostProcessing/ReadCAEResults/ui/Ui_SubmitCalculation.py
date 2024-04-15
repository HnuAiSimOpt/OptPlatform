# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SubmitCalculation.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SubmitCalculation(object):
    def setupUi(self, SubmitCalculation):
        SubmitCalculation.setObjectName("SubmitCalculation")
        SubmitCalculation.resize(922, 640)
        self.verticalLayout = QtWidgets.QVBoxLayout(SubmitCalculation)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.label_filePath = QtWidgets.QLabel(SubmitCalculation)
        self.label_filePath.setMinimumSize(QtCore.QSize(0, 30))
        self.label_filePath.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_filePath.setObjectName("label_filePath")
        self.gridLayout.addWidget(self.label_filePath, 0, 0, 1, 1)
        self.lineEdit_filePath = QtWidgets.QLineEdit(SubmitCalculation)
        self.lineEdit_filePath.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_filePath.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_filePath.setObjectName("lineEdit_filePath")
        self.gridLayout.addWidget(self.lineEdit_filePath, 0, 1, 1, 1)
        self.label_solverPath = QtWidgets.QLabel(SubmitCalculation)
        self.label_solverPath.setMinimumSize(QtCore.QSize(0, 30))
        self.label_solverPath.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_solverPath.setObjectName("label_solverPath")
        self.gridLayout.addWidget(self.label_solverPath, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.cbB_solverPath = QtWidgets.QComboBox(SubmitCalculation)
        self.cbB_solverPath.setMinimumSize(QtCore.QSize(0, 30))
        self.cbB_solverPath.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbB_solverPath.setObjectName("cbB_solverPath")
        self.horizontalLayout_5.addWidget(self.cbB_solverPath)
        self.Btn_findSolver = QtWidgets.QPushButton(SubmitCalculation)
        self.Btn_findSolver.setMinimumSize(QtCore.QSize(32, 30))
        self.Btn_findSolver.setMaximumSize(QtCore.QSize(32, 30))
        self.Btn_findSolver.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/icons/打开文件icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Btn_findSolver.setIcon(icon)
        self.Btn_findSolver.setIconSize(QtCore.QSize(16, 16))
        self.Btn_findSolver.setObjectName("Btn_findSolver")
        self.horizontalLayout_5.addWidget(self.Btn_findSolver)
        self.horizontalLayout_5.setStretch(0, 1)
        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)
        self.label_batPath = QtWidgets.QLabel(SubmitCalculation)
        self.label_batPath.setMinimumSize(QtCore.QSize(0, 30))
        self.label_batPath.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_batPath.setObjectName("label_batPath")
        self.gridLayout.addWidget(self.label_batPath, 2, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.cbB_batPath = QtWidgets.QComboBox(SubmitCalculation)
        self.cbB_batPath.setMinimumSize(QtCore.QSize(0, 30))
        self.cbB_batPath.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbB_batPath.setObjectName("cbB_batPath")
        self.horizontalLayout_7.addWidget(self.cbB_batPath)
        self.Btn_findBat = QtWidgets.QPushButton(SubmitCalculation)
        self.Btn_findBat.setMinimumSize(QtCore.QSize(32, 30))
        self.Btn_findBat.setMaximumSize(QtCore.QSize(32, 30))
        self.Btn_findBat.setText("")
        self.Btn_findBat.setIcon(icon)
        self.Btn_findBat.setIconSize(QtCore.QSize(16, 16))
        self.Btn_findBat.setObjectName("Btn_findBat")
        self.horizontalLayout_7.addWidget(self.Btn_findBat)
        self.horizontalLayout_7.setStretch(0, 1)
        self.gridLayout.addLayout(self.horizontalLayout_7, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_NCPU = QtWidgets.QLabel(SubmitCalculation)
        self.label_NCPU.setMinimumSize(QtCore.QSize(0, 30))
        self.label_NCPU.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_NCPU.setObjectName("label_NCPU")
        self.horizontalLayout_2.addWidget(self.label_NCPU)
        self.CBb_NCPU = QtWidgets.QComboBox(SubmitCalculation)
        self.CBb_NCPU.setMinimumSize(QtCore.QSize(100, 30))
        self.CBb_NCPU.setMaximumSize(QtCore.QSize(16777215, 30))
        self.CBb_NCPU.setObjectName("CBb_NCPU")
        self.horizontalLayout_2.addWidget(self.CBb_NCPU)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_MEMORY = QtWidgets.QLabel(SubmitCalculation)
        self.label_MEMORY.setMinimumSize(QtCore.QSize(0, 30))
        self.label_MEMORY.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_MEMORY.setObjectName("label_MEMORY")
        self.horizontalLayout.addWidget(self.label_MEMORY)
        self.CBb_MEMORY = QtWidgets.QComboBox(SubmitCalculation)
        self.CBb_MEMORY.setMinimumSize(QtCore.QSize(100, 30))
        self.CBb_MEMORY.setMaximumSize(QtCore.QSize(16777215, 30))
        self.CBb_MEMORY.setObjectName("CBb_MEMORY")
        self.horizontalLayout.addWidget(self.CBb_MEMORY)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_3.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.rBtn_inputCmd = QtWidgets.QRadioButton(SubmitCalculation)
        self.rBtn_inputCmd.setObjectName("rBtn_inputCmd")
        self.horizontalLayout_6.addWidget(self.rBtn_inputCmd)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.textEdit_cmd = QtWidgets.QTextEdit(SubmitCalculation)
        self.textEdit_cmd.setObjectName("textEdit_cmd")
        self.verticalLayout.addWidget(self.textEdit_cmd)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(8)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.Btn_submit = QtWidgets.QPushButton(SubmitCalculation)
        self.Btn_submit.setMinimumSize(QtCore.QSize(96, 40))
        self.Btn_submit.setMaximumSize(QtCore.QSize(96, 16777215))
        self.Btn_submit.setObjectName("Btn_submit")
        self.horizontalLayout_4.addWidget(self.Btn_submit)
        self.Btn_cancel = QtWidgets.QPushButton(SubmitCalculation)
        self.Btn_cancel.setMinimumSize(QtCore.QSize(96, 40))
        self.Btn_cancel.setMaximumSize(QtCore.QSize(96, 16777215))
        self.Btn_cancel.setObjectName("Btn_cancel")
        self.horizontalLayout_4.addWidget(self.Btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout.setStretch(3, 1)

        self.retranslateUi(SubmitCalculation)
        QtCore.QMetaObject.connectSlotsByName(SubmitCalculation)

    def retranslateUi(self, SubmitCalculation):
        _translate = QtCore.QCoreApplication.translate
        SubmitCalculation.setWindowTitle(_translate("SubmitCalculation", "Form"))
        self.label_filePath.setText(_translate("SubmitCalculation", "文件路径"))
        self.label_solverPath.setText(_translate("SubmitCalculation", "求解器路径"))
        self.label_batPath.setText(_translate("SubmitCalculation", "批处理文件路径"))
        self.label_NCPU.setText(_translate("SubmitCalculation", "NCPU"))
        self.label_MEMORY.setText(_translate("SubmitCalculation", "MEMORY"))
        self.rBtn_inputCmd.setText(_translate("SubmitCalculation", "在下框中输入调用指令"))
        self.Btn_submit.setText(_translate("SubmitCalculation", "提交计算"))
        self.Btn_cancel.setText(_translate("SubmitCalculation", "取消"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SubmitCalculation = QtWidgets.QWidget()
    ui = Ui_SubmitCalculation()
    ui.setupUi(SubmitCalculation)
    SubmitCalculation.show()
    sys.exit(app.exec_())
