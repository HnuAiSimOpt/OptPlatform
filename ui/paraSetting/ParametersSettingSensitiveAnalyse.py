from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QTableWidget, QHBoxLayout, QTableWidgetItem, QLabel, QComboBox, QHeaderView, QFrame, QListView
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from AnalyzeProcessTemplates.public import TemplateNameEnum
from ui.paraSetting.myTableWidget import myTableWidget

class SensitiveAnalyseParamSetting(myTableWidget):
    def __init__(self, parent):
        super(SensitiveAnalyseParamSetting, self).__init__(parent)
        self.initUI()
        self.initConnect()

    def initUI(self):
        self.setRowCount(1)
        self.setColumnCount(2)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(self.itemHeight)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 表格宽度自适应内容宽度
        self.createSAParametersItem()

    def initConnect(self):
        self.chooseSAWaysCBB.activated.connect(self.slotCBBChooseSAWaysActivited)

    def createSAParametersItem(self):
        # 敏感性分析方法选择
        self.setMyItem(0, 0, '敏感性分析方法')
        confFile = ReadandWriteTemplateConf()
        strSAWaysName = confFile.getSensitiveAnalyseNameList()
        self.chooseSAWaysCBB = self.setQcomboBoxCellWidget(strSAWaysName.split(";"))
        self.setCellWidget(0, 1, self.chooseSAWaysCBB)
        if confFile.data_SensitiveAnalyse.SA_Name: # 将默认值显示到UI
            self.chooseSAWaysCBB.setCurrentText(confFile.data_SensitiveAnalyse.SA_Name)
        else:
            #将第一顺位的方法设置为默认方法
            confFile.data_SensitiveAnalyse.SA_Name = self.chooseSAWaysCBB.itemText(0)

    def slotCBBChooseSAWaysActivited(self):
        """
        选择敏感性分析算法的槽函数
        :return:
        """
        curWays = self.sender().currentText()
        ReadandWriteTemplateConf().data_SensitiveAnalyse.SA_Name = curWays