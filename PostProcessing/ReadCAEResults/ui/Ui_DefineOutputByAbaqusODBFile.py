# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'defineOutputByAbaqusODBFile.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(963, 547)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_name = QtWidgets.QLabel(Form)
        self.label_name.setMinimumSize(QtCore.QSize(0, 30))
        self.label_name.setObjectName("label_name")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_name)
        self.lineEdit_name = QtWidgets.QLineEdit(Form)
        self.lineEdit_name.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_name)
        self.label_step = QtWidgets.QLabel(Form)
        self.label_step.setMinimumSize(QtCore.QSize(0, 30))
        self.label_step.setObjectName("label_step")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_step)
        self.cbb_step = QtWidgets.QComboBox(Form)
        self.cbb_step.setMinimumSize(QtCore.QSize(0, 30))
        self.cbb_step.setObjectName("cbb_step")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cbb_step)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.rB_FieldOutput = QtWidgets.QRadioButton(Form)
        self.rB_FieldOutput.setMinimumSize(QtCore.QSize(0, 30))
        self.rB_FieldOutput.setMaximumSize(QtCore.QSize(16777215, 30))
        self.rB_FieldOutput.setObjectName("rB_FieldOutput")
        self.horizontalLayout_7.addWidget(self.rB_FieldOutput)
        self.rB_HistoryOutput = QtWidgets.QRadioButton(Form)
        self.rB_HistoryOutput.setMinimumSize(QtCore.QSize(0, 30))
        self.rB_HistoryOutput.setMaximumSize(QtCore.QSize(16777215, 30))
        self.rB_HistoryOutput.setObjectName("rB_HistoryOutput")
        self.horizontalLayout_7.addWidget(self.rB_HistoryOutput)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.stackedWidget = QtWidgets.QStackedWidget(Form)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_FieldOutput = QtWidgets.QWidget()
        self.page_FieldOutput.setObjectName("page_FieldOutput")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page_FieldOutput)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_frame = QtWidgets.QLabel(self.page_FieldOutput)
        self.label_frame.setMinimumSize(QtCore.QSize(0, 30))
        self.label_frame.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_frame.setObjectName("label_frame")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_frame)
        self.cbb_frame = QtWidgets.QComboBox(self.page_FieldOutput)
        self.cbb_frame.setMinimumSize(QtCore.QSize(0, 30))
        self.cbb_frame.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbb_frame.setObjectName("cbb_frame")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbb_frame)
        self.label_instanceORnodeset = QtWidgets.QLabel(self.page_FieldOutput)
        self.label_instanceORnodeset.setMinimumSize(QtCore.QSize(0, 30))
        self.label_instanceORnodeset.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_instanceORnodeset.setObjectName("label_instanceORnodeset")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_instanceORnodeset)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cbb_insORset = QtWidgets.QComboBox(self.page_FieldOutput)
        self.cbb_insORset.setMinimumSize(QtCore.QSize(0, 30))
        self.cbb_insORset.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbb_insORset.setObjectName("cbb_insORset")
        self.horizontalLayout_3.addWidget(self.cbb_insORset)
        self.cbb_insORsetName = QtWidgets.QComboBox(self.page_FieldOutput)
        self.cbb_insORsetName.setMinimumSize(QtCore.QSize(0, 30))
        self.cbb_insORsetName.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbb_insORsetName.setObjectName("cbb_insORsetName")
        self.horizontalLayout_3.addWidget(self.cbb_insORsetName)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_component = QtWidgets.QLabel(self.page_FieldOutput)
        self.label_component.setMinimumSize(QtCore.QSize(0, 30))
        self.label_component.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_component.setObjectName("label_component")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_component)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cbb_component = QtWidgets.QComboBox(self.page_FieldOutput)
        self.cbb_component.setMinimumSize(QtCore.QSize(0, 30))
        self.cbb_component.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbb_component.setObjectName("cbb_component")
        self.horizontalLayout_4.addWidget(self.cbb_component)
        self.cbb_compDirec = QtWidgets.QComboBox(self.page_FieldOutput)
        self.cbb_compDirec.setMinimumSize(QtCore.QSize(0, 30))
        self.cbb_compDirec.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbb_compDirec.setObjectName("cbb_compDirec")
        self.horizontalLayout_4.addWidget(self.cbb_compDirec)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(20)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rB_filterByNum = QtWidgets.QRadioButton(self.page_FieldOutput)
        self.rB_filterByNum.setMinimumSize(QtCore.QSize(0, 30))
        self.rB_filterByNum.setMaximumSize(QtCore.QSize(16777215, 30))
        self.rB_filterByNum.setObjectName("rB_filterByNum")
        self.horizontalLayout.addWidget(self.rB_filterByNum)
        self.lineEdit_filter = QtWidgets.QLineEdit(self.page_FieldOutput)
        self.lineEdit_filter.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_filter.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_filter.setObjectName("lineEdit_filter")
        self.horizontalLayout.addWidget(self.lineEdit_filter)
        self.horizontalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rB_filterByFunc = QtWidgets.QRadioButton(self.page_FieldOutput)
        self.rB_filterByFunc.setMinimumSize(QtCore.QSize(0, 30))
        self.rB_filterByFunc.setMaximumSize(QtCore.QSize(16777215, 30))
        self.rB_filterByFunc.setObjectName("rB_filterByFunc")
        self.horizontalLayout_2.addWidget(self.rB_filterByFunc)
        self.cbb_function = QtWidgets.QComboBox(self.page_FieldOutput)
        self.cbb_function.setMinimumSize(QtCore.QSize(0, 30))
        self.cbb_function.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbb_function.setObjectName("cbb_function")
        self.horizontalLayout_2.addWidget(self.cbb_function)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.widget_finalValue = QtWidgets.QWidget(self.page_FieldOutput)
        self.widget_finalValue.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_finalValue.setObjectName("widget_finalValue")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_finalValue)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem1 = QtWidgets.QSpacerItem(255, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.label_FieldResult = QtWidgets.QLabel(self.widget_finalValue)
        self.label_FieldResult.setMinimumSize(QtCore.QSize(400, 0))
        self.label_FieldResult.setText("")
        self.label_FieldResult.setObjectName("label_FieldResult")
        self.horizontalLayout_9.addWidget(self.label_FieldResult)
        spacerItem2 = QtWidgets.QSpacerItem(254, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.widget_finalValue)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.stackedWidget.addWidget(self.page_FieldOutput)
        self.page_HistoryOutput = QtWidgets.QWidget()
        self.page_HistoryOutput.setObjectName("page_HistoryOutput")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_HistoryOutput)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_region = QtWidgets.QLabel(self.page_HistoryOutput)
        self.label_region.setMinimumSize(QtCore.QSize(0, 30))
        self.label_region.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_region.setObjectName("label_region")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_region)
        self.cbb_region = QtWidgets.QComboBox(self.page_HistoryOutput)
        self.cbb_region.setMinimumSize(QtCore.QSize(0, 30))
        self.cbb_region.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbb_region.setObjectName("cbb_region")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbb_region)
        self.label_type = QtWidgets.QLabel(self.page_HistoryOutput)
        self.label_type.setMinimumSize(QtCore.QSize(0, 30))
        self.label_type.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_type.setObjectName("label_type")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_type)
        self.cbb_type = QtWidgets.QComboBox(self.page_HistoryOutput)
        self.cbb_type.setMinimumSize(QtCore.QSize(0, 30))
        self.cbb_type.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbb_type.setObjectName("cbb_type")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cbb_type)
        self.label_Function = QtWidgets.QLabel(self.page_HistoryOutput)
        self.label_Function.setMinimumSize(QtCore.QSize(0, 30))
        self.label_Function.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_Function.setObjectName("label_Function")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_Function)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.cbb_function_2 = QtWidgets.QComboBox(self.page_HistoryOutput)
        self.cbb_function_2.setMinimumSize(QtCore.QSize(0, 30))
        self.cbb_function_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbb_function_2.setObjectName("cbb_function_2")
        self.horizontalLayout_8.addWidget(self.cbb_function_2)
        self.label_finalResult = QtWidgets.QLabel(self.page_HistoryOutput)
        self.label_finalResult.setMinimumSize(QtCore.QSize(0, 30))
        self.label_finalResult.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_finalResult.setObjectName("label_finalResult")
        self.horizontalLayout_8.addWidget(self.label_finalResult)
        self.formLayout_3.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_8)
        self.verticalLayout_2.addLayout(self.formLayout_3)
        self.widget_chart = myLineChart(self.page_HistoryOutput)
        self.widget_chart.setObjectName("widget_chart")
        self.verticalLayout_2.addWidget(self.widget_chart)
        self.verticalLayout_2.setStretch(1, 1)
        self.stackedWidget.addWidget(self.page_HistoryOutput)
        self.verticalLayout_3.addWidget(self.stackedWidget)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.Btn_yes = QtWidgets.QPushButton(Form)
        self.Btn_yes.setMinimumSize(QtCore.QSize(80, 40))
        self.Btn_yes.setMaximumSize(QtCore.QSize(80, 40))
        self.Btn_yes.setObjectName("Btn_yes")
        self.horizontalLayout_6.addWidget(self.Btn_yes)
        self.Btn_cancel = QtWidgets.QPushButton(Form)
        self.Btn_cancel.setMinimumSize(QtCore.QSize(80, 40))
        self.Btn_cancel.setMaximumSize(QtCore.QSize(80, 40))
        self.Btn_cancel.setObjectName("Btn_cancel")
        self.horizontalLayout_6.addWidget(self.Btn_cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_name.setText(_translate("Form", "名称"))
        self.label_step.setText(_translate("Form", "STEP"))
        self.rB_FieldOutput.setText(_translate("Form", "场输出"))
        self.rB_HistoryOutput.setText(_translate("Form", "历程输出"))
        self.label_frame.setText(_translate("Form", "FRAME"))
        self.label_instanceORnodeset.setText(_translate("Form", "INSTANCE/NODESET"))
        self.label_component.setText(_translate("Form", "COMPONENT"))
        self.rB_filterByNum.setText(_translate("Form", "FilterByNumber"))
        self.rB_filterByFunc.setText(_translate("Form", "FilterByFunction"))
        self.label_region.setText(_translate("Form", "HISTORY REGION"))
        self.label_type.setText(_translate("Form", "TYPE"))
        self.label_Function.setText(_translate("Form", "FUNCTION"))
        self.label_finalResult.setText(_translate("Form", "(x：；y：)"))
        self.Btn_yes.setText(_translate("Form", "确定"))
        self.Btn_cancel.setText(_translate("Form", "取消"))
from PublicTool.myLineChart import myLineChart
