from PostProcessing.ui.Ui_SensitiveAnalyseResults import Ui_Form
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidgetItem
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
import numpy as np

class SensitiveAnalyseResults(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(SensitiveAnalyseResults, self).__init__(parent)
        self.setupUi(self)
        self.initData()
        self.initUI()
        self.initConnect()

    def initData(self):
        """
        初始化数据，获取敏感性分析结果
        :return:
        """
        SAResults = ReadandWriteTemplateConf().data_SensitiveAnalyse
        self.results = SAResults.SA_Result
        self.curName = SAResults.SA_Name

    def initUI(self):
        self.lineEdit_pieShowNum.setValidator(QIntValidator(self.lineEdit_pieShowNum))
        self.outputList = list(self.results.get('outputNameList'))
        self.cbb_chooseOutput.addItems(self.outputList)
        self.lineEdit_SAWays.setText(self.curName)
        self.lineEdit_SAWays.setEnabled(False)
        variableNameList = list(self.results.get('variableNameList'))
        variNum = len(variableNameList)

        # 设置默认饼状图中显示的指标数量
        self.pieShowNum = int(variNum * 0.6)
        self.lineEdit_pieShowNum.setText(str(self.pieShowNum))

        # 隐藏表格自带表头
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        # 设置表格的行数和列数
        self.tableWidget.setColumnCount(variNum + 1)
        if self.curName == 'Morris':
            self.tableWidget.setRowCount(2)
        else:
            self.tableWidget.setRowCount(variNum + 1)
        # 设置表头
        for index in range(1, variNum + 1):
            self.tableWidget.setItem(0, index, QTableWidgetItem(variableNameList[index - 1]))
        if self.curName != 'Morris':
            for index in range(1, variNum + 1):
                self.tableWidget.setItem(index, 0, QTableWidgetItem(variableNameList[index - 1]))
        # 添加数据
        self.curOutputIndex = self.outputList.index(self.cbb_chooseOutput.currentText())
        self.curSAData = self.results.get('SASortBox')[self.curOutputIndex]
        if isinstance(self.curSAData, list):
            dataShape = np.array(self.curSAData).shape
            if len(dataShape) == 3 and dataShape[0] == 1:
                self.curSAData = np.array(self.curSAData[0]).T
        self.addDataToTable(self.curSAData)
        # 图初始化
        self.updatePieData()
        showNum = self.widget_pieChart.createPieChart(self.pieData, variableNameList, self.pieShowNum)
        if showNum != self.pieShowNum:
            self.lineEdit_pieShowNum.setText(showNum)
            self.pieShowNum = showNum

    def initConnect(self):
        self.cbb_chooseOutput.activated.connect(self.slotCBBChooseOutputActivated)
        self.lineEdit_pieShowNum.editingFinished.connect(self.slotLineEditPieShowNumChanged)

    def addDataToTable(self, data):
        """
        向表格中添加敏感性指标数据
        :param data:
        :return:
        """
        nRow, nCol = data.shape
        if nCol == 3:
            for index in range(nRow):
                curVari_X = int(data[index, 1])
                curVari_Y = int(data[index, 2])
                item_0 = QTableWidgetItem(format(data[index, 0], '.5f'))
                self.tableWidget.setItem(curVari_X, curVari_Y, item_0)
                if curVari_X != curVari_Y:
                    item_1 = QTableWidgetItem(format(data[index, 0], '.5f'))
                    self.tableWidget.setItem(curVari_Y, curVari_X, item_1)
        elif nCol == 2:
            for index in range(nRow):
                curVari_X = data[index, 0]
                if isinstance(curVari_X, str):
                    curVari_X = int(curVari_X.split('V')[1])
                else:
                    curVari_X = int(curVari_X)
                curValue = data[index, 1]
                if isinstance(curValue, str):
                    curValue = float(curValue)
                item = QTableWidgetItem(format(curValue, '.5f'))
                self.tableWidget.setItem(1, curVari_X, item)

    def slotCBBChooseOutputActivated(self):
        curOutputIndex = self.outputList.index(self.cbb_chooseOutput.currentText())
        if curOutputIndex == self.curOutputIndex:
            return
        else:
            self.curOutputIndex = curOutputIndex
        self.curSAData = self.results.get('SASortBox')[self.curOutputIndex]
        if isinstance(self.curSAData, list):
            dataShape = np.array(self.curSAData).shape
            if len(dataShape) == 3 and dataShape[0] == 1:
                self.curSAData = np.array(self.curSAData[0]).T
        self.clearTableWidgetData()
        self.addDataToTable(self.curSAData)
        self.updatePieData()
        self.slotLineEditPieShowNumChanged(isForceRefresh=True)

    def clearTableWidgetData(self):
        nRow = self.tableWidget.rowCount()
        nCol = self.tableWidget.columnCount()
        for rowIndex in range(1, nRow):
            for colIndex in range(1, nCol):
                self.tableWidget.removeCellWidget(rowIndex, colIndex)

    def updatePieData(self):
        if self.curName == 'Morris':
            orderList = self.curSAData[:, 0]
            valueList = self.curSAData[:, 1]
            self.pieData = np.zeros([len(orderList), 2])
            for index in range(len(orderList)):
                self.pieData[index, 0] = float(valueList[index])
                self.pieData[index, 1] = int(orderList[index].split('V')[1])
        else:
            self.pieData = self.curSAData

    def slotLineEditPieShowNumChanged(self, isForceRefresh=False):
        pieShowNum = int(self.lineEdit_pieShowNum.text())
        if pieShowNum > self.pieData.shape[0]:
            pieShowNum = self.pieData.shape[0]
        if self.pieShowNum != pieShowNum or isForceRefresh:
            self.pieShowNum = pieShowNum
            self.widget_pieChart.chart.removeAllSeries()
            showNum = self.widget_pieChart.createPieChart(self.pieData, self.results.get('variableNameList'), self.pieShowNum)
            self.lineEdit_pieShowNum.setText(str(showNum))
            self.pieShowNum = showNum
        else:
            self.lineEdit_pieShowNum.setText(str(pieShowNum))