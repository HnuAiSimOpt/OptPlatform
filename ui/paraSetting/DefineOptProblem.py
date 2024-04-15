from ui.paraSetting.ui.Ui_DefineOptProblem import Ui_Form
from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QListView
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from AnalyzeProcessTemplates.public import *
from PyQt5 import QtGui, Qt
from PyQt5.QtCore import Qt
from ui.paraSetting.DefineOptTarget import DefineOptTarget
import logging
from PublicTool.myMaskWidget import myMaskWidget
from AnalyzeProcessTemplates.public import getBtnStyleString
from PublicTool.myPublicDialogBackground import myPublicDialogBackground

class DefineOptProblem(QWidget, Ui_Form):
    def __init__(self):
        super(DefineOptProblem, self).__init__()
        self.setupUi(self)
        self.__initUI__()
        self.getTargetAndShowInTable()
        self.getConstrainAndShowInTable()
        self.getVariableNumAndShowDesignRangeInTable()
        self.__initConnect__()

    def __initUI__(self):
        self.lineEdit_optTargetNum.setValidator(QtGui.QIntValidator())
        self.lineEdit_constrainNum.setValidator(QtGui.QIntValidator())
        self.lineEdit_variableNum.setEnabled(False)
        self.Btn_cancel.setStyleSheet(getBtnStyleString())
        self.Btn_yes.setStyleSheet(getBtnStyleString())
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def __initConnect__(self):
        self.lineEdit_optTargetNum.editingFinished.connect(self.slotOptTargetNumChanged)
        self.lineEdit_constrainNum.editingFinished.connect(self.slotConstrainsNumChanged)
        self.Btn_yes.clicked.connect(self.slotYesButtonClicked)
        self.Btn_cancel.clicked.connect(self.slotCancelButtonClicked)

    def getVariableNumAndShowDesignRangeInTable(self):
        """获取设计变量个数，并且将变量的设计范围写入表格中，作为优化问题中各个变量的上下限"""
        variables = None
        if ReadandWriteTemplateConf().usrChoosnTemplate == TemplateNameEnum.Template_opt_FE.value:
            variables = ReadandWriteTemplateConf().data_DOE.doe_VariablesValueRange
        if ReadandWriteTemplateConf().usrChoosnTemplate == TemplateNameEnum.Template_opt.value:
            variables = ReadandWriteTemplateConf().data_DataInput.DataFile_VariableRange

        #################################################
        # todo 没有doe的计算流程，从输入数据中查找变量的取值范围 变量的取值范围是dict类型的数据 {'变量名': [下限, 上限]}
        if variables is None:
            return
        variNum = len(variables)
        self.lineEdit_variableNum.setText(str(variNum))
        self.TW_variableNum.setRowCount(variNum)
        self.TW_variableNum.setColumnCount(2)
        # self.TW_variableNum.setColumnWidth(0, self.TW_variableNum.width() * 0.2)
        # self.TW_variableNum.setColumnWidth(1, self.TW_variableNum.width() * 0.8)
        self.addDataToVariablesTable(variables)
        self.updateTableSize()

    def getTargetAndShowInTable(self):
        """从数据结构查找目前已定义优化目标，并显示在UI"""
        targetData = ReadandWriteTemplateConf().data_OptimizationAlgorithm.Opt_AlgorithmProblem_target
        num = len(targetData)
        self.lineEdit_optTargetNum.setText(str(num))
        if len(targetData.items()) > 0:
            self.getOptTargetNumAndShowInTable(num, targetData.items())

    def getConstrainAndShowInTable(self):
        """获取约束条件，显示到UI"""
        constrData = ReadandWriteTemplateConf().data_OptimizationAlgorithm.Opt_AlgorithmProblem_constrains
        num = len(constrData)
        self.lineEdit_constrainNum.setText(str(num))
        if len(constrData.items()) > 0:
            self.getConstrainsNumAndShowInTable(num, constrData.items())

    def slotOptTargetNumChanged(self):
        targetNum = int(self.lineEdit_optTargetNum.text())
        self.getOptTargetNumAndShowInTable(targetNum)
        self.updateTableSize()

    def slotConstrainsNumChanged(self):
        constrNum = int(self.lineEdit_constrainNum.text())
        self.getConstrainsNumAndShowInTable(constrNum)
        self.updateTableSize()

    def getOptTargetNumAndShowInTable(self, num, valueList=[]):
        """获取优化目标，并显示到表格"""
        responses = ReadandWriteTemplateConf().data_SurrogateModel.SM_Model
        # if len(responses) == 0:
        #     return
        self.spanRow = 2
        currentNum = self.TW_optTargetNum.rowCount() // self.spanRow
        # 当前表格无数据
        if currentNum == 0:
            self.TW_optTargetNum.setRowCount(self.spanRow * num)
            self.TW_optTargetNum.setColumnCount(2)
            index = 0
            while index < self.spanRow*num:
                # self.TW_optTargetNum.setColumnWidth(0, self.TW_optTargetNum.width() * 0.2)
                # self.TW_optTargetNum.setColumnWidth(1, self.TW_optTargetNum.width() * 0.8)
                self.TW_optTargetNum.setSpan(index, 0, self.spanRow, 1)
                self.TW_optTargetNum.setSpan(index, 1, self.spanRow, 1)
                rowNum = index//self.spanRow
                if len(valueList) >= rowNum and len(valueList):
                    tmpValue = list(valueList)[rowNum]
                    self.TW_optTargetNum.setMyItem(index, 0, tmpValue[0], False)
                    widget = DefineOptTarget(self.TW_optTargetNum, tmpValue[1][0], tmpValue[1][1])
                    self.TW_optTargetNum.setCellWidget(index, 1, widget)
                else:
                    self.TW_optTargetNum.setMyItem(index, 0, f'Target_{rowNum}', False)
                    self.TW_optTargetNum.setCellWidget(index, 1, DefineOptTarget(self.TW_optTargetNum))
                index += self.spanRow
        elif currentNum > num:
            self.TW_optTargetNum.setRowCount(self.spanRow * num)
        elif currentNum < num:
            while currentNum < num:
                currentRow = currentNum * self.spanRow
                self.TW_optTargetNum.insertRow(currentRow)
                self.TW_optTargetNum.insertRow(currentRow + 1)
                self.TW_optTargetNum.setSpan(currentRow, 0, self.spanRow, 1)
                self.TW_optTargetNum.setSpan(currentRow, 1, self.spanRow, 1)
                # self.TW_optTargetNum.setColumnWidth(0, self.TW_optTargetNum.width() * 0.2)
                # self.TW_optTargetNum.setColumnWidth(1, self.TW_optTargetNum.width() * 0.8)
                self.TW_optTargetNum.setMyItem(currentRow, 0, f'Target_{currentNum}', False)
                self.TW_optTargetNum.setCellWidget(currentRow, 1, DefineOptTarget(self.TW_optTargetNum))
                currentNum += 1
        elif currentNum == num:
            print('行数相等，不做任何操作')

    def addDataToVariablesTable(self, variables: dict):
        """
        添加变量名称及变量取值范围到表格中
        :param variables: 变量名称及取值范围 dict
        :return:
        """
        index = 0
        for variableName, range in variables.items():
            self.TW_variableNum.setMyItem(index, 0, variableName, False)
            self.TW_variableNum.setCellWidget(index, 1, self.TW_variableNum.createValueRangeItem(range, index))
            index += 1

    def getConstrainsNumAndShowInTable(self, num, valueList=[]):
        """获取约束个数，显示在表格中"""
        currentNum = self.TW_constrainNum.rowCount()
        if currentNum == 0:
            self.TW_constrainNum.setColumnCount(3)
            self.TW_constrainNum.setRowCount(num)
            tablewidth = self.TW_constrainNum.width()
            # self.TW_constrainNum.setColumnWidth(0, tablewidth * 0.2)
            # self.TW_constrainNum.setColumnWidth(1, tablewidth * 0.7)
            # lastWidth = tablewidth - tablewidth * 0.2 - tablewidth * 0.7
            # self.TW_constrainNum.setColumnWidth(2, lastWidth)
            for index in range(num):
                if len(valueList) > index and len(valueList):
                    tmpValue = list(valueList)[index]
                    self.TW_constrainNum.setMyItem(index, 0, tmpValue[0], False)
                    self.TW_constrainNum.setCellWidget(index, 1,
                                                       self.TW_variableNum.setQLineEditCellWidget(tmpValue[1], f'ConstrainText_{index}'))
                else:
                    self.TW_constrainNum.setMyItem(index, 0, f'Constrain_{index}', False)
                    self.TW_constrainNum.setCellWidget(index, 1,
                                                       self.TW_variableNum.setQLineEditCellWidget('', f'ConstrainText_{index}'))
        elif currentNum > num:
            self.TW_constrainNum.setRowCount(num)
        elif currentNum < num:
            while currentNum < num:
                self.TW_constrainNum.insertRow(currentNum)
                self.TW_constrainNum.setMyItem(currentNum, 0, f'Constrain_{currentNum}', False)
                self.TW_constrainNum.setCellWidget(currentNum, 1,
                                                   self.TW_variableNum.setQLineEditCellWidget('', f'ConstrainText_{currentNum}'))
                currentNum += 1
        for index in range(num):
            self.TW_constrainNum.setMyItem(index, 2, '<=0', False)

    def slotYesButtonClicked(self):
        """确定按钮的槽函数"""
        optData = ReadandWriteTemplateConf().data_OptimizationAlgorithm
        optData.Opt_AlgorithmProblem_constrains.clear()
        optData.Opt_AlgorithmProblem_target.clear()
        optData.Opt_AlgorithmProblem_variUpLow.clear()
        optData.Opt_AlgorithmProblem_variNameList.clear()
        #保存优化问题
        optTargetNum = self.TW_optTargetNum.rowCount() #优化目标数量
        for index in range(optTargetNum):
            if index % self.spanRow == 0:
                cellWidget = self.TW_optTargetNum.cellWidget(index, 1)
                targetName = self.TW_optTargetNum.item(index, 0).text()
                tmpValue = cellWidget.constructOptTarget()
                if tmpValue is not None:
                    optData.Opt_AlgorithmProblem_target[targetName] = tmpValue
        #保存变量上下限及变量名
        variableNum = self.TW_variableNum.rowCount()
        lowList = []
        upList = []
        nameList = []
        for index in range(variableNum):
            cellWidget = self.TW_variableNum.cellWidget(index, 1)
            variableName = self.TW_variableNum.item(index, 0).text()
            upValue = cellWidget.findChild(QLineEdit, f'up_{index}').text()
            lowValue = cellWidget.findChild(QLineEdit, f'low_{index}').text()
            upList.append(upValue)
            lowList.append(lowValue)
            nameList.append(variableName)
        optData.Opt_AlgorithmProblem_variUpLow['up'] = upList
        optData.Opt_AlgorithmProblem_variUpLow['low'] = lowList
        optData.Opt_AlgorithmProblem_variNameList = nameList
        #保存约束条件
        constrainNum = self.TW_constrainNum.rowCount()
        for index in range(constrainNum):
            cellWidget = self.TW_constrainNum.cellWidget(index, 1)
            constrainName = self.TW_constrainNum.item(index, 0).text()
            constrain = cellWidget.text()
            if constrain != '':
                optData.Opt_AlgorithmProblem_constrains[constrainName] = constrain
            else:
                logging.getLogger().info('存在未定义约束条件，请检查！')
                return
        parent = self.parent()
        while not isinstance(parent, myMaskWidget):
            parent = parent.parent()
        parent.close()

    def slotCancelButtonClicked(self):
        """取消按钮槽函数"""
        parent = self.parent()
        while not isinstance(parent, myMaskWidget):
            parent = parent.parent()
        parent.close()

    def resizeEvent(self, e):
        self.updateTableSize()

    def updateTableSize(self):
        totalHeight = 0
        tablewidth = self.width() - 20
        """优化目标表格"""
        if self.TW_optTargetNum.rowCount() <= 6:
            tableheight = self.TW_optTargetNum.rowCount() * self.TW_optTargetNum.rowHeight(0) + 2
        else:
            tableheight = 6 * self.TW_optTargetNum.rowHeight(0) + 2
        totalHeight += tableheight
        self.TW_optTargetNum.changeSize(tablewidth, tableheight)
        if self.TW_optTargetNum.columnCount() == 2:
            self.TW_optTargetNum.setColumnWidth(0, int(tablewidth * 0.2))
            lastWidth = tablewidth - int(tablewidth * 0.2) - 20
            self.TW_constrainNum.setColumnWidth(1, lastWidth)
            rownum = self.TW_optTargetNum.rowCount()
            for index in range(rownum):
                widget = self.TW_optTargetNum.cellWidget(index, 1)
                if widget is not None:
                    widget.changeSize(lastWidth, self.spanRow * self.TW_optTargetNum.rowHeight(index))
        """约束条件表格"""
        rownum = self.TW_constrainNum.rowCount()
        if self.TW_constrainNum.rowCount() <= 4:
            tableheight = self.TW_constrainNum.rowCount() * self.TW_constrainNum.rowHeight(0) + 2
        else:
            tableheight = 4 * self.TW_constrainNum.rowHeight(0) + 2
        totalHeight += tableheight
        self.TW_constrainNum.changeSize(tablewidth, tableheight)
        if self.TW_constrainNum.columnCount() == 3:
            self.TW_constrainNum.setColumnWidth(0, int(tablewidth * 0.2))
            self.TW_constrainNum.setColumnWidth(1, int(tablewidth * 0.7))
            self.TW_constrainNum.setColumnWidth(2, tablewidth - int(tablewidth * 0.2) - int(tablewidth * 0.7))
            for index in range(rownum):
                widget = self.TW_constrainNum.cellWidget(index, 1)
                if widget is not None:
                    widget.setFixedWidth(int(tablewidth * 0.7) - 10)
                    #widget.resize(int(tablewidth * 0.7), self.TW_constrainNum.rowHeight(index))
        """变量"""
        if self.TW_variableNum.rowCount() <= 8:
            tableheight = self.TW_variableNum.rowCount() * self.TW_variableNum.rowHeight(0) + 2
        else:
            tableheight = 8 * self.TW_variableNum.rowHeight(0) + 2
        totalHeight += tableheight
        self.TW_variableNum.changeSize(tablewidth, tableheight)
        if self.TW_variableNum.columnCount() == 2:
            self.TW_variableNum.changeColumnWidth(0, int(tablewidth * 0.2))
            self.TW_variableNum.changeColumnWidth(1, int(tablewidth * 0.8))

        totalHeight += 300
        parent = self.parent()
        # while not isinstance(parent, myPublicDialogBackground):
        #     parent = parent.parent()
        self.setFixedHeight(totalHeight)
        # self.setFixedWidth(totalHeight * 1.2)
        if parent is not None:
            # parent.setFixedWidth(totalHeight * 1.2)
            parent.setFixedHeight(totalHeight)
            parent.parent().setFixedHeight(totalHeight + 40)