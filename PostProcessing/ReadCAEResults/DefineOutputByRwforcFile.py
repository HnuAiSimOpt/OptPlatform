from PostProcessing.ReadCAEResults.ui.Ui_DefineOutputByRwforcFile import Ui_rwforcFileReader
from PostProcessing.ReadCAEResults.ReadRwforcFile import ReadRwforcFile
from AnalyzeProcessTemplates.public import OutputFunc, SolverFileTyeEnum, getBtnStyleString
import numpy as np
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QCategoryAxis, QScatterSeries
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QLabel, QMessageBox, QListView, QComboBox
from PyQt5.QtGui import QPainter, QPen, QCursor, QFontMetrics, QColor
import math
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from PublicTool.myMaskWidget import myMaskWidget

class DefineOutputByRwforcFile(QWidget, Ui_rwforcFileReader):
    msg = pyqtSignal(str)
    def __init__(self, filePath):
        super(DefineOutputByRwforcFile, self).__init__()
        self.setupUi(self)
        self.filePath = filePath
        self.__initUI__()
        self.__initConnect__()
        self.valueLabel = QLabel(self)
        self.valueLabel.setStyleSheet("background-color: rgb(52, 134, 57);color: rgb(245, 245, 245);font: 12pt 'Times New Roman';")
        self.valueLabel.setAlignment(Qt.AlignCenter)
        self.valueLabel.hide()

    def __initUI__(self):
        ReadRwforcFile().praserFile(self.filePath)
        self.cbb_direction.addItems(ReadRwforcFile().get_directions())
        self.cbb_rigidID.addItems(ReadRwforcFile().get_rigid_ids())
        self.cbb_func.clear()
        self.cbb_func.addItem(OutputFunc.Max.value)
        self.cbb_func.addItem(OutputFunc.Min.value)
        self.cbb_func.addItem(OutputFunc.Mean.value)
        self.cbb_func.addItem(OutputFunc.Sum.value)
        self.cbb_func.addItem(OutputFunc.First.value)
        self.cbb_func.addItem(OutputFunc.Last.value)
        self.cbb_func.addItem(OutputFunc.NO.value)
        self.lineEdit_name.setText('output_force')
        self.Btn_cancel.setStyleSheet(getBtnStyleString())
        self.Btn_yes.setStyleSheet(getBtnStyleString())
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def __initConnect__(self):
        self.cbb_func.activated.connect(self.showDataToChart)
        self.cbb_rigidID.activated.connect(self.showDataToChart)
        self.cbb_direction.activated.connect(self.showDataToChart)
        self.Btn_yes.clicked.connect(self.slotBtnYesClicked)
        self.Btn_cancel.clicked.connect(self.slotBtnCancelClicked)

    def showDataToChart(self):
        self.func = self.cbb_func.currentText()
        self.rigidID = self.cbb_rigidID.currentText()
        self.direction = self.cbb_direction.currentText()
        self.times = ReadRwforcFile().get_time_step()
        currentData = ReadRwforcFile().get_rw_force(self.rigidID, self.direction)
        finalResult = ReadRwforcFile().getTargetValueByOutputFunc(currentData, self.func)
        self.showChart(self.times, currentData)
        self.getFinalOutputValueByFunc(self.func, finalResult)

    def addLineToChart(self, x_value, y_value, type, color):
        self.widget_chart.deleteSeriesByObjName(f'line_{type}')
        self.widget_chart.deleteSeriesByObjName(f'scatter_{type}')
        self.widget_chart.addLineSeries(x_value, y_value, type, color)
        self.widget_chart.addScatterSeries(x_value, y_value, type, color)

    def showChart(self, x_values, y_values):
        self.widget_chart.clearLayoutAllItems()
        self.widget_chart.createChart()
        self.widget_chart.createAxis(x_values, y_values)
        self.addLineToChart(x_values, y_values, 'force', Qt.blue)

        # self.clearLayoutAllItems()
        # chart = QChart()
        # chart.setTitle("")
        # chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.legend().hide()
        #
        # lineSeries = QLineSeries()
        # scatterSeries = QScatterSeries()
        # markLineSeries = QLineSeries()
        # markScatterSeries = QScatterSeries()
        # # x_values = range(len(self.currentData))
        # # y_values = self.currentData
        # self.formatSeries(lineSeries, scatterSeries, markScatterSeries, markLineSeries, x_values, y_values)
        #
        # chartAxisY = QCategoryAxis()
        # y_maxValue = y_values[np.argmax(y_values)]
        # y_minValue = y_values[np.argmin(y_values)]
        # span_y = y_maxValue - y_minValue
        # interval_y = span_y * 1.1 / (self.widget_chart.height() / 80)
        # self.formatAxis(chartAxisY, y_minValue - span_y * 0.05, y_maxValue + span_y * 0.05, interval_y)
        # chartAxisX = QCategoryAxis()
        # x_maxValue = x_values[np.argmax(x_values)]
        # x_minValue = x_values[np.argmin(x_values)]
        # interval_x = (x_maxValue - x_minValue) / (self.widget_chart.width() / 80)
        # if interval_x > 1:
        #     interval_x = int(interval_x)
        # self.formatAxis(chartAxisX, x_minValue, x_maxValue, interval_x, False)
        #
        # chart.addSeries(lineSeries)
        # chart.addSeries(scatterSeries)
        # chart.addSeries(markScatterSeries)
        # chart.addSeries(markLineSeries)
        # chart.addAxis(chartAxisX, Qt.AlignBottom)
        # chart.addAxis(chartAxisY, Qt.AlignLeft)
        # lineSeries.attachAxis(chartAxisX)
        # lineSeries.attachAxis(chartAxisY)
        # scatterSeries.attachAxis(chartAxisX)
        # scatterSeries.attachAxis(chartAxisY)
        # markLineSeries.attachAxis(chartAxisX)
        # markLineSeries.attachAxis(chartAxisY)
        # markScatterSeries.attachAxis(chartAxisX)
        # markScatterSeries.attachAxis(chartAxisY)
        #
        # self.chart_view = QChartView(chart)
        # self.chart_view.setRenderHint(QPainter.Antialiasing, True)
        # self.widget_chart.layout().addWidget(self.chart_view)
        # chart.setBackgroundBrush(QColor(244, 246, 224))  # f4f6e0
        # self.chart_view.setBackgroundBrush(QColor(244, 246, 224))

    # def clearLayoutAllItems(self):
    #     if self.widget_chart.layout() != None:
    #         item_List = list(range(self.widget_chart.layout().count()))
    #         item_List.reverse()
    #         for i in item_List:
    #             item = self.widget_chart.layout().itemAt(i)
    #             self.widget_chart.layout().removeItem(item)
    #     else:
    #         v_box = QVBoxLayout()
    #         v_box.setSpacing(0)
    #         v_box.setContentsMargins(0, 0, 0, 0)
    #         self.widget_chart.setLayout(v_box)

    # def formatAxis(self, axis, min_value, max_value, step, isAxisX = False):
    #     pen_Axis = QPen()
    #     pen_Axis.setColor(Qt.blue)
    #     pen_Axis.setStyle(Qt.SolidLine)
    #     if step == 0:
    #         step = 0.25
    #     for s in axis.categoriesLabels():
    #         axis.remove(s)
    #     axis.setStartValue(min_value)
    #     axis.append('%g' % min_value, min_value)
    #     for i in range(math.ceil(min_value / step), math.floor(max_value / step) + 1):
    #         if isAxisX == True:
    #             step = int(step)
    #         v = i * step
    #         axis.append('%g' % v, v)
    #     axis.append('%g' % max_value, max_value)
    #     axis.setLinePen(pen_Axis)
    #     axis.setRange(min_value, max_value)
    #     axis.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
    #     axis.setGridLineVisible(True)
    #     axis.setMinorGridLineVisible(True)
    #     axis.setTickType(QValueAxis.TickType.TicksDynamic)
    #     pen_Grid = QPen()
    #     pen_Grid.setStyle(Qt.DotLine)
    #     pen_Grid.setColor(Qt.blue)
    #     axis.setGridLinePen(pen_Grid)
    #     axis.setMinorGridLinePen(pen_Grid)
    #     axis.setMinorTickCount(2)
    #     axis.setMinorGridLineColor(Qt.gray)
    #
    # def formatSeries(self, lineSeries, scatterSeries, markscatterSeries, markLineSeries, x_values, y_values):
    #     scatterSeries.setMarkerShape(QScatterSeries.MarkerShapeCircle)
    #     scatterSeries.setBorderColor(Qt.blue)
    #     scatterSeries.setBrush(Qt.blue)
    #     scatterSeries.setMarkerSize(6)
    #     markscatterSeries.setMarkerShape(QScatterSeries.MarkerShapeCircle)
    #     markscatterSeries.setBorderColor(Qt.red)
    #     markscatterSeries.setBrush(Qt.red)
    #     markscatterSeries.setMarkerSize(6)
    #     lineSeries.setBrush(Qt.blue)
    #     lineSeries.setPen(QPen(Qt.blue))
    #     markLineSeries.setBrush(Qt.red)
    #     markLineSeries.setPen(QPen(Qt.red))
    #     for value in range(0, len(x_values)):
    #         lineSeries.append(x_values[value], y_values[value])
    #         scatterSeries.append(x_values[value], y_values[value])
    #     scatterSeries.hovered.connect(self.slotScatterSeriesHovered)

    # def slotScatterSeriesHovered(self, point, state):
    #     if state:
    #         text = f"x：{point.x()}；y：{point.y()}"
    #         self.valueLabel.setText(text)
    #         font = self.valueLabel.font()
    #         fm = QFontMetrics(font)
    #         tmpWidth = fm.boundingRect(text).width() + 10
    #         self.valueLabel.setFixedWidth(tmpWidth)
    #         curPos = self.mapFromGlobal(QCursor.pos())
    #         if curPos.x() + 10 + tmpWidth <= self.width():
    #             self.valueLabel.move(curPos.x() + 10,
    #                                  curPos.y() - self.valueLabel.height()/2)
    #         else:
    #             self.valueLabel.move(curPos.x() - self.valueLabel.width(),
    #                                  curPos.y() - self.valueLabel.height() / 2)
    #         self.valueLabel.show()
    #     else:
    #         self.valueLabel.hide()

    def markPoint(self, pointNum, value):
        """求最大值、最小值、最初点、最后一个点 时需要标记点"""
        self.doOutPutFuncNone()
        self.widget_chart.addMarkPoint(pointNum, value)
        text = f"(x：{pointNum}；y：{value})"
        self.setSpecialValueLabelText(text)

    def addAverageLines(self, ave):
        """求平均值时，需要添加一条线"""
        self.doOutPutFuncNone()
        xValue = [0, len(self.times)-1]
        yValue = [ave, ave]
        self.widget_chart.addMarkLine(xValue, yValue)
        text = f"(mean：{ave})"
        self.setSpecialValueLabelText(text)

    def doOutPutFuncNone(self):
        """选择输出函数为None"""
        self.widget_chart.deleteSeriesByObjName('scatter_mark')
        self.widget_chart.deleteSeriesByObjName('line_mark')
        self.label_finalResult.clear()
        self.label_finalResult.hide()

    def setSpecialValueLabelText(self, text):
        self.label_finalResult.setText(text)
        font = self.label_finalResult.font()
        fm = QFontMetrics(font)
        tmpWidth = fm.boundingRect(text).width()
        self.label_finalResult.setFixedWidth(tmpWidth)
        self.label_finalResult.show()

    def getFinalOutputValueByFunc(self, strFunc, value):
        if value is None:
            self.doOutPutFuncNone()
        elif strFunc == OutputFunc.Max.value or strFunc == OutputFunc.Min.value or \
                strFunc == OutputFunc.Last.value or strFunc == OutputFunc.First.value:
            self.markPoint(value[0], value[1])
        elif strFunc == OutputFunc.Mean.value:
            self.addAverageLines(value[1])
        elif strFunc == OutputFunc.Sum.value:
            self.doOutPutFuncNone()
            self.setSpecialValueLabelText(f"(sum：{value[1]})")

    def slotBtnYesClicked(self):
        strName = self.lineEdit_name.text()
        if strName.isspace():
            reply = QMessageBox.question(self, "警告", "请输入变量名称", QMessageBox.Yes, QMessageBox.Yes)
            return
        data = ReadandWriteTemplateConf().data_FECalcuFile
        responseValueDict = data.responseValue
        if responseValueDict.get(strName) != None:
            reply = QMessageBox.question(self, "警告", "变量名重复，请重新输入",
                                         QMessageBox.Yes, QMessageBox.Yes)
            return
        else:
            tmpValue = {"solver": "LS-DYNA",
                        "fileType": SolverFileTyeEnum.rwforc.value,
                        "rigidID": self.rigidID,
                        "direction": self.direction,
                        "outputFunc": self.func,
                        "filePath": self.filePath}
            responseValueDict[strName] = tmpValue
            ReadandWriteTemplateConf().data_DOE.doe_ResponseName.append(strName)  # 向响应数据集中添加响应名称
        self.msg.emit(strName)
        parent = self.parent()
        while not isinstance(parent, myMaskWidget):
            parent = parent.parent()
        parent.close()

    def slotBtnCancelClicked(self):
        parent = self.parent()
        while not isinstance(parent, myMaskWidget):
            parent = parent.parent()
        parent.close()