from PostProcessing.ui.Ui_ModelingResult import Ui_ModelingResult
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QApplication, QHeaderView, QComboBox, QListView, QSizePolicy
from PyQt5.QtCore import Qt
from configFile.ReadTemplateConf import *
from ui.paraSetting.myTableWidget import myTableWidget
from sklearn.metrics import explained_variance_score #回归方差
from sklearn.metrics import mean_squared_error    #均方差
from sklearn.metrics import mean_absolute_error   #平均绝对误差
from sklearn.metrics import r2_score              #R平方值
from sklearn.metrics import median_absolute_error #中值绝对误差
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import logging
from PublicTool.myMessageDialog import myMessageDialog, MessageType
from PublicTool.myPublicDialogBackground import myPublicDialogBackground
from PublicTool.myMaskWidget import myMaskWidget

class ModelingResults(QWidget, Ui_ModelingResult):
    def __init__(self):
        super(ModelingResults, self).__init__()
        self.setupUi(self)
        self.doCalcuData()
        self.xText_lineChart = None
        self.yText_lineChart = None
        self.xText_surfacePlot = None
        self.yText_surfacePlot = None
        self.__initUI__()
        self.__initConnect__()
        self.createTableWidget()
        self.prepareSurfaceCanvas()
        self.createLinePlot()
        self.createSurfacePlot()

    def doCalcuData(self):
        # 获取各个模型的预测值与真实值
        self.preValueDict = {}
        model = ReadandWriteTemplateConf().data_SurrogateModel.SM_Model
        trainyData = ReadandWriteTemplateConf().data_SurrogateModel.SM_TrainyData
        self.dataX = trainyData[0]
        self.dataY = trainyData[1]
        self.XnameList = trainyData[2]
        self.YnameList = trainyData[3]
        for key, value in model.items():
            self.preValueDict[key] = value.predict(self.dataX)

    def __initUI__(self):
        self.cbb_AxisY.addItems(self.YnameList)
        self.cbb_AxisY_2.addItems(self.YnameList)
        # if len(self.YnameList) > 1:
        #     self.cbb_AxisY.addItem('all')
        self.cbb_AxisX.addItem('index')
        nVar = len(self.XnameList)
        if nVar > 1:
            for i in range(nVar):
                j = i + 1
                while j < nVar:
                    self.cbb_AxisX_2.addItem(f'{self.XnameList[i]}, {self.XnameList[j]}')
                    j += 1
        else:
            self.widget_SurfaceChart.hide()
        self.cbb_AxisX.addItems(self.XnameList)
        self.widget_SurfaceChart.setStyleSheet('QWidget#widget_SurfaceChart{background-color:#f4f6e0;}')
        # 设置qcombobox的样式
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def __initConnect__(self):
        self.cbb_AxisX.activated.connect(self.createLinePlot)
        self.cbb_AxisY.activated.connect(self.createLinePlot)
        self.cbb_AxisX_2.activated.connect(self.createSurfacePlot)
        self.cbb_AxisY_2.activated.connect(self.createSurfacePlot)

    def createLinePlot(self):
        curX = self.cbb_AxisX.currentText()
        curY = self.cbb_AxisY.currentText()
        if self.xText_lineChart == curX and self.yText_lineChart == curY:
            return
        else:
            self.xText_lineChart = curX
            self.yText_lineChart = curY
            self.createLines(self.xText_lineChart, self.yText_lineChart)

    def createSurfacePlot(self):
        curX = self.cbb_AxisX_2.currentText()
        curY = self.cbb_AxisY_2.currentText()
        if self.xText_surfacePlot == curX and self.yText_surfacePlot == curY:
            return
        else:
            self.xText_surfacePlot = curX
            self.yText_surfacePlot = curY
            if self.xText_surfacePlot.__contains__(', '):
                self.create3DSurface(self.xText_surfacePlot.split(', ')[0],
                                     self.xText_surfacePlot.split(', ')[1],
                                     self.yText_surfacePlot)

    def createLines(self, xText, yText):
        self.widget_LineChart.clearLayoutAllItems() # 删除现有曲线
        xValue = self.getVariableValueListByVariableName(xText)
        if yText == 'all':
            for outputName in self.YnameList:
                yValue = self.getOutputValueListByOutputName(outputName)
                self.addLineToChart(xValue, yValue, yText)
        else:
            yValue = self.getOutputValueListByOutputName(yText)
            if yValue is None:
                return
            if xText == 'index' and xValue is None:
                xValue = range(len(yValue))
            yPreValue = self.preValueDict.get(yText)
            self.widget_LineChart.clearLayoutAllItems()
            self.widget_LineChart.createChart()
            self.widget_LineChart.createAxis(xValue, yValue)
            self.addLineToChart(xValue, yValue, yText, Qt.blue)
            self.addLineToChart(xValue, yPreValue, f'{yText}Pre', Qt.red)

    def addLineToChart(self, x_value, y_value, type, color):
        self.widget_LineChart.addLineSeries(x_value, y_value, type, color)
        self.widget_LineChart.addScatterSeries(x_value, y_value, type, color)

    def getVariableValueListByVariableName(self, varName):
        """
        通过变量名获取对应的变量值
        :param varName: 变量名
        :return:
        """
        # 获取指定的变量值或者真实响应值
        value = None
        if varName in self.XnameList:
            index = list(self.XnameList).index(varName)
            value = self.dataX[:, index]
        elif varName in self.YnameList:
            index = list(self.YnameList).index(varName)
            value = self.dataY[:, index]
        return value

    def getOutputValueListByOutputName(self, outputName):
        """
        通过输出名获取对应的输出值
        :param outputName: 输出名
        :return:
        """
        value = None
        if outputName in self.YnameList:
            index = list(self.YnameList).index(outputName)
            value = self.dataY[:, index]
        return value

    def createTableWidget(self):
        SurrogateModel = ReadandWriteTemplateConf().data_SurrogateModel.SM_Model
        itemHeight = self.tableWidget_evaluationIndicator.itemHeight
        self.tableWidget_evaluationIndicator.setRowCount(len(SurrogateModel) + 1)
        tableHeight = self.tableWidget_evaluationIndicator.rowCount() * itemHeight + 10
        self.tableWidget_evaluationIndicator.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_evaluationIndicator.setFixedHeight(tableHeight)
        self.tableWidget_evaluationIndicator.setColumnCount(4)
        self.tableWidget_evaluationIndicator.setMyItem(0, 0, '模型名称', False)
        self.tableWidget_evaluationIndicator.setMyItem(0, 1, 'R2(可决系数)', False)
        self.tableWidget_evaluationIndicator.setMyItem(0, 2, 'RMSE(均方根误差)', False)
        self.tableWidget_evaluationIndicator.setMyItem(0, 3, 'MAE(平均绝对误差)', False)
        index = 1
        for key, value in SurrogateModel.items():
            self.tableWidget_evaluationIndicator.setRowHeight(index, itemHeight)
            self.tableWidget_evaluationIndicator.setMyItem(index, 0, key, False)
            indicators_r2 = value.cv_results_['mean_test_R2']
            indicators_rmse = value.cv_results_['mean_test_RMSE']
            indicators_mae = value.cv_results_['mean_test_MAE']
            index_r2 = list(value.cv_results_['rank_test_R2']).index(1)
            # index_rmse = list(value.cv_results_['rank_test_RMSE']).index(1)
            # index_mae = list(value.cv_results_['rank_test_MAE']).index(1)
            self.tableWidget_evaluationIndicator.setMyItem(index, 1, str(indicators_r2[index_r2]), False)
            self.tableWidget_evaluationIndicator.setMyItem(index, 2, str(indicators_rmse[index_r2]), False)
            self.tableWidget_evaluationIndicator.setMyItem(index, 3, str(indicators_mae[index_r2]), False)
            index += 1

    def prepareSurfaceCanvas(self):
        self.surfaceFigure = Figure_Canvas()
        self.surfaceFigureLayout = QVBoxLayout(self.widget_SurfaceChart)
        self.surfaceFigureLayout.addWidget(self.surfaceFigure)
        #self.surfaceFigure.ax.remove()
        #self.ax3d = self.surfaceFigure.fig.add_axes(Axes3D(self.surfaceFigure.fig))

    def create3DSurface(self, varName_1, varName_2, outputName):
        try:
            self.surfaceFigure.fig.clf() #清理画布
        except:
            pass
        ax3d = self.surfaceFigure.fig.add_axes(Axes3D(self.surfaceFigure.fig)) #重新添加绘图区域（坐标轴）
        ax3d.patch.set_facecolor("#f4f6e0")  # 设置ax区域背景颜色
        ax3d.patch.set_alpha(0.5)  # 设置ax区域背景颜色透明度
        self.surfaceFigure.fig.patch.set_facecolor('#f4f6e0')  # 设置绘图区域颜色
        # ax3d.axes.spines['bottom'].set_color('r')  # 设置下边界颜色
        ax3d.spines['top'].set_visible(False)  # 顶边界不可见
        ax3d.spines['right'].set_visible(False)  # 右边界不可见
        ax3d.spines['bottom'].set_visible(False)  # 下边界不可见
        ax3d.spines['right'].set_visible(False)  # 左边界不可见
        surfaceData = self.getSurfacePlotData(varName_1, varName_2, outputName)
        x_array = surfaceData[0]
        y_array = surfaceData[1]
        z_array = surfaceData[2]
        if (x_array is None) or (y_array is None) or (z_array is None):
            return
        if (x_array.shape == y_array.shape) and (y_array.shape == z_array.shape):
            # 作图
            ax3d.plot_surface(x_array, y_array, z_array, cmap='rainbow')
            ax3d.set_xlabel(varName_1)
            ax3d.set_ylabel(varName_2)
            ax3d.set_zlabel(outputName)
            self.surfaceFigure.fig.canvas.draw() #画布重绘
            self.surfaceFigure.fig.canvas.flush_events() #画布刷新
        else:
            logging.getLogger().info('数据出现错误，暂时无法绘图！')
            myMessage = myMessageDialog(MessageType.Error, "当前数据出现错误，暂时无法绘图！")
            self.mask_message = myMaskWidget(self.widget_SurfaceChart)
            backgroundWidget_message = myPublicDialogBackground()
            backgroundWidget_message.setTitle(MessageType.Error.value)
            backgroundWidget_message.setWidget(myMessage, False)
            self.mask_message.layout().addWidget(backgroundWidget_message)
            if self.mask_message.isVisible():
                self.mask_message.show()
                reply = myMessage.exec_()
                if reply:
                    self.mask_message.close()

    def getSurfacePlotData(self, varName_1, varName_2, outputName):
        # 定义三维数据
        nGrid = 85
        trainyData = ReadandWriteTemplateConf().data_SurrogateModel.SM_TrainyData
        self.dataX = trainyData[0]
        self.XnameList = trainyData[2]
        if varName_1 in self.XnameList and varName_2 in self.XnameList:
            var1_index = list(self.XnameList).index(varName_1)
            var2_index = list(self.XnameList).index(varName_2)
        else:
            logging.getLogger().error(f'无此变量{varName_1},{varName_2}, 无法进行后续曲面图绘制！')
            return None, None, None
        names = locals()
        for index in range(self.dataX.shape[1]):
            if index == var1_index or index == var2_index:
                minValue = min(self.dataX[:, index].tolist())
                maxValue = max(self.dataX[:, index].tolist())
                gap = (maxValue - minValue) / nGrid
                names['x_%s' % index] = np.arange(minValue, maxValue, gap)
            else:
                names['x_%s' % index] = np.array([self.dataX[0, index]])

        names['x_%s' % var1_index], names['x_%s' % var2_index] = eval(f'np.meshgrid(x_{var1_index}, x_{var2_index})')

        # 获取输出函数
        model = ReadandWriteTemplateConf().data_SurrogateModel.SM_Model
        for key, value in model.items():
            if key == outputName:
                func = value

        # 组建x，求Y
        z_array = np.empty([nGrid, nGrid], dtype=float)
        xlist = self.dataX[0, :]
        for i in range(nGrid):
            for j in range(nGrid):
                xlist[var1_index] = eval(f'x_{var1_index}[i, j]')
                xlist[var2_index] = eval(f'x_{var2_index}[i, j]')
                tmpY = func.predict(xlist.reshape(1, -1))
                z_array[i, j] = tmpY
        x_array = names['x_%s' % var1_index]
        y_array = names['x_%s' % var2_index]
        return x_array[0:nGrid, 0:nGrid], y_array[0:nGrid, 0:nGrid], z_array


class Figure_Canvas(FigureCanvas):
    def __init__(self, parent=None, width=3, height=2.7, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(Figure_Canvas, self).__init__(self.fig)
        self.ax = self.fig.add_axes(Axes3D(self.fig))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModelingResults()
    ex.show()
    app.exec_()
