from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QTableWidget, QComboBox, QHBoxLayout, QTableWidgetItem, QFileDialog, QFrame, QListView, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
import logging
from PyQt5.QtGui import QIcon, QPixmap
from configFile.ReadTemplateConf import *
from ReadingData.ExcelFileReading import *
from AnalyzeProcessTemplates.public import *

class myTableWidget(QTableWidget):
    itemHeight = 30
    def __init__(self, parent):
        super(myTableWidget, self).__init__(parent)
        self.__initMyUI__()

    def __initMyUI__(self):
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setFocusPolicy(Qt.NoFocus)  # 选中单元格时不出现虚线框
        self.horizontalHeader().setStretchLastSection(True)
        # self.setStyleSheet('QTableWidget{background:rgb(57,57,57); gridline-color: rgb(30,30,30);border:1px solid rgb(30,30,30); font-size:12px; color:white;selection-background-color:rgb(57,57,57); selection-color:white}')
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def setMyItem(self, row, col, strValue, isEditable = True, aligen=(Qt.AlignLeft|Qt.AlignVCenter)):
        """
        设置单元格
        :param row: 行
        :param col: 列
        :param strValue: 单元格内容
        :param isEditable: 是否可编辑 True:可编辑
        :return:
        """
        Item = QTableWidgetItem(strValue)
        Item.setTextAlignment(aligen)
        if not isEditable:
            Item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable |
                            Qt.ItemIsSelectable | Qt.ItemIsDragEnabled |
                            Qt.ItemIsDropEnabled)
        self.setItem(row, col, Item)

    def setButtonCellWidget(self, strValue, objName = 'button'):
        """
        将button插入item
        :param strValue:
        :param objName:
        :return:
        """
        btn = QPushButton(strValue)
        btn.setObjectName(objName)
        string = getBtnStyleString()
        btn.setStyleSheet(string)
        return btn

    def setQLineEditCellWidget(self, strValue, objName = "lineEdit"):
        """
        将qlineedit插入item
        :param strValue:
        :return:
        """
        lineEdit = QLineEdit(str(strValue))
        lineEdit.setObjectName(objName)
        lineEdit.setStyleSheet(getLineEditStyleSheet())
        return lineEdit

    def setQcomboBoxCellWidget(self, stringList, objName = "comboBox"):
        """
        将单元格设置成qcombobox
        :param stringList: 下拉菜单列表
        :return:
        """
        chooseParam = QComboBox()
        chooseParam.addItems(stringList)
        chooseParam.setObjectName(objName)
        chooseParam.setStyleSheet(getQcomboBoxStyleSheet())
        return chooseParam

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

    def getRowIndexBySpecialString(self, string):
        """
        查找string在单元格中的位置，如果表格中没有string单元格，则返回最后一行
        :param string: 指定特征
        :return: 所在位置的行数/表格的总行数
        """
        items = self.findItems(string, Qt.MatchExactly)
        if len(items) == 1:
            return items[0].row()
        elif len(items) > 1:
            logging.getLogger().error("表格内容出现错误，请更改")
            return 0
        return self.rowCount()

    def createValueRangeItem(self, range, row):
        """
        创建取值范围item
        :param range: 取值范围
        :param row: 当前item所在的行
        :return: item对象
        """
        if isinstance(range, list):
            if len(range) == 2:
                widgetDesignRange = QWidget()
                HboxLayout = QHBoxLayout()
                spacerItem_1 = QSpacerItem(0, 0, QSizePolicy.Expanding)
                HboxLayout.addItem(spacerItem_1)
                label_lowValue = QLineEdit(str(range[0]), widgetDesignRange)
                label_lowValue.setFixedHeight(self.itemHeight)
                label_lowValue.setObjectName(f"low_{row}")
                label_lowValue.setAlignment(Qt.AlignCenter)
                label_lowValue.setMinimumWidth(88)
                HboxLayout.addWidget(label_lowValue)
                line = QFrame(widgetDesignRange)
                line.setMinimumWidth(6)
                line.setFrameShape(QFrame.HLine)
                line.setStyleSheet(getQFrameStyleSheet())
                HboxLayout.addWidget(line)
                label_upValue = QLineEdit(str(range[1]), widgetDesignRange)
                label_upValue.setFixedHeight(self.itemHeight)
                label_upValue.setObjectName(f"up_{row}")
                label_upValue.setAlignment(Qt.AlignCenter)
                label_upValue.setMinimumWidth(88)
                HboxLayout.addWidget(label_upValue)
                spacerItem_2 = QSpacerItem(0, 0, QSizePolicy.Expanding)
                HboxLayout.addItem(spacerItem_2)
                HboxLayout.setContentsMargins(0, 0, 0, 0)
                HboxLayout.setSpacing(4)
                HboxLayout.setStretch(0, 1)
                HboxLayout.setStretch(1, 6)
                HboxLayout.setStretch(2, 2)
                HboxLayout.setStretch(3, 6)
                HboxLayout.setStretch(4, 1)
                widgetDesignRange.setLayout(HboxLayout)
                widgetDesignRange.setStyleSheet(getWidgetStyleSheet())
                label_lowValue.setStyleSheet(getLineEditStyleSheet())
                label_upValue.setStyleSheet(getLineEditStyleSheet())
                return widgetDesignRange
        return None

    def createOpenFileCellWidget(self, LineEditObjName = 'Edit_', BtnObjName= 'Btn_', LineEditText = ''):
        """
        打开文件控件 qlineedit + btn
        :return:
        """
        icon_OpenFile = QIcon()
        icon_OpenFile.addPixmap(QPixmap(":/pic/icons/打开文件.png"), QIcon.Normal, QIcon.Off)
        HboxLayout = QHBoxLayout()
        Edit_OpenFile = QLineEdit(LineEditText)
        Edit_OpenFile.setFixedHeight(self.itemHeight)
        Edit_OpenFile.setStyleSheet(getLineEditStyleSheet())
        Edit_OpenFile.setObjectName(LineEditObjName)
        HboxLayout.addWidget(Edit_OpenFile)
        button_OpenFile = QPushButton()
        button_OpenFile.setFixedSize(self.itemHeight, self.itemHeight)
        # button_OpenFile.setStyleSheet(getBtnStyleString())
        button_OpenFile.setIcon(icon_OpenFile)
        button_OpenFile.setObjectName(BtnObjName)
        HboxLayout.addWidget(button_OpenFile)
        HboxLayout.setContentsMargins(0, 0, 0, 0)
        HboxLayout.setSpacing(0)
        widgetOpenFile = QWidget()
        widgetOpenFile.setLayout(HboxLayout)
        widgetOpenFile.setStyleSheet(getWidgetStyleSheet())
        return widgetOpenFile, Edit_OpenFile, button_OpenFile

    def showEvent(self, e) -> None:
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def changeSize(self, width, height):
        self.setFixedWidth(width)
        self.setFixedHeight(height)

    def changeColumnWidth(self, columnIndex, width):
        self.setColumnWidth(columnIndex, width)

    def resize(self, width, height) -> None:
        self.setFixedWidth(width)
        self.setFixedHeight(height)
