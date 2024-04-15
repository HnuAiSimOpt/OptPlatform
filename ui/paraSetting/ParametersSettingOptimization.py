from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QTableWidget, QHBoxLayout, QTableWidgetItem, QLabel, QComboBox, QHeaderView
from PyQt5.QtCore import Qt
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from ui.paraSetting.myTableWidget import myTableWidget
from ui.paraSetting.DefineOptProblem import DefineOptProblem
from PublicTool.myPublicDialogBackground import myPublicDialogBackground
from PublicTool.myMaskWidget import myMaskWidget

class OptimizationAlgorithmParamSetting(myTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.__initUI__()
        self.__initConnect__()

    def __initUI__(self):
        self.setRowCount(2)
        self.setColumnCount(2)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(self.itemHeight)
        self.setMyItem(0, 0, "定义优化问题", False)
        self.setCellWidget(0, 1, self.setButtonCellWidget("Go", "defineOptProblemBtn"))
        self.findChild(QPushButton, "defineOptProblemBtn").clicked.connect(self.slotDefineOptProblemBtnClicked)
        confFile = ReadandWriteTemplateConf()
        nameList = confFile.getOptimizationAlgorithmNameList()
        self.item_chooseAlgorithm = self.setQcomboBoxCellWidget(nameList.split(";"))
        self.setMyItem(1, 0, '优化算法', False)
        self.setCellWidget(1, 1, self.item_chooseAlgorithm)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 表格宽度自适应内容宽度
        # 设置单元格样式
        self.setFocusPolicy(Qt.NoFocus) # 选中单元格时不出现虚线框
        # self.setStyleSheet("background:rgb(30,30,30); border:1px black; font-size:12px; color:white;"
        #                    "selection-background-color:rgb(30,30,30); selection-color:white")
        if confFile.data_OptimizationAlgorithm.isEmpty() == True:
            if self.setChooseModelText(): # 从配置文件获取默认模型
                if self.setDefaultParameters():   # 从配置文件获取默认模型的默认参数
                    self.setUIShowValueByDataStaructValue() # 显示到UI
        else:
            self.setUIShowValueByDataStaructValue()  # 显示到UI

    def __initConnect__(self):
        self.item_chooseAlgorithm.currentIndexChanged.connect(self.getParametersList)

    def createChooseParameterItem(self, strList):
        if len(strList) == 1 and strList[0] == '':
            lineEdit = self.setQLineEditCellWidget('')
            return lineEdit
        else:
            chooseParam = self.setQcomboBoxCellWidget(strList)
            return chooseParam

    def getParametersList(self):
        """从用户配置文件中查找优化算法相应的参数，并显示到界面中"""
        paramlist = self.updateChooseModelValueByUserChoosen()  # 更新数据结构以及用户配置文件
        if self.setDefaultParameters():  # 将配置文件中的默认参数值存储到数据结构中
            self.updateParamTableData(paramlist)  # 根据参数类型创建表格样式
            dict_param = ReadandWriteTemplateConf().data_OptimizationAlgorithm.Opt_AlgorithmParams
            self.setTableParamValue(dict_param)  # 将存储于数据结构中的参数值，显示到上一步创建的参数表中
        else:
            self.clearTable()

    def setOptimizationAlgorithmDataStaructValue(self):
        """设置优化算法数据结构中的相关参数"""
        confFile = ReadandWriteTemplateConf()
        key = self.sender().objectName()
        try:
            value = self.sender().currentText()
        except:
            value = self.sender().text()
        confFile.data_OptimizationAlgorithm.Opt_AlgorithmParams[key] = value

    def setUIShowValueByDataStaructValue(self):
        """将数据结构中设置的参数值，显示在界面中"""
        confFile = ReadandWriteTemplateConf()
        # 根据数据结构中存储的模型名称，显示到对应的单元格内
        self.item_chooseAlgorithm.setCurrentText(confFile.data_OptimizationAlgorithm.Opt_AlgorithmName)
        # 从用户配置文件中获取代理模型参数列表，并根据参数形式，创建对应的单元格
        paramList = confFile.getParametersNameAndValuesList("point/chooseAlgorithm")
        self.updateParamTableData(paramList)
        # 将存储于数据结构中的参数值，显示到上一步创建的参数表中
        dict_param = confFile.data_OptimizationAlgorithm.Opt_AlgorithmParams
        self.setTableParamValue(dict_param)

    """更新参数表中的内容"""
    def updateParamTableData(self, paramList):
        self.clearTable() # 清空表格

        """将参数显示到界面中"""
        if len(paramList) > 0:
            for param in paramList:
                rowCount = self.rowCount()
                self.insertRow(rowCount)  # 增加一行
                self.setMyItem(rowCount, 0, param["name"], False, Qt.AlignCenter)
                item_chooseParam = self.createChooseParameterItem(param["value"].split(";"))
                item_chooseParam.setObjectName(param["name"])
                if isinstance(item_chooseParam, QComboBox):
                    item_chooseParam.currentIndexChanged.connect(self.setOptimizationAlgorithmDataStaructValue)
                elif isinstance(item_chooseParam, QLineEdit):
                    item_chooseParam.textChanged.connect(self.setOptimizationAlgorithmDataStaructValue)
                self.setCellWidget(rowCount, 1, item_chooseParam)

    def clearTable(self):
        """删除现有内容"""
        rowCount = self.rowCount() - 1
        while rowCount >= 2:
            self.removeCellWidget(rowCount, 1)
            self.removeRow(rowCount)
            rowCount -= 1

    def setDefaultParameters(self):
        """从配置文件读取算法参数默认值，并存储到数据结构"""
        confFile = ReadandWriteTemplateConf()
        paramValue = confFile.getOptimizationAlgorithmDefaultValue()
        if paramValue:
            confFile.data_OptimizationAlgorithm.Opt_AlgorithmParams = paramValue #将获取到的默认值添加到数据结构中
            return True
        return False

    def setChooseModelText(self):
        """从配置文件获取默认算法， 并设置qcombobox的当前显示， 并存储到数据结构中"""
        confFile = ReadandWriteTemplateConf()
        defaultAlgorithm = confFile.getAttribValueByKeyInPath("point/chooseAlgorithm", "defaultValue")
        if defaultAlgorithm is not None:
            confFile.addChildPointsByName("optimizationAlgorithm", defaultAlgorithm)
            self.item_chooseAlgorithm.setCurrentText(defaultAlgorithm)
            confFile.data_OptimizationAlgorithm.Opt_AlgorithmName = defaultAlgorithm
            return True
        else:
            return False

    def setTableParamValue(self, dict_param):
        """将指定的参数，显示到表格中"""
        if dict_param:
            rowCount = self.rowCount() -1
            while rowCount >= 2:
                paramName = self.item(rowCount, 0).text()
                if dict_param.keys().__contains__(paramName):
                    paramValue = dict_param[paramName]
                else:
                    paramName = None
                if paramValue is not None:
                    textControl = self.cellWidget(rowCount, 1)
                    try:
                        textControl.setCurrentText(paramValue)
                    except:
                        textControl.setText(paramValue)
                rowCount -= 1

    def updateChooseModelValueByUserChoosen(self):
        """当用户更换代理模型时，更换用户配置文件中的相关参数配置，并将其记录到数据结构中"""
        """返回参数列表"""
        confFile = ReadandWriteTemplateConf()
        if confFile.isCreatedTemplate():
            algorithmName = self.item_chooseAlgorithm.currentText()
            confFile.addChildPointsByName("optimizationAlgorithm", algorithmName)
            paramList = confFile.getParametersNameAndValuesList("point/chooseAlgorithm")
            ReadandWriteTemplateConf().data_OptimizationAlgorithm.Opt_AlgorithmName = algorithmName  # 更新数据结构中相应的参数值
            return paramList
        else:
            return None

    def slotDefineOptProblemBtnClicked(self):
        """定义优化问题按钮的槽函数"""
        self.widget = DefineOptProblem()
        self.mask = myMaskWidget(self.parent().parent().parent())
        backgroundWidget = myPublicDialogBackground()
        backgroundWidget.setTitle('定义优化问题')
        backgroundWidget.setWidget(self.widget)
        self.mask.layout().addWidget(backgroundWidget)
        self.mask.show()