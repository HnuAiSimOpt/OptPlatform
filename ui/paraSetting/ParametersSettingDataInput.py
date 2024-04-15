from PyQt5.QtWidgets import QMessageBox, QPushButton, QWidget, QLineEdit, QTableWidget, QHBoxLayout, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from configFile.ReadTemplateConf import *
from ReadingData.ExcelFileReading import *
from ui.paraSetting.myTableWidget import *

class DataInputParamSetting(myTableWidget):
    TrainExcelDataReader = None
    TestExcelDataReader = None

    def __init__(self, parent):
        super().__init__(parent)
        self.__initUI__()
        self.__initConnect__()

    def __initUI__(self):
        confFile = ReadandWriteTemplateConf()
        icon_OpenFile = QIcon()
        icon_OpenFile.addPixmap(QPixmap(":/pic/icons/打开文件.png"), QIcon.Normal, QIcon.Off)
        """ 训练集 打开文件 单元格设置 """
        HboxLayout = QHBoxLayout()
        self.label_OpenFile = QLineEdit(confFile.data_DataInput.DataFile_Path)
        self.label_OpenFile.setFixedHeight(self.itemHeight)
        # self.label_OpenFile.setStyleSheet("background-color:rgb(57, 57, 57); border: black 0px; color : white;")
        HboxLayout.addWidget(self.label_OpenFile)
        self.button_OpenFile = QPushButton()
        self.button_OpenFile.setFixedSize(self.itemHeight, self.itemHeight)
        # self.button_OpenFile.setStyleSheet("background-color:rgb(57, 57, 57);")
        self.button_OpenFile.setIcon(icon_OpenFile)
        self.button_OpenFile.setObjectName("Btn_TrainyData")
        HboxLayout.addWidget(self.button_OpenFile)
        HboxLayout.setContentsMargins(0, 0, 0, 0)
        HboxLayout.setSpacing(0)
        widgetOpenFile = QWidget()
        widgetOpenFile.setLayout(HboxLayout)

        """测试集"""
        HboxLayout_test = QHBoxLayout()
        self.label_OpenFile_Test = QLineEdit(confFile.data_DataInput.DataFile_TestPath)
        self.label_OpenFile_Test.setFixedHeight(self.itemHeight)
        # self.label_OpenFile_Test.setStyleSheet("background-color:rgb(57, 57, 57); border: black 0px; color : white;")
        HboxLayout_test.addWidget(self.label_OpenFile_Test)
        self.button_OpenFile_Test = QPushButton()
        self.button_OpenFile_Test.setFixedSize(self.itemHeight, self.itemHeight)
        #self.button_OpenFile_Test.setStyleSheet("background-color:rgb(57, 57, 57);")
        self.button_OpenFile_Test.setIcon(icon_OpenFile)
        self.button_OpenFile_Test.setObjectName("Btn_TestData")
        HboxLayout_test.addWidget(self.button_OpenFile_Test)
        HboxLayout_test.setContentsMargins(0, 0, 0, 0)
        HboxLayout_test.setSpacing(0)
        widgetOpenFile_Test = QWidget()
        widgetOpenFile_Test.setLayout(HboxLayout_test)

        """ 设置单元格行和列 隐藏表头"""
        self.setRowCount(2)
        self.setColumnCount(2)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(self.itemHeight)

        self.setMyItem(0, 0, "训练数据集", False)
        self.setCellWidget(0, 1, widgetOpenFile)
        self.setMyItem(1, 0, "测试数据集", False)
        self.setCellWidget(1, 1, widgetOpenFile_Test)

        self.horizontalHeader().setStretchLastSection(True)
        # self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents) #表格宽度自适应内容宽度

        """设置单元格样式"""
        self.setFocusPolicy(Qt.NoFocus) # 选中单元格时不出现虚线框
        # self.setStyleSheet("background:rgb(30,30,30); border:1px black; font-size:12px; color:white;"
        #                    "selection-background-color:rgb(30,30,30); selection-color:white")

        """初始化数据"""
        self.initTableData()

    def __initConnect__(self):
        self.button_OpenFile.clicked.connect(self.getDir)
        self.button_OpenFile_Test.clicked.connect(self.getDir)

    def getDir(self):
        dir = QFileDialog.getOpenFileName(self,  "选取文件", os.getcwd(), "All Files (*);;Excel Files (*.xls)") # 设置文件扩展名过滤,用双分号间隔
        if dir[0]:
            if self.sender().objectName() == "Btn_TrainyData":
                self.label_OpenFile.setText(dir[0])
                self.setDataInputDataStaructValue("train")
            elif self.sender().objectName() == "Btn_TestData":
                self.label_OpenFile_Test.setText(dir[0])
                self.setDataInputDataStaructValue("test")
        else:
            pass

    def setDataInputDataStaructValue(self, DataType):
        confFile = ReadandWriteTemplateConf()
        if DataType == "train":
            confFile.data_DataInput.DataFile_Path = self.label_OpenFile.text()
        elif DataType == "test":
            confFile.data_DataInput.DataFile_TestPath = self.label_OpenFile_Test.text()
        self.parseXlsFile(DataType)

    def parseXlsFile(self, DataType):
        """删除原来的UI显示及数据结构中的值"""
        rowCount = self.rowCount()
        rowTest = self.findItems("测试数据集", Qt.MatchExactly)[0].row()
        # 删除表格
        if DataType == "train":
            filePath = ReadandWriteTemplateConf().data_DataInput.DataFile_Path
            while rowTest > 1:
                self.removeCellWidget(rowTest - 1, 1)
                self.removeRow(rowTest - 1)
                rowTest -= 1
            self.TrainExcelDataReader = ExcelReader(filePath)
            sheetNameList = self.TrainExcelDataReader.getAllSheetsNames()
        elif DataType == "test":
            filePath = ReadandWriteTemplateConf().data_DataInput.DataFile_TestPath
            if rowCount > rowTest:
                while rowCount - 1 > rowTest:
                    self.removeCellWidget(rowCount - 1, 1)
                    self.removeRow(rowCount - 1)
                    rowCount -= 1
            self.TestExcelDataReader = ExcelReader(filePath)
            sheetNameList = self.TestExcelDataReader.getAllSheetsNames()

        self.showDataParamInTable(DataType, "sheet选择", sheetNameList)
        if len(sheetNameList) > 0:
            self.setVariableAndOutputData(DataType, sheetNameList[0]) #默认的输出数为1,默认选择第一个sheet
            self.addCellToTable(dataType=DataType)

    def setVariableAndOutputData(self, dataType, sheetName, varNum=0):
        """
        从excel读取的数据存储至数据结构中
        :param sheetName: 表格名
        :param dataType: 数据类型（是测试数据还是训练数据）
        :param varNum: 变量个数
        :return:
        """
        if dataType == "test":
            excelFileData = self.TestExcelDataReader
        else:
            excelFileData = self.TrainExcelDataReader
        self.inputData = excelFileData.getSheetContent(sheetName)
        columnNum = self.inputData.shape[1]
        if columnNum == 0:
            widget = QWidget()
            reply = QMessageBox.question(widget, "提示", f"{sheetName}的数据为空，请检查", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.Yes)
            outputNum = 0
            varNum = 0
        elif varNum == 0:
            outputNum = 1
            varNum = columnNum - outputNum
        else:
            outputNum = columnNum - varNum
        # 获取变量数并将其显示到UI
        confFileData = ReadandWriteTemplateConf().data_DataInput
        if dataType == "train":
            confFileData.DataFile_TrainyDataSheetName = sheetName
            confFileData.DataFile_TrainyData = self.inputData
            confFileData.DataFile_SampleNum = self.inputData.shape[0]
            confFileData.DataFile_VariableNum = varNum
            #######################
            # todo 需要将变量名与变量的取值范围存储至dict中
            ##########################
            columnNameList = excelFileData.getTableTitleListBySheetName(sheetName)
            confFileData.DataFile_VariableNameList = columnNameList[:varNum] # 变量的名称
            # 变量范围
            varRange = confFileData.DataFile_VariableRange
            varRange.clear()
            index = 0
            for variableName in confFileData.DataFile_VariableNameList:
                dataArray = self.inputData[:, index]
                varRange[variableName] = [min(dataArray), max(dataArray)]
                index += 1
            confFileData.DataFile_OutputNameList = columnNameList[-outputNum:]  # 输出值的名称
            confFileData.DataFile_OutputNum = outputNum
            # 将变量和输出分别存储到数据结构对应的位置
            self.updateTraingSetXYByVariableNumAndOutputNum(VariableNum=confFileData.DataFile_VariableNum,
                                                            OutputNum=confFileData.DataFile_OutputNum)
        elif dataType == "test":
            confFileData.DataFile_TestDataSheetName = sheetName
            confFileData.DataFile_TestData = self.inputData
            confFileData.DataFile_TestSetSampleNum = self.inputData.shape[0]
            confFileData.DataFile_TestSetVariableNum = varNum
            confFileData.DataFile_TestSetOutputNum = outputNum
            self.updateTestSetXYByVariableNumAndOutputNum(VariableNum=confFileData.DataFile_TestSetVariableNum,
                                                          OutputNum=confFileData.DataFile_TestSetOutputNum)

    def addCellToTable(self, dataType):
        """添加单元格到参数表中"""
        confFileData = ReadandWriteTemplateConf().data_DataInput
        if dataType == "train":
            self.showDataParamInTable(dataType, "样本数", confFileData.DataFile_SampleNum)
            self.showDataParamInTable(dataType, "变量数", confFileData.DataFile_VariableNum)
            self.showDataParamInTable(dataType, "输出数", confFileData.DataFile_OutputNum)
        elif dataType == "test":
            self.showDataParamInTable(dataType, "样本数", confFileData.DataFile_TestSetSampleNum)
            self.showDataParamInTable(dataType, "变量数", confFileData.DataFile_TestSetVariableNum)
            self.showDataParamInTable(dataType, "输出数", confFileData.DataFile_TestSetOutputNum)

    # 初始化表格数据
    def initTableData(self):
        confFileData = ReadandWriteTemplateConf().data_DataInput
        if confFileData.isExistTrainingData():
            self.TrainExcelDataReader = ExcelReader(confFileData.DataFile_Path)
            sheetNameList = self.TrainExcelDataReader.getAllSheetsNames()
            self.showDataParamInTable("train", "sheet选择", sheetNameList)
            self.showDataParamInTable("train", "样本数", confFileData.DataFile_SampleNum)
            self.showDataParamInTable("train", "变量数", confFileData.DataFile_VariableNum)
            self.showDataParamInTable("train", "输出数", confFileData.DataFile_OutputNum)
        if confFileData.isExistTestData():
            self.TestExcelDataReader = ExcelReader(confFileData.DataFile_TestPath)
            sheetNameList = self.TestExcelDataReader.getAllSheetsNames()
            self.showDataParamInTable("test", "sheet选择", sheetNameList)
            self.showDataParamInTable("test", "样本数", confFileData.DataFile_TestSetSampleNum)
            self.showDataParamInTable("test", "变量数", confFileData.DataFile_TestSetVariableNum)
            self.showDataParamInTable("test", "输出数", confFileData.DataFile_TestSetOutputNum)

    def showDataParamInTable(self, DataType, variableName, value):
        if DataType == "train":
            items = self.findItems("测试数据集", Qt.MatchExactly)
            if len(items) == 1:
                item = items[0]
                num = item.row()
        else:
            num = self.rowCount()
        self.insertRow(num)
        self.setMyItem(num, 0, variableName, False)
        if isinstance(value, list):
            self.setCellWidget(num, 1, self.setQcomboBoxCellWidget(value, f'cbb_{DataType}_sheetName'))
            cbb = self.findChild(QComboBox, f'cbb_{DataType}_sheetName')
            if cbb is not None:
                confFileData = ReadandWriteTemplateConf().data_DataInput
                if DataType == 'test':
                    sheetName = confFileData.DataFile_TestDataSheetName
                elif DataType == 'train':
                    sheetName = confFileData.DataFile_TrainyDataSheetName
                if sheetName:
                    cbb.setCurrentText(sheetName)
                cbb.activated.connect(self.slotUpdateCurrentDataBySheetName)
        else:
            objName = DataType
            if variableName == '变量数':
                objName = f'{DataType}_variablesNum'
            elif variableName == '输出数':
                objName = f'{DataType}_outputsNum'
            elif variableName == '样本数':
                objName = f'{DataType}_sampleNum'
            self.setCellWidget(num, 1, self.setQLineEditCellWidget(str(value), objName))
            self.findChild(QLineEdit, objName).editingFinished.connect(self.slotVariableNumOrOutputNumchanged)

    # 设置变量数
    def slotVariableNumOrOutputNumchanged(self):
        """
        变量数或者输出数改变的槽函数
        :return:
        """
        confFileData = ReadandWriteTemplateConf().data_DataInput
        allNum = confFileData.DataFile_VariableNum + confFileData.DataFile_OutputNum
        # 更改UI中的显示
        num = int(self.sender().text())
        senderObjName = self.sender().objectName()
        variablesNum = 0
        outputsNum = 0
        if senderObjName == 'train_variablesNum':
            variablesNum = num
            outputsNum = allNum - num
            trainOutputNumEdit = self.findChild(QLineEdit, 'train_outputsNum')
            if isinstance(trainOutputNumEdit, QLineEdit):
                trainOutputNumEdit.setText(str(outputsNum))
            # testVariablesNumEdit = self.findChild(QLineEdit, 'test_variablesNum')
            # if isinstance(testVariablesNumEdit, QLineEdit):
            #     testVariablesNumEdit.setText(str(variablesNum))
            # testOutputNumEdit = self.findChild(QLineEdit, 'test_outputsNum')
            # if isinstance(testOutputNumEdit, QLineEdit):
            #     testOutputNumEdit.setText(str(outputsNum))
            cbb = self.findChild(QComboBox, 'cbb_train_sheetName')
        elif senderObjName == 'train_outputsNum':
            variablesNum = allNum - num
            outputsNum = num
            trainVariablesNumEdit = self.findChild(QLineEdit, 'train_variablesNum')
            if isinstance(trainVariablesNumEdit, QLineEdit):
                trainVariablesNumEdit.setText(str(variablesNum))
            # testVariablesNumEdit = self.findChild(QLineEdit, 'test_variablesNum')
            # if isinstance(testVariablesNumEdit, QLineEdit):
            #     testVariablesNumEdit.setText(str(outputsNum))
            # testOutputNumEdit = self.findChild(QLineEdit, 'test_outputsNum')
            # if isinstance(testOutputNumEdit, QLineEdit):
            #     testOutputNumEdit.setText(str(variablesNum))
            cbb = self.findChild(QComboBox, 'cbb_train_sheetName')
        elif senderObjName == 'test_variablesNum':
            variablesNum = num
            outputsNum = allNum - num
            # trainOutputNumEdit = self.findChild(QLineEdit, 'train_outputsNum')
            # if isinstance(trainOutputNumEdit, QLineEdit):
            #     trainOutputNumEdit.setText(str(outputsNum))
            # trainVariablesNumEdit = self.findChild(QLineEdit, 'train_variablesNum')
            # if isinstance(trainVariablesNumEdit, QLineEdit):
            #     trainVariablesNumEdit.setText(str(variablesNum))
            testOutputNumEdit = self.findChild(QLineEdit, 'test_outputsNum')
            if isinstance(testOutputNumEdit, QLineEdit):
                testOutputNumEdit.setText(str(outputsNum))
            cbb = self.findChild(QComboBox, 'cbb_test_sheetName')
        elif senderObjName == 'test_outputsNum':
            variablesNum = allNum - num
            outputsNum = num
            # trainOutputNumEdit = self.findChild(QLineEdit, 'train_outputsNum')
            # if isinstance(trainOutputNumEdit, QLineEdit):
            #     trainOutputNumEdit.setText(str(outputsNum))
            # trainVariablesNumEdit = self.findChild(QLineEdit, 'train_variablesNum')
            # if isinstance(trainVariablesNumEdit, QLineEdit):
            #     trainVariablesNumEdit.setText(str(variablesNum))
            testVariablesNumEdit = self.findChild(QLineEdit, 'test_variablesNum')
            if isinstance(testVariablesNumEdit, QLineEdit):
                testVariablesNumEdit.setText(str(variablesNum))
            cbb = self.findChild(QComboBox, 'cbb_test_sheetName')

        # 更改数据结构中的数据
        if cbb is not None:
            sheetName = cbb.currentText()
            self.setVariableAndOutputData(dataType=senderObjName.split('_')[0], sheetName=sheetName,
                                          varNum=variablesNum)

    def slotUpdateCurrentDataBySheetName(self):
        """选择不同的sheetName"""
        sheetName = self.sender().currentText()
        dataType = self.sender().objectName().split('_')[1]
        varNum = ReadandWriteTemplateConf().data_DataInput.DataFile_VariableNum
        # 更新数据结构中的数据
        self.setVariableAndOutputData(dataType=dataType, sheetName=sheetName, varNum=varNum)
        # 更新UI中显示的数据
        self.updateCellData(dataType)

    def updateCellData(self, dataType):
        """
        根据dataType,更新单元格中的数据
        :param dataType: 数据类型
        :return:
        """
        confFileData = ReadandWriteTemplateConf().data_DataInput
        if dataType == 'train':
            varNum = str(confFileData.DataFile_VariableNum)
            outputNum = str(confFileData.DataFile_OutputNum)
            sampleNum = str(confFileData.DataFile_SampleNum)
        elif dataType == 'test':
            varNum = str(confFileData.DataFile_TestSetVariableNum)
            outputNum = str(confFileData.DataFile_TestSetOutputNum)
            sampleNum = str(confFileData.DataFile_TestSetSampleNum)
        self.findChild(QLineEdit, f'{dataType}_variablesNum').setText(varNum)
        self.findChild(QLineEdit, f'{dataType}_outputsNum').setText(outputNum)
        self.findChild(QLineEdit, f'{dataType}_sampleNum').setText(sampleNum)


    def updateTraingSetXYByVariableNumAndOutputNum(self, VariableNum, OutputNum):
        confFileData = ReadandWriteTemplateConf().data_DataInput
        confFileData.DataFile_TrainingSet_x = confFileData.DataFile_TrainyData[:, 0:VariableNum]
        confFileData.DataFile_TrainingSet_y = confFileData.DataFile_TrainyData[:, VariableNum:(VariableNum + OutputNum)]

    def updateTestSetXYByVariableNumAndOutputNum(self, VariableNum, OutputNum):
        confFileData = ReadandWriteTemplateConf().data_DataInput
        confFileData.DataFile_TestSet_x = confFileData.DataFile_TestData[:, 0:VariableNum]
        confFileData.DataFile_TestSet_y = confFileData.DataFile_TestData[:, VariableNum:(VariableNum + OutputNum)]






