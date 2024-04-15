from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QTableWidget, QHBoxLayout, QTableWidgetItem, QLabel, QComboBox, QHeaderView
from PyQt5.QtCore import Qt
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from ui.paraSetting.myTableWidget import myTableWidget
from AnalyzeProcessTemplates.public import SurrogateModelParamSettingWayEnum, ValidationWayEnum
import logging
from AnalyzeProcessTemplates.public import *

class SurrogateModelParamSetting(myTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.__initConnect__()

    def initUI(self):
        self.setRowCount(1)
        self.setColumnCount(2)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(self.itemHeight)
        # item_ModelExtend = self.createDetailParametersItem()
        confFile = ReadandWriteTemplateConf()
        strSurrogateModelName = confFile.getSurrogateModelNameList()
        self.chooseModel = self.setQcomboBoxCellWidget(strSurrogateModelName.split(";"))
        self.setMyItem(0, 0, "代理模型", False)
        self.setCellWidget(0, 1, self.chooseModel)

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 表格宽度自适应内容宽度

        # 设置单元格样式
        self.setFocusPolicy(Qt.NoFocus) # 选中单元格时不出现虚线框
        # self.setStyleSheet("background:rgb(30,30,30); border:1px black; font-size:12px; color:white;"
        #                    "selection-background-color:rgb(30,30,30); selection-color:white")

        if confFile.data_SurrogateModel.isEmpty() == True:
            if self.setChooseModelText(): # 从配置文件获取默认模型
                if self.setParamSettingWays(): # 如果是自定义参数
                    if self.setDefaultParameters():   # 从配置文件获取默认模型的默认参数
                        self.setUIShowValueByDataStaructValue() # 显示到UI
                else:
                    self.setValidationWays()
        else:
            self.setUIShowValueByDataStaructValue()  # 显示到UI

    def __initConnect__(self):
        self.chooseModel.currentIndexChanged.connect(self.getParametersList)

    def setParamSettingWays(self):
        """
        从配置文件获取默认的参数设置方法，并保存到数据结构中以及用户模板文件中
        :return: 如果是“自定义参数”，返回True，其他返回False
        """
        smData = ReadandWriteTemplateConf().data_SurrogateModel
        name = "参数设置"
        defaultValue = SurrogateModelParamSettingWayEnum.GridSearch.value
        # 检查是否已经创建了该单元格
        if not self.checkVariableNameHasExistedInTable(name):
            valueList = [e.value for e in SurrogateModelParamSettingWayEnum]
            self.insertRow(1)
            self.setMyItem(1, 0, name, False)
            combobox = self.setQcomboBoxCellWidget(valueList, "paramSettingWay")
            self.setCellWidget(1, 1, combobox)
            combobox.activated.connect(self.slotParamSettingWaysChoosen)
        # 若用户从未设置默认值，则将GridSearch作为默认值赋给数据结构，否则采用用户自行设置的值作为默认值
        if smData.SM_ModelParamSettingWays == None:
            smData.SM_ModelParamSettingWays = defaultValue
        else:
            defaultValue = smData.SM_ModelParamSettingWays
        cbb = self.findChild(QComboBox, "paramSettingWay")
        cbb.setCurrentText(defaultValue)
        # 根据默认值，返回True/False
        if defaultValue == SurrogateModelParamSettingWayEnum.Customization.value:
            return True # 自定义参数，返回True
        else:
            return False

    def setValidationWays(self):
        """
        设置验证方法
        :return:
        """
        smData = ReadandWriteTemplateConf().data_SurrogateModel
        name = "验证方法"
        defaultValue = ValidationWayEnum.CrossValidation.value
        if not self.checkVariableNameHasExistedInTable(name):
            valuList = [e.value for e in ValidationWayEnum]
            self.insertRow(self.rowCount())
            self.setMyItem(self.rowCount() - 1, 0, name, False)
            combobox = self.setQcomboBoxCellWidget(valuList, "validationWay")
            self.setCellWidget(self.rowCount() - 1, 1, combobox)
            combobox.currentTextChanged.connect(self.slotValidationWaysChoosen)
            self.slotValidationWaysChoosen(combobox.currentText())
        if smData.SM_ValidationWays == None:
            smData.SM_ValidationWays = defaultValue
        else:
            defaultValue = smData.SM_ValidationWays
        cbb = self.findChild(QComboBox, "validationWay")
        cbb.setCurrentText(defaultValue)

    def slotValidationWaysChoosen(self, currentValue):
        """
        选择验证方法的槽函数
        :return:
        """
        smData = ReadandWriteTemplateConf().data_SurrogateModel
        smData.SM_ValidationWays = currentValue
        self.clearTableValidationParameters() #删除UI中，目前验证方法的参数
        if currentValue == ValidationWayEnum.CrossValidation.value:
            self.insertRow(self.rowCount())
            name = "K-折"
            value = smData.SM_ValidationParams.get("k-fold")
            if value is None:
                value = 10
                smData.SM_ValidationParams["k-fold"] = value
            self.setMyItem(self.rowCount() - 1, 0, name, False, aligen=Qt.AlignCenter)
            self.setCellWidget(self.rowCount() - 1, 1, self.setQLineEditCellWidget(str(value), "kfold"))
            self.findChild(QLineEdit, "kfold").textChanged.connect(self.slotKfoldChanged)
            smData.SM_ValidationWays = currentValue
        elif currentValue == ValidationWayEnum.TestSetValidation.value:
            name = "测试集"
            value = ReadandWriteTemplateConf().data_DataInput.DataFile_TestPath
            if value != "":
                self.insertRow(self.rowCount())
                self.setMyItem(self.rowCount() - 1, 0, name, False)
                self.setCellWidget(self.rowCount() - 1, 1, self.setQLineEditCellWidget(str(value)))
                smData.SM_ValidationWays = currentValue
            else:
                logging.getLogger().info("未检测到测试集数据，设置失败，请先导入测试集数据")
                self.sender().setCurrentText(ValidationWayEnum.CrossValidation.value)

    def slotKfoldChanged(self, num):
        if is_number(num):
            params = ReadandWriteTemplateConf().data_SurrogateModel.SM_ValidationParams
            params["k-fold"] = int(num)

    def slotParamSettingWaysChoosen(self):
        ReadandWriteTemplateConf().data_SurrogateModel.SM_ModelParamSettingWays =\
            self.sender().currentText()
        if self.setParamSettingWays():  # 如果是自定义参数
            if self.setDefaultParameters():  # 从配置文件获取默认模型的默认参数
                self.setUIShowValueByDataStaructValue()  # 显示到UI
        else:
            self.setUIShowValueByDataStaructValue()

    def createDetailParametersItem(self):
        """参数展开：按钮+qLabel"""
        button = QPushButton(">")
        #button.setStyleSheet("background-color:rgb(57, 57, 57);")
        button.setFixedSize(self.itemHeight, self.itemHeight)
        label = QLabel("代理模型")
        #label.setStyleSheet("background-color:rgb(57, 57, 57);")
        Layout = QHBoxLayout()
        Layout.addWidget(button)
        Layout.addWidget(label)
        Layout.setContentsMargins(0, 0, 0, 0)
        Layout.setSpacing(0)
        widgetModel = QWidget()
        widgetModel.setLayout(Layout)
        return widgetModel

    def createChooseParameterItem(self, strList):
        if len(strList) == 1 and strList[0] == '':
            curWidget = self.setQLineEditCellWidget('')
            return curWidget
        else:
            curWidget = self.setQcomboBoxCellWidget(strList)
            return curWidget

    def getParametersList(self):
        """从用户配置文件中查找代理模型相应的参数，并显示到界面中, 此函数为代理模型选择改变时的槽函数"""
        paramlist = self.updateChooseModelValueByUserChoosen() #更新数据结构以及用户配置文件
        if self.setDefaultParameters(): #将配置文件中的默认参数值存储到数据结构中
            self.updateParamTableData(paramlist) # 根据参数类型创建表格样式
            dict_param = ReadandWriteTemplateConf().data_SurrogateModel.SM_Params
            self.setTableParamValue(dict_param) # 将存储于数据结构中的参数值，显示到上一步创建的参数表中
        else:
            self.clearTableModelingParameters() #无参数，清空表格

    def setSurrogateModelDataStaructValue(self):
        """设置代理模型数据结构中的相关参数"""
        confFile = ReadandWriteTemplateConf()
        key = self.sender().objectName()
        try:
            value = self.sender().currentText()
        except:
            value = self.sender().text()
        confFile.data_SurrogateModel.SM_Params[key] = value

    def setUIShowValueByDataStaructValue(self):
        """将数据结构中设置的参数值，显示在界面中"""
        confFile = ReadandWriteTemplateConf()

        # 根据数据结构中存储的值模型名称，显示到对应的单元格内
        self.chooseModel.setCurrentText(confFile.data_SurrogateModel.SM_ModelName)

        # 如果是用户自定义参数，从用户配置文件中获取代理模型参数列表，并根据参数形式，创建对应的单元格
        if self.setParamSettingWays():
            paramList = confFile.getParametersNameAndValuesList("point/chooseModel")
            self.updateParamTableData(paramList)
            # 将存储于数据结构中的参数值，显示到上一步创建的参数表中
            dict_param = confFile.data_SurrogateModel.SM_Params
            self.setTableParamValue(dict_param)
        else:
            self.clearTableModelingParameters()

        # 设置模型的验证方法
        self.setValidationWays()

    def updateParamTableData(self, paramList):
        """根据参数内容创建表格（表格的行数、表格内控件样式）"""
        self.clearTableModelingParameters() #清空表格

        # 创建新的表格
        if len(paramList) > 0:
            rowCount = self.getRowIndexBySpecialString("参数设置") + 1
            for param in paramList:
                self.insertRow(rowCount)  # 增加一行
                self.setMyItem(rowCount, 0, param["name"], False, Qt.AlignCenter)
                item_chooseParam = self.createChooseParameterItem(param["value"].split(";"))
                item_chooseParam.setObjectName(param["name"])
                if isinstance(item_chooseParam, QComboBox):
                    item_chooseParam.currentIndexChanged.connect(self.setSurrogateModelDataStaructValue)
                elif isinstance(item_chooseParam, QLineEdit):
                    item_chooseParam.textChanged.connect(self.setSurrogateModelDataStaructValue)
                self.setCellWidget(rowCount, 1, item_chooseParam)
                rowCount += 1

    def clearTableModelingParameters(self):
        """删除现有建模参数的表格"""
        lowRow = self.getRowIndexBySpecialString("参数设置")
        upRow = self.getRowIndexBySpecialString("验证方法")
        currentRow = upRow - 1
        self.deleteCellWidget(lowRow, currentRow)

    def clearTableValidationParameters(self):
        """删除现有验证方法的参数表格"""
        lowRow = self.getRowIndexBySpecialString("验证方法")
        upRow = self.rowCount()
        currentRow = upRow - 1
        self.deleteCellWidget(lowRow, currentRow)

    def deleteCellWidget(self, lowRow, upRow):
        while upRow > lowRow:
            self.removeCellWidget(upRow, 1)
            self.removeRow(upRow)
            upRow -= 1

    def setDefaultParameters(self):
        """从配置文件读取算法参数默认值，并存储到数据结构"""
        confFile = ReadandWriteTemplateConf()
        paramValue = confFile.getSurrogateModelDefaultValue()
        if paramValue:
            confFile.data_SurrogateModel.SM_Params = paramValue #将获取到的默认值添加到数据结构中
            return True
        return False

    def setChooseModelText(self):
        """从配置文件获取默认算法， 并设置qcombobox的当前显示， 并存储到数据结构中"""
        confFile = ReadandWriteTemplateConf()
        defaultModel = confFile.getAttribValueByKeyInPath("point/chooseModel", "defaultValue")
        if defaultModel is not None:
            confFile.addChildPointsByName("surrogateModel", defaultModel)
            self.chooseModel.setCurrentText(defaultModel)
            confFile.data_SurrogateModel.SM_ModelName = defaultModel
            return True
        else:
            return False

    def setTableParamValue(self, dict_param):
        """将指定的参数，显示到表格中"""
        if dict_param:
            rowCount = self.rowCount() -1
            while rowCount >= 1:
                paramName = self.item(rowCount, 0).text()
                if dict_param.keys().__contains__(paramName):
                    paramValue = dict_param[paramName]
                else:
                    paramValue = None
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
            model = self.chooseModel.currentText()
            confFile.addChildPointsByName("surrogateModel", model)
            paramList = confFile.getParametersNameAndValuesList("point/chooseModel")
            ReadandWriteTemplateConf().data_SurrogateModel.SM_ModelName = model  # 更新数据结构中相应的参数值
            return paramList
        else:
            return None