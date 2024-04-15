from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QTableWidget, QHBoxLayout, QTableWidgetItem, QLabel, QComboBox, QHeaderView, QFrame, QListView
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from AnalyzeProcessTemplates.public import TemplateNameEnum
from ui.paraSetting.myTableWidget import myTableWidget

class DOEParamSetting(myTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.__initUI__()

    def initUI(self):
        self.setRowCount(3)
        self.setColumnCount(2)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(self.itemHeight)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 表格宽度自适应内容宽度
        self.createDOEParametersItem()

        # 如果是从计算文件中获取的变量，则需要插入数据
        doeData = ReadandWriteTemplateConf().data_DOE.doe_VariablesValueRange
        if ReadandWriteTemplateConf().usrChoosnTemplate == TemplateNameEnum.Template_opt_FE.value:
            designVariable = ReadandWriteTemplateConf().data_FECalcuFile.designVariable
            if designVariable is not None:
                currentRow = 2
                for paramName, value in designVariable.items():
                    self.insertDesignVariableRowToTable(currentRow, paramName, value[0]) #将设计变量显示到界面
                    currentRow += 1
        else:
            if len(doeData) > 0: # 如果DOE数据结构中已经存在数据，则直接显示在UI
                currentRow = 2
                for paramName, value in doeData.items():
                    self.insertDesignVariableRowToTable(currentRow, paramName, value)  # 将设计变量显示到界面
                    currentRow += 1

    def __initUI__(self):
        self.lineEdit_SampleNum.setValidator(QIntValidator(self.lineEdit_SampleNum))
        self.lineEdit_variNum.setValidator(QIntValidator(self.lineEdit_variNum))

    def createDOEParametersItem(self):
        """创建DOE需要输入的参数表"""
        # 实验设计方法选择
        self.setMyItem(0, 0, '实验设计方法')
        confFile = ReadandWriteTemplateConf()
        strDOEName = confFile.getDOENameList()
        self.chooseDOEWays = self.setQcomboBoxCellWidget(strDOEName.split(";"))
        self.setCellWidget(0, 1, self.chooseDOEWays)
        if confFile.data_DOE.doe_Method is not None: # 将默认值显示到UI
            self.chooseDOEWays.setCurrentText(confFile.data_DOE.doe_Method)
        else:
            confFile.data_DOE.doe_Method = self.chooseDOEWays.itemText(0)
        # 变量个数：
        # 如果是从FECalcuFile中读取设置的参数，则直接显示参数个数，不需要在此进行参数个数及设计范围输入
        # 如果是直接进行参数设置，则需要用户自行输入参数个数和每个参数的设计范围
        self.setMyItem(1, 0, '变量个数')
        self.lineEdit_variNum = self.setQLineEditCellWidget('', 'variableNumLineEdit')
        if TemplateNameEnum.Template_opt_FE.value == ReadandWriteTemplateConf().usrChoosnTemplate:
            designVariNum = len(confFile.data_FECalcuFile.designVariable) #获取当前设计变量的个数
            self.lineEdit_variNum.setText(str(designVariNum))
            self.lineEdit_variNum.setEnabled(False)
            confFile.data_DOE.doe_VariablesNum = designVariNum
        else:
            designVariNum = confFile.data_DOE.doe_VariablesNum
            self.lineEdit_variNum.setText(str(designVariNum))
        self.setCellWidget(1, 1, self.lineEdit_variNum)
        self.lineEdit_variNum.textChanged.connect(self.slotVariableNumLineEditChanged)
        # 样本数量
        self.setMyItem(2, 0, '样本数量')
        self.lineEdit_SampleNum = self.setQLineEditCellWidget('', 'sampleNumLineEdit')
        self.setCellWidget(2, 1, self.lineEdit_SampleNum)
        if confFile.data_DOE.doe_SampleSize == 0:
            variNum = confFile.data_DOE.doe_VariablesNum
            confFile.data_DOE.doe_SampleSize = 20 * variNum
        self.lineEdit_SampleNum.setText(str(confFile.data_DOE.doe_SampleSize))
        self.lineEdit_SampleNum.textChanged.connect(self.slotSampleNumLineEditTextChanged)

    def slotVariableNumLineEditChanged(self, strVariNum):
        """变量个数改变时的槽函数"""
        ReadandWriteTemplateConf().data_DOE.doe_VariablesNum = strVariNum
        # 在倒数第二行插入或者删除需要新增或者减少的变量
        currentRowCount = self.rowCount()
        if currentRowCount >= 3:
            currentVariNum = currentRowCount - 3
            if strVariNum != "":
                intVariNum = int(strVariNum)
                if intVariNum > currentVariNum: #需要插入行
                    for i in range(currentRowCount-1, intVariNum+2):
                        self.insertDesignVariableRowToTable(i)
                else: # 需要删除行
                    row = currentRowCount - 2
                    while row >= intVariNum + 2:
                        self.deleteSpecifiedRowInTable(row)
                        row -= 1

    def clearTable(self):
        """删除现有表格"""
        rowCount = self.rowCount() - 1
        while rowCount >= 1:
            self.deleteSpecifiedRowInTable(rowCount)
            rowCount -= 1

    def deleteSpecifiedRowInTable(self, row):
        item = self.item(row, 0)
        paramName = item.text()
        self.removeCellWidget(row, 1)
        self.removeRow(row)
        # 更新数据结构
        data = ReadandWriteTemplateConf().data_DOE.doe_VariablesValueRange
        if data.get(paramName) is not None:
            del data[paramName]

    def insertDesignVariableRowToTable(self, row, variableName = None, variableRange = None):
        if variableRange is None and variableRange is None: # 没有给定设计变量范围，可编辑
            if ReadandWriteTemplateConf().usrChoosnTemplate != TemplateNameEnum.Template_opt_FE.value:
                variableName = f"变量_{row - 1}"
                variableRange = ["", ""]
            else:
                print("参数设置有误，请前往FECalcuFile进行修改！！！")
                pass
        if variableRange is not None and variableRange is not None: # 给了设计变量范围，不可编辑
            self.insertRow(row)
            self.setMyItem(row, 0, variableName, False, Qt.AlignCenter)
            item = self.createValueRangeItem(variableRange, row)
            self.setCellWidget(row, 1, item)
            self.findChild(QLineEdit, f"low_{row}").editingFinished.connect(self.slotLineEditTextChanged)
            self.findChild(QLineEdit, f"up_{row}").editingFinished.connect(self.slotLineEditTextChanged)
            self.updateDOEDataStructureVariablesRange(variableName, variableRange) # 更新数据结构
            if ReadandWriteTemplateConf().usrChoosnTemplate == TemplateNameEnum.Template_opt_FE.value:
                item.setEnabled(False)

    def slotLineEditTextChanged(self):
        data = ReadandWriteTemplateConf().data_DOE
        objName = self.sender().objectName()
        currentText = self.sender().text()
        features = objName.split("_")
        if len(features) == 2:
            paramName = self.item(int(features[1]), 0).text()
            if features[0] == "low":
                data.updateVariableRangeLowByName(paramName, float(currentText))
            elif features[0] == "up":
                data.updateVariableRangeUpByName(paramName, float(currentText))

    def slotSampleNumLineEditTextChanged(self, sampleSize):
        if sampleSize:
            ReadandWriteTemplateConf().data_DOE.doe_SampleSize = int(sampleSize)

    def updateDOEDataStructureVariablesRange(self, paramName, range):
        data = ReadandWriteTemplateConf().data_DOE.doe_VariablesValueRange
        if len(data) > 0:
            if data.get(paramName) is None:
                data[paramName] = range
            else:
                print(f"参数名（{paramName}）重复, 请更改！！！")
        else:
            data[paramName] = range