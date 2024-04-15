from FiniteElementCalculationFileProcessing.ui.Ui_setVariableDialog import Ui_setVariable
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from AnalyzeProcessTemplates.public import *
from PublicTool.myMaskWidget import myMaskWidget

class Dialog_setVariable(QWidget, Ui_setVariable):
    sendmsg = pyqtSignal()
    def __init__(self, row, col, selectedStr):
        super().__init__()
        self.setupUi(self)
        self.position = [row, col]
        self.selectedStr = selectedStr
        self.designVariable = ReadandWriteTemplateConf().data_FECalcuFile.designVariable
        self.__initConnect__()
        self.upValue = None
        self.lowValue = None
        self.label_err.setStyleSheet('QLabel#label_err{color:red}')
        self.Btn_cancel.setStyleSheet(getBtnStyleString())
        self.Btn_ok.setStyleSheet(getBtnStyleString())
        self.line.setStyleSheet('QFrame#line{color:#f4f6e0}')
        self.label_err.hide()

    def __initConnect__(self):
        self.Btn_ok.clicked.connect(self.slotOKBtnClicked)
        self.Btn_cancel.clicked.connect(self.slotCancelBtnClicked)
        self.lineEdit_variableName.editingFinished.connect(self.slotVariableNameEditingFinished)
        self.lineEdit_lowRange.editingFinished.connect(self.slotVariableRangeEditingFinished)
        self.lineEdit_upRange.editingFinished.connect(self.slotVariableRangeEditingFinished)

    def slotVariableNameEditingFinished(self):
        variableName = self.lineEdit_variableName.text()
        if variableName in self.designVariable:
            # 该变量名已存在
            str = f"{variableName}(该变量名称已存在，请更改！)"
            self.label_err.setText(str)
            self.label_err.show()
        else:
            self.label_err.hide()

    def slotVariableRangeEditingFinished(self):
        strLowValue = self.lineEdit_lowRange.text()
        strUpValue = self.lineEdit_upRange.text()
        LowValue_decimal = findDecimalPointPos(strLowValue)
        UpValue_decimal = findDecimalPointPos(strUpValue)
        self.decimal = max(LowValue_decimal[0], UpValue_decimal[0])
        self.isSciNotation = LowValue_decimal[1] or UpValue_decimal[1]
        if strLowValue:
            self.lowValue = translateStringToFloat(strLowValue, self.decimal, self.isSciNotation)
        else:
            self.lowValue = None
        if strUpValue:
            self.upValue = translateStringToFloat(strUpValue, self.decimal, self.isSciNotation)
        else:
            self.upValue = None
        if self.lowValue is None or self.upValue is None:
            return
        if float(self.lowValue) >= float(self.upValue):
            # 变量的下限大于上限
            self.label_err.setText('变量范围设置错误，请重新设置！')
            self.label_err.show()
        else:
            self.label_err.hide()

    def slotOKBtnClicked(self):
        if self.lowValue is None or self.upValue is None:
            return
        variableName = self.lineEdit_variableName.text()
        if variableName in self.designVariable:
            # 该变量名已存在
            str = f"{variableName}：该变量名称已存在，请更改！"
            self.label_err.setText(str)
            self.label_err.show()
            return
        else:
            if float(self.lowValue) >= float(self.upValue):
                # 变量的下限大于上限
                self.label_err.setText('变量范围设置错误，请重新设置！')
                self.label_err.show()
                return
            valueRange = [float(self.lowValue), float(self.upValue)]
            value = [valueRange, self.position, self.selectedStr, self.decimal, self.isSciNotation]
            self.designVariable[variableName] = value
            self.sendmsg.emit()
            parent = self.parent()
            while not isinstance(parent, myMaskWidget):
                parent = parent.parent()
            parent.close()

    def slotCancelBtnClicked(self):
        parent = self.parent()
        while not isinstance(parent, myMaskWidget):
            parent = parent.parent()
        parent.close()