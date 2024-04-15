from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QPen, QCursor, QFontMetrics, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QLabel, QMessageBox
import math
import numpy as np
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QCategoryAxis, QScatterSeries, QPieSeries, QPieSlice

class myLineChart(QWidget):
    msgClickedScatterPos = pyqtSignal(float, float)
    def __init__(self, parent):
        super(myLineChart, self).__init__(parent)
        self.valueLabel = QLabel(self)
        self.valueLabel.setStyleSheet(
            "background-color: rgb(52, 134, 57);color: rgb(245, 245, 245);font: 12pt 'Times New Roman';")
        self.valueLabel.setAlignment(Qt.AlignCenter)
        # self.valueLabel.hide()
        # v_box = QVBoxLayout()
        # v_box.setSpacing(0)
        # v_box.setContentsMargins(0, 0, 0, 0)
        # self.setLayout(v_box)
        self.createChart()
        self.setObjectName('myLineChart')

    def createChart(self):
        self.clearLayoutAllItems()
        """创建图"""
        self.chart = QChart()
        self.chart.setObjectName('myChart')
        self.chart.setTitle("")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.legend().hide()
        self.chart.setBackgroundBrush(QColor(244, 246, 224)) #f4f6e0
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing, True)
        self.layout().addWidget(self.chart_view)
        self.chart_view.setBackgroundBrush(QColor(244, 246, 224))

    def createAxis(self, x_values, y_values):
        """创建坐标轴"""
        self.chartAxisY = QCategoryAxis()
        y_maxValue = y_values[np.argmax(y_values)]
        y_minValue = y_values[np.argmin(y_values)]
        span_y = y_maxValue - y_minValue
        interval_y = span_y * 1.1 / (self.height() / 80)
        self.formatAxis(self.chartAxisY, y_minValue, y_maxValue, interval_y)
        self.chartAxisX = QCategoryAxis()
        x_maxValue = x_values[np.argmax(x_values)]
        x_minValue = x_values[np.argmin(x_values)]
        span_x = x_maxValue - x_minValue
        interval_x = span_x * 1.1 / (self.width() / 80)
        self.formatAxis(self.chartAxisX, x_minValue, x_maxValue, interval_x, True)
        # chart = self.findChild(QChart, 'myChart')
        self.chart.addAxis(self.chartAxisX, Qt.AlignBottom)
        self.chart.addAxis(self.chartAxisY, Qt.AlignLeft)

    def deleteAxis(self):
        axesList = self.chart.axes()
        for axes in axesList:
          self.chart.removeAxis(axes)

    def addLineSeries(self, x_value, y_value, type, color, lineWidth=2.0, penStyle=Qt.SolidLine):
        """添加折线"""
        lineSeries = QLineSeries()
        lineSeries.setObjectName(f'line_{type}')
        lineSeries.setName(f'line_{type}')
        lineSeries.setBrush(color)
        pen = QPen()
        pen.setColor(color)
        pen.setWidth(lineWidth)
        pen.setStyle(penStyle)
        lineSeries.setPen(pen)
        for value in range(0, len(x_value)):
            lineSeries.append(x_value[value], y_value[value])
        #chart = self.findChild(QChart, 'myChart')
        self.chart.addSeries(lineSeries)
        lineSeries.attachAxis(self.chartAxisX)
        lineSeries.attachAxis(self.chartAxisY)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignTop)
        self.updateAxisRange(x_value, y_value)

    def findMaxAndMinValue(self, points:list):
        if len(points) > 0:
            xmin = points[0].x()
            xmax = points[0].x()
            ymin = points[0].y()
            ymax = points[0].y()
            for point in points:
                xmin = min(xmin, point.x())
                xmax = max(xmax, point.x())
                ymin = min(ymin, point.y())
                ymax = max(ymax, point.y())
            return xmin, xmax, ymin, ymax
        return None

    def updateAxisRange(self, xValue, yValue):
        """
        添加曲线时，根据曲线范围更新图标的刻度范围
        :param xValue: x轴的值
        :param yValue: y轴的值
        :return:
        """
        seriesList = self.chart.series()
        xmin = None
        xmax = None
        ymin = None
        ymax = None
        for series in seriesList:
            curMaxMin = self.findMaxAndMinValue(series.points())
            if curMaxMin is None:
                continue
            if xmin is None:
                xmin = curMaxMin[0]
                xmax = curMaxMin[1]
                ymin = curMaxMin[2]
                ymax = curMaxMin[3]
            xmin = min(curMaxMin[0], xmin)
            xmax = max(curMaxMin[1], xmax)
            ymin = min(curMaxMin[2], ymin)
            ymax = max(curMaxMin[3], ymax)
        interval_x = (xmax - xmin) * 1.1 / (self.height() / 80)
        self.formatAxis(self.chartAxisX, xmin, xmax, interval_x, True)
        interval_y = (ymax - ymin) * 1.1 / (self.height() / 80)
        self.formatAxis(self.chartAxisY, ymin, ymax, interval_y)

    def deleteSeriesByObjName(self, objName):
        curSeries = self.chart.series()
        for series in curSeries:
            if series.objectName() == objName:
                self.chart.removeSeries(series)

    def addScatterSeries(self, x_value, y_value, type, color, markerShape=QScatterSeries.MarkerShapeCircle, markerSize=6):
        """添加散点"""
        scatterSeries = QScatterSeries()
        scatterSeries.setObjectName(f'scatter_{type}')
        scatterSeries.setName(f'scatter_{type}')
        scatterSeries.setMarkerShape(markerShape)
        scatterSeries.setBorderColor(color)
        scatterSeries.setBrush(color)
        scatterSeries.setMarkerSize(markerSize)
        try:
            for value in range(0, len(x_value)):
                scatterSeries.append(x_value[value], y_value[value])
        except:
            scatterSeries.append(x_value, y_value)
        #chart = self.findChild(QChart, 'myChart')
        self.chart.addSeries(scatterSeries)
        scatterSeries.hovered.connect(self.slotScatterSeriesHovered)
        scatterSeries.clicked.connect(self.slotScatterSeriesClicked)
        scatterSeries.attachAxis(self.chartAxisX)
        scatterSeries.attachAxis(self.chartAxisY)
        self.updateAxisRange(x_value, y_value)

    def clearLayoutAllItems(self):
        if self.layout() != None:
            item_List = list(range(self.layout().count()))
            item_List.reverse()
            for i in item_List:
                item = self.layout().itemAt(i)
                self.layout().removeItem(item)
        else:
            v_box = QVBoxLayout()
            v_box.setSpacing(0)
            v_box.setContentsMargins(0, 0, 0, 0)
            self.setLayout(v_box)

    def formatAxis(self, axis, min_value, max_value, step, isAxisX = False):
        if max_value > 5:
            max_value = math.ceil(max_value)
        pen_Axis = QPen()
        pen_Axis.setColor(Qt.blue)
        pen_Axis.setStyle(Qt.SolidLine)
        if step == 0:
            step = 0.25
        for s in axis.categoriesLabels():
            axis.remove(s)
        axis.setStartValue(min_value)
        axis.append('%g' % min_value, min_value)
        for i in range(math.ceil(min_value / step), math.floor(max_value / step) + 1):
            # if isAxisX == True:
            #     step = int(step)
            v = i * step
            axis.append('%g' % v, v)
        axis.append('%g' % max_value, max_value)
        axis.setLinePen(pen_Axis)
        axis.setRange(min_value, max_value)
        axis.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axis.setGridLineVisible(True)
        axis.setMinorGridLineVisible(True)
        axis.setTickType(QValueAxis.TickType.TicksDynamic)
        pen_Grid = QPen()
        pen_Grid.setStyle(Qt.DotLine)
        pen_Grid.setColor(Qt.blue)
        axis.setGridLinePen(pen_Grid)
        axis.setMinorGridLinePen(pen_Grid)
        axis.setMinorTickCount(2)
        axis.setMinorGridLineColor(Qt.gray)

    def slotScatterSeriesHovered(self, point, state):
        if state:
            text = f"x：{point.x()}；y：{point.y()}"
            self.valueLabel.setText(text)
            font = self.valueLabel.font()
            fm = QFontMetrics(font)
            tmpWidth = fm.boundingRect(text).width() + 10
            self.valueLabel.setFixedWidth(tmpWidth)
            curPos = self.mapFromGlobal(QCursor.pos())
            if curPos.x() + 10 + tmpWidth <= self.width():
                self.valueLabel.move(curPos.x() + 10,
                                     curPos.y() - self.valueLabel.height()/2)
            else:
                self.valueLabel.move(curPos.x() - self.valueLabel.width(),
                                     curPos.y() - self.valueLabel.height() / 2)
            self.valueLabel.raise_()
            self.valueLabel.show()
        else:
            self.valueLabel.hide()

    def slotScatterSeriesClicked(self, point):
        self.msgClickedScatterPos.emit(point.x(), point.y())

    def addMarkPoint(self, xValue, yValue):
        """
        添加标记点：最大值、最小值、第一个值，最后一个值等
        :param xValue:
        :param yValue:
        :return:
        """
        self.addScatterSeries(xValue, yValue, 'mark', Qt.red)

    def addMarkLine(self, xValue, yValue):
        """
        添加标记线
        :param xValue:
        :param yValue:
        :return:
        """
        self.addLineSeries(xValue, yValue, 'mark', Qt.red)

    def createPieChart(self, data: np.ndarray, variNameList: list, showNum: int):
        """
        创建饼状图
        :return:
        """
        pieSeries = QPieSeries()
        nRow, nCol = data.shape
        nameList = []
        dataList = []
        if nCol == 3:
            for indexRow in range(nRow):
                curValue = data[indexRow, 0]
                if curValue <= 0:
                    break
                index_x = int(data[indexRow, 1])
                index_y = int(data[indexRow, 2])
                if index_x == index_y:
                    nameList.append(variNameList[index_x - 1])
                else:
                    nameList.append(f'耦合（{variNameList[index_x - 1]}，{variNameList[index_y - 1]}）')
                dataList.append(curValue)
        elif nCol == 2:
            for indexRow in range(nRow):
                curValue = data[indexRow, 0]
                if curValue <= 0:
                    break
                index_x = int(data[indexRow, 1])
                nameList.append(variNameList[index_x - 1])
                dataList.append(curValue)

        curShowNum = 0
        for index_showNum in range(len(nameList)):
            if index_showNum < showNum:
                if dataList[index_showNum] > 0:
                    pieSeries.append(nameList[index_showNum], dataList[index_showNum])
                    curShowNum += 1
                else:
                    break
            else:
                break

        slice = QPieSlice()
        factor = 0.15
        for index in range(curShowNum):
            slice = pieSeries.slices()[index]
            slice.setLabelVisible(True)
            # slice.setBrush()
            # 比例小于0.1，增加臂长，防止标签堆积
            if slice.percentage() < 0.01:
                #slice.setLabelArmLengthFactor(factor)
                slice.setLabelVisible(False)
                #factor += 0.1
        # 调整起始角度、结束角度
        # if pieSeries.pieStartAngle() < 135:
        #     pieSeries.setPieStartAngle(135)
        #     pieSeries.setPieEndAngle(360+13)

        # self.chart.setTitle('各变量敏感性指标')
        self.chart.addSeries(pieSeries)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignRight)

        return curShowNum





















