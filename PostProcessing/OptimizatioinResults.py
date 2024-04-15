from PostProcessing.ui.Ui_OptimizationResults import Ui_OptimizationResults
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFontMetrics
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QHeaderView, QComboBox, QListView
from configFile.ReadTemplateConf import *
import logging

class OptimizationResults(QWidget, Ui_OptimizationResults):
    tableHeight = 0
    def __init__(self):
        super(OptimizationResults, self).__init__()
        self.setupUi(self)
        self.__initUI__()
        self.data = ReadandWriteTemplateConf().data_OptimizationAlgorithm
        self.showOptimizationResults()
        self.createScatter()

    def __initUI__(self):
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def showOptimizationResults(self):
        if self.data.Opt_AlgorithmResult is not None:
            # self.showIterationDiagram()
            self.showBestResult()
            # print('best_x is ', self.data.Opt_AlgorithmResult.gbest_x, 'best_y is', self.data.Opt_AlgorithmResult.gbest_y)

    def showBestResult(self):
        """将最优解显示到表格中"""
        params = self.data.Opt_AlgorithmResult.X
        results = self.data.Opt_AlgorithmResult.F
        constrain = self.data.Opt_AlgorithmResult.G
        try:
            len(results.shape)
            len(params.shape)
            len(constrain.shape)
        except:
            logging.getLogger().error('未计算出优化结果，请检查优化问题设置是否准确，代理模型精度是否达到要求！')
            return
        if len(results.shape) == 1:
            objNum = results.shape[0]
        else:
            objNum = results.shape[1]
        if len(params.shape) == 1:
            paramsNum = params.shape[0]
        else:
            paramsNum = params.shape[1]
        if len(constrain.shape) == 1:
            constrainNum = constrain.shape[0]
        else:
            constrainNum = constrain.shape[1]
        self.tableWidget.setRowCount(results.shape[0] + 1)
        self.tableWidget.setColumnCount(paramsNum + objNum + constrainNum)
        itemHeight = self.tableWidget.itemHeight
        self.tableWidget.setRowHeight(0, itemHeight)
        self.tableHeight = self.tableWidget.rowCount() * itemHeight + 2
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        index = 0
        # 响应值
        for key in self.data.Opt_AlgorithmProblem_target.keys():
            self.tableWidget.setMyItem(0, index, f'优化目标_{key}', False)
            index += 1
        # 约束值
        for key in self.data.Opt_AlgorithmProblem_constrains.keys():
            self.tableWidget.setMyItem(0, index, f'约束条件_{key}', False)
            index += 1
        # 变量值
        for name in self.data.Opt_AlgorithmProblem_variNameList:
            self.tableWidget.setMyItem(0, index, f'变量_{name}', False)
            index += 1
        index_row = 1
        index_column = 0
        for i in range(results.shape[0]):
            if len(results.shape) > 1:
                for j in range(results.shape[1]):
                    if abs(results[i, j]) < 0.0001:
                        valueStr = format(results[i, j], '.5e')
                    else:
                        valueStr = format(results[i, j], '.6f')
                    self.tableWidget.setMyItem(index_row + i, j, valueStr, False)
                    self.tableWidget.setRowHeight(index_row + i, itemHeight)
            else:
                if abs(results[i]) < 0.0001:
                    valueStr = format(results[i], '.5e')
                else:
                    valueStr = format(results[i], '.6f')
                self.tableWidget.setMyItem(index_row, index_column, valueStr, False)
                index_column += 1
                self.tableWidget.setRowHeight(index_row + i, itemHeight)

        for i in range(constrain.shape[0]):
            if len(results.shape) > 1:
                for j in range(constrain.shape[1]):
                    if abs(constrain[i, j]) < 0.0001:
                        valueStr = format(constrain[i, j], '.5e')
                    else:
                        valueStr = format(constrain[i, j], '.6f')
                    self.tableWidget.setMyItem(index_row + i, objNum + j, valueStr, False)
            else:
                if abs(constrain[i]) < 0.0001:
                    valueStr = format(constrain[i], '.5e')
                else:
                    valueStr = format(constrain[i], '.6f')
                self.tableWidget.setMyItem(index_row, index_column, valueStr, False)
                index_column += 1

        for i in range(params.shape[0]):
            if len(results.shape) > 1:
                for j in range(params.shape[1]):
                    if abs(params[i, j]) < 0.0001:
                        valueStr = format(params[i, j], '.5e')
                    else:
                        valueStr = format(params[i, j], '.6f')
                    self.tableWidget.setMyItem(index_row + i, objNum + constrainNum + j, valueStr, False)
            else:
                if abs(params[i]) < 0.0001:
                    valueStr = format(params[i], '.5e')
                else:
                    valueStr = format(params[i], '.6f')
                self.tableWidget.setMyItem(index_row, index_column, valueStr, False)
                index_column += 1


    def createScatter(self):
        self.widget.clearLayoutAllItems()  # 删除现有曲线
        results = self.data.Opt_AlgorithmResult.F
        Text = 'obj1-obj2'
        if len(results) > 1:
            if results.shape[1] > 1:
                xValue = results[:, 0]
                yValue = results[:, 1]
                if abs(xValue[np.argmax(xValue)] - xValue[np.argmin(xValue)]) <= 1e-6:
                    self.widget.hide()
                    return
                self.widget.show()
                self.widget.clearLayoutAllItems()
                self.widget.createChart()
                self.widget.createAxis(xValue, yValue)
                self.widget.addScatterSeries(xValue, yValue, Text, Qt.blue)
            else:
                self.widget.hide()
        else:
            self.widget.hide()

    def resizeEvent(self, e):
        if self.tableHeight > self.tableWidget.parentWidget().height() / 2:
            self.tableWidget.setFixedHeight(self.tableWidget.parentWidget().height() / 2)
        else:
            self.tableWidget.setFixedHeight(self.tableHeight)