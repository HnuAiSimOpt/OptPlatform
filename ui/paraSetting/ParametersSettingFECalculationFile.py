from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QTableWidget, QHBoxLayout, QTableWidgetItem, QFileDialog, \
    QFrame
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from configFile.ReadTemplateConf import *
from FiniteElementCalculationFileProcessing.widget.myTextEdit import myTextEdit
from PostProcessing.ReadCAEResults.SubmitCalculation import SubmitCalculation
from PostProcessing.ReadCAEResults.DefineOutputByD3plotFile import DefineLsDynaOutput
from PostProcessing.ReadCAEResults.ReadLsDynaResultsFile import ReadLsDynaResultsFile
from PostProcessing.ReadCAEResults.ReadRwforcFile import ReadRwforcFile
from ui.paraSetting.myTableWidget import myTableWidget
from PostProcessing.ReadCAEResults.ChooseFileType import ChooseFileType
from PostProcessing.ReadCAEResults.DefineOutputByODBFile import DefineOutputByODBFile, ParsingODBFile
from PostProcessing.ReadCAEResults.DefineOutputByMultiFile import ReadMultiResultFile
import os
from AnalyzeProcessTemplates.public import SolverFileTyeEnum
from PublicTool.myMaskWidget import myMaskWidget
from PublicTool.myPublicDialogBackground import myPublicDialogBackground

class FECalcuFileParamSetting(myTableWidget):
    strDefineDesignVariable = '设计变量'
    strTestModel = '模型测试'
    strDefineOutput = '响应值'
    def __init__(self, parent):
        super().__init__(parent)
        self.__initUI__()
        # self.__initConnect__()

    def __initUI__(self):
        confFile = ReadandWriteTemplateConf()
        widgetList = self.createOpenFileCellWidget(LineEditObjName='Edit_FEFilePath', BtnObjName='Btn_FEFileData', LineEditText=confFile.data_FECalcuFile.filePath)
        widgetList[2].clicked.connect(self.getDir)
        self.label_OpenFile = widgetList[1]

        """ 设置单元格行和列 隐藏表头"""
        self.setRowCount(1)
        self.setColumnCount(2)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(self.itemHeight)

        OpenFileItem = QTableWidgetItem("计算文件")
        OpenFileItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.setItem(0, 0, OpenFileItem)
        self.setCellWidget(0, 1, widgetList[0])

        self.horizontalHeader().setStretchLastSection(True)

        """设置单元格样式"""
        self.setFocusPolicy(Qt.NoFocus) # 选中单元格时不出现虚线框

        """初始化数据"""
        self.initTableData()

    def initTableData(self):
        data = ReadandWriteTemplateConf().data_FECalcuFile
        if data.filePath != "":
            self.addDefineDesignVariableBtn()
        if data.isEmpty() == False:
            if data.designVariable is not None:
                self.addDefineDesignVariableBtn()
                self.slotDesignVariablesDefined()
                self.addTryCalcuBtn()
                if ReadandWriteTemplateConf().data_FECalcuFile.isTryCalcuCompeleted == True:
                    self.addDefineOutputBtn()
                if len(ReadandWriteTemplateConf().data_FECalcuFile.responseValue) >= 1:
                    self.showOutputValue()


    def __initConnect__(self):
        self.button_OpenFile.clicked.connect(self.getDir)

    def getDir(self):
        dir = QFileDialog.getOpenFileName(self,  "选取文件", os.getcwd(), "All Files (*)") # 设置文件扩展名过滤,用双分号间隔
        if dir[0]:
            if self.sender().objectName() == "Btn_FEFileData":
                data = ReadandWriteTemplateConf().data_FECalcuFile
                data.clear() #打开新的文件，删除数据
                self.label_OpenFile.setText(dir[0])
                data.filePath = dir[0]
                self.addDefineDesignVariableBtn()
        else:
            pass

    def addDefineDesignVariableBtn(self):
        """添加定义设计变量按钮"""
        if self.checkVariableNameHasExistedInTable(self.strDefineDesignVariable) == False:
            row = self.rowCount()
            self.insertRow(row)
            self.setMyItem(row, 0, QTableWidgetItem(self.strDefineDesignVariable), False)
            Btn = self.setButtonCellWidget('定义')
            self.setCellWidget(row, 1, Btn)
            Btn.clicked.connect(self.slotDefineDesignVariablesBtnClicked)

    def addTryCalcuBtn(self):
        """参数设置完成之后，在界面添加试计算按钮"""
        if self.checkVariableNameHasExistedInTable(self.strTestModel) == False:
            row = self.rowCount()
            self.insertRow(row)
            self.setMyItem(row, 0, QTableWidgetItem(self.strTestModel), False)
            Btn = self.setButtonCellWidget("提交测试")
            self.setCellWidget(row, 1, Btn)
            Btn.clicked.connect(self.slotSubmitBtn)

    def addDefineOutputBtn(self):
        """添加定义输出按钮"""
        if self.checkVariableNameHasExistedInTable(self.strDefineOutput) == False:
            row = self.rowCount()
            self.insertRow(row)  # 增加一行
            self.setItem(row, 0, QTableWidgetItem(self.strDefineOutput))
            Btn = self.setButtonCellWidget("定义")
            self.setCellWidget(row, 1, Btn)
            Btn.clicked.connect(self.slotDefineOutput)

    def slotDefineDesignVariablesBtnClicked(self):
        """定义设计变量的槽函数"""
        filepath = ReadandWriteTemplateConf().data_FECalcuFile.filePath
        with open(filepath) as f:
            self.fileEditor = myTextEdit(filepath, f.read())
            self.mask = myMaskWidget(self.parent().parent().parent())
            backgroundWidget = myPublicDialogBackground()
            backgroundWidget.setTitle('定义设计变量')
            backgroundWidget.setWidget(self.fileEditor)
            self.mask.layout().addWidget(backgroundWidget)
            self.mask.show()
            #self.fileEditor.show()
            self.fileEditor.updateParamShowMsg.connect(self.slotDesignVariablesDefined)

    def slotDesignVariablesDefined(self):
        """参数设置完成，在界面显示参数名称及对应的取值范围"""
        dict_param = ReadandWriteTemplateConf().data_FECalcuFile.designVariable
        # 将参数显示到界面中
        if len(dict_param) > 0:
            for paramName, value in dict_param.items():
                if self.checkVariableNameHasExistedInTable(paramName) == False:
                    rowCount = self.getRowIndexBySpecialString(self.strTestModel)
                    if rowCount == 0:
                        return
                    self.insertRow(rowCount)  # 增加一行
                    self.setMyItem(rowCount, 0, paramName, aligen=Qt.AlignCenter)
                    item_variableRange = self.createValueRangeItemAndCreateConnect(value[0], rowCount)
                    if item_variableRange is not None:
                        self.setCellWidget(rowCount, 1, item_variableRange)
                    else:
                        print("创建控件失败")
            self.addTryCalcuBtn()

    def checkVariableNameHasExistedInTable(self, variableName):
        """
        查找某个变量名是否已经存在于表格中
        :param variableName: 变量名
        :return: 存在返回True
        """
        row = self.rowCount()
        for index_row in range(row):
            if self.item(index_row, 0).text() == variableName:
                return True
        return False

    def clearTable(self):
        """删除现有内容"""
        rowCount = self.rowCount() - 1
        while rowCount >= 1:
            self.removeCellWidget(rowCount, 1)
            self.removeRow(rowCount)
            rowCount -= 1

    def createValueRangeItemAndCreateConnect(self, range, row):
        """创建取值范围item"""
        rangeWidget = self.createValueRangeItem(range, row)
        if rangeWidget:
            lineeditList = rangeWidget.findChildren(QLineEdit)
            for lineedit in lineeditList:
                lineedit.editingFinished.connect(self.slotLineEditTextChanged)
            return rangeWidget
        return None

    def slotLineEditTextChanged(self):
        data = ReadandWriteTemplateConf().data_FECalcuFile
        objName = self.sender().objectName()
        currentText = self.sender().text()
        features = objName.split("_")
        if len(features) == 2:
            if currentText != "":
                paramName = self.item(int(features[1]), 0).text()
                if features[0] == "low":
                    data.changeDesignVariableLowByParamName(paramName, float(currentText))
                elif features[0] == "up":
                    data.changeDesignVariableUpByParamName(paramName, float(currentText))

    def slotSubmitBtn(self):
        """
        提交计算按钮的槽函数
        :return:
        """
        self.widget = SubmitCalculation(self.label_OpenFile.text())
        self.mask = myMaskWidget(self.parent().parent().parent())
        backgroundWidget = myPublicDialogBackground()
        backgroundWidget.setTitle('提交试计算')
        backgroundWidget.setWidget(self.widget)
        self.mask.layout().addWidget(backgroundWidget)
        self.mask.show()
        self.widget.calcuCompeleteMsg.connect(self.slotTryCalcuCompelete)

    def slotTryCalcuCompelete(self):
        """有限元文件试计算正常结束，触发此函数：更改试计算按钮样式，添加定义输出按钮"""
        #计算完成，更改该提交计算按钮前的状态
        ReadandWriteTemplateConf().data_FECalcuFile.isTryCalcuCompeleted = True
        self.addDefineOutputBtn()

    def slotDefineOutput(self):
        """根据结果文件定义输出"""
        if ReadandWriteTemplateConf().data_Simulation.solver == SolverTypeEnum.LsDyna:
            self.chooseFile = ChooseFileType()
            self.mask = myMaskWidget(self.parent().parent().parent())
            backgroundWidget = myPublicDialogBackground()
            backgroundWidget.setTitle('选择结果文件类型')
            backgroundWidget.setWidget(self.chooseFile, True)
            self.mask.layout().addWidget(backgroundWidget)
            self.mask.show()
            self.chooseFile.msg.connect(self.slotOutputValueDefinedCompleted)
        elif ReadandWriteTemplateConf().data_Simulation.solver == SolverTypeEnum.Abaqus:
            filePath = ReadandWriteTemplateConf().data_Simulation.folderPath
            odbFileName = ReadandWriteTemplateConf().data_FECalcuFile.filePath
            odbFileName = odbFileName[odbFileName.rfind('/'): odbFileName.rfind('.')]
            ReadandWriteTemplateConf().data_Simulation.fileName = odbFileName
            ODBFilePath = filePath + 'TryCalculation' + odbFileName + '.odb'
            if os.path.exists(ODBFilePath):
                self.abaqusFilePrasing = DefineOutputByODBFile(ODBFilePath)
                self.mask = myMaskWidget(self.parent().parent().parent())
                backgroundWidget = myPublicDialogBackground()
                backgroundWidget.setTitle('ODB文件解析及响应值定义')
                backgroundWidget.setWidget(self.abaqusFilePrasing, False)
                self.mask.layout().addWidget(backgroundWidget)
                self.mask.show()
                self.abaqusFilePrasing.msg.connect(self.slotOutputValueDefinedCompleted)

    def seekFile(self, path, name):
        """
        查找指定文件
        :param path: 文件路径
        :param name: 需要查找的文件名
        :return: 文件地址
        """
        for root, dirs, files in os.walk(path):
            if name in files:
                return f"{path}/{name}"
        return None

    def slotOutputValueDefinedCompleted(self, outputName):
        """
        响应值定义完成的槽函数，将响应名称及对应的值显示到界面
        :param outputName: 响应值名称
        :return:
        """
        response = ReadandWriteTemplateConf().data_FECalcuFile.responseValue
        dictParameters = response.get(outputName)
        FilePath = dictParameters.get("filePath")
        FileType = dictParameters.get('fileType')
        if FilePath is None and FileType != SolverFileTyeEnum.multi.value:
            logging.getLogger().info("未找到对应的结果文件，请重新计算！")
            return
        targetValue = None
        if FileType == SolverFileTyeEnum.d3plot.value:
            if ReadLsDynaResultsFile().loadResultFile(FilePath):
                targetValue = ReadLsDynaResultsFile().getOutputValueByParameters(dictParameters)
        elif FileType == SolverFileTyeEnum.rwforc.value:
            if ReadRwforcFile().praserFile(FilePath):
                targetValue = ReadRwforcFile().getOutputValueByParameters(dictParameters)
        elif FileType == SolverFileTyeEnum.odb.value:
            readResult = ParsingODBFile()
            targetValue = readResult.getOutputValueByParameters(dictParameters)
        elif FileType == SolverFileTyeEnum.multi.value:
            readResult = ReadMultiResultFile()
            targetValue = readResult.getOutputValueByParameters(dictParameters)
        if targetValue is not None:
            row = self.rowCount()
            # 添加输出名称及值
            self.insertRow(row)  # 增加一行
            self.setMyItem(row, 0, outputName, False, aligen=Qt.AlignCenter)
            self.setMyItem(row, 1, str(targetValue), False)
        try:
            self.chooseFile.close()
        except:
            pass

    def showOutputValue(self):
        response = ReadandWriteTemplateConf().data_FECalcuFile.responseValue
        for key, value in response.items():
            if self.checkVariableNameHasExistedInTable(key) == False:
                self.slotOutputValueDefinedCompleted(key)

