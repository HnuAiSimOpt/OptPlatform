from PostProcessing.ReadCAEResults.ui.Ui_DefineOutputByD3plotFile import *
from PostProcessing.ReadCAEResults.ReadLsDynaResultsFile import *
from lasso.dyna import FilterType, ArrayType
from PyQt5.QtWidgets import QWidget, QApplication
import sys
import abc
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QCategoryAxis, QScatterSeries
from PyQt5.QtCore import Qt, pyqtSignal, QVariant
from PyQt5.QtGui import QPainter, QPen, QCursor, QFontMetrics, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QLabel, QMessageBox, QComboBox, QListView
import math
from configFile.ReadTemplateConf import *
from AnalyzeProcessTemplates.public import OutputFunc, getBtnStyleString
from PublicTool.myMaskWidget import myMaskWidget

class DefineOutputByCAEResultFile(QWidget, Ui_DefineOutputByCAEResultFile):
    defineOutputMsg = pyqtSignal(str)
    def __init__(self):
        super(DefineOutputByCAEResultFile, self).__init__()
        self.setupUi(self)

    """加载结果文件"""
    @abc.abstractmethod
    def loadingFile(self, filepath): pass

    """获取文件中存在的 所有结果集 """
    @abc.abstractmethod
    def getResultsSet(self): pass

    """获取 指定位置 指定类型的结果集"""
    @abc.abstractmethod
    def getResultByPos(self, pos, resultType): pass

    """获取 指定位置指定类型的结果集 的 指定表达形式 的 结果集"""
    @abc.abstractmethod
    def getResultSetoftheSpecifiedExpression(self): pass

    """根据 用户需求 获取指定表达形式结果集 的 最终值作为模型的输出"""
    @abc.abstractmethod
    def getResultValueasModelOutput(self): pass

class DefineLsDynaOutput(DefineOutputByCAEResultFile):
    def __init__(self):
        super(DefineLsDynaOutput, self).__init__()
        self.__initConnect__()
        self.setWindowTitle("Ls-Dyna输出值定义")
        self.lineEdit_name.setText("output_1")
        # 显示坐标点
        self.valueLabel = QLabel(self)
        self.valueLabel.setStyleSheet("background-color: rgb(52, 134, 57);color: rgb(245, 245, 245);font: 12pt 'Times New Roman';")
        self.valueLabel.setAlignment(Qt.AlignCenter)
        self.valueLabel.hide()
        # 显示最大值、最小值等特征点的坐标值
        self.label_specialValue.setStyleSheet("color: rgb(216, 0, 0);font: 12pt 'Times New Roman';")
        self.label_specialValue.setAlignment(Qt.AlignCenter)
        self.label_specialValue.hide()
        self.Btn_cancel.setStyleSheet(getBtnStyleString())
        self.Btn_yes.setStyleSheet(getBtnStyleString())
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def __initConnect__(self):
        self.comboBox_OutputType.activated.connect(self.slotcomboBoxOutputTypeActivated)
        self.comboBox_Pos.activated.connect(self.slotcomboBoxPosActivied)
        self.comboBox_OutputValue.activated.connect(self.slotcomboBoxOutputValueActivied)
        self.comboBox_OutputFunc.activated.connect(self.slotcomboBoxValueFuncActivated)
        self.Btn_yes.clicked.connect(self.slotBtnYesClicked)
        self.Btn_cancel.clicked.connect(self.slotBtnCancelClicked)

    def loadingFile(self, filepath):
        self.d3plotFilepath = filepath
        ReadLsDynaResultsFile().loadResultFile(filepath)
        self.getResultsSet()

    def getResultsSet(self):
        outputTypeDict = ReadLsDynaResultsFile().getAllOutputType()
        for key, value in outputTypeDict.items():
            self.comboBox_OutputType.addItem(key, value)

    def slotcomboBoxOutputTypeActivated(self, index):
        """选择输出类型下拉框的槽函数"""
        self.resultType = self.comboBox_OutputType.itemData(index)
        posList = ReadLsDynaResultsFile().getAllPositionByOutputType(self.resultType)
        self.comboBox_Pos.clear()
        if posList is None:
            self.comboBox_Pos.setEnabled(False)
            self.comboBox_Pos.addItem('None')
        else:
            self.comboBox_Pos.setEnabled(True)
            self.comboBox_Pos.addItems(posList)

        if self.comboBox_Pos.isEnabled():
            # 默认位置选择框中的当前选择为当前需要输出的位置
            if self.resultType == ArrayType.part_internal_energy \
                    or self.resultType == ArrayType.part_kinetic_energy \
                    or self.resultType == ArrayType.part_mass:

                # curPosList = list(self.dynaReader.getAllPartTitlesIDs())
                # curPosList.append('Total')
                # currentPos = curPosList[self.comboBox_Pos.currentIndex()]
                currentPos = self.comboBox_Pos.currentIndex()
            else:
                currentPos = self.comboBox_Pos.currentText()[1:]
        else:
            currentPos = None
        # 根据结果类型及位置信息，获取结果
        self.getOutputDataByCurrnetResultTypeAndCurrentPosChoosen(currentPos)
        # 根据输出类型，确定具体输出值的表达形式，并加到输出值选择下拉菜单
        self.addItemtocomboBox_OutputValue()
        # 根据位置，画图
        self.drawPlotBasedOnLocationInfo()
        # 添加处理函数
        self.setOutputFunc()
        self.getFinalOutputValueByFunc(self.comboBox_OutputFunc.currentText())

    def slotcomboBoxPosActivied(self, index):
        """位置下拉框的槽函数"""
        if self.resultType == ArrayType.part_internal_energy \
                or self.resultType == ArrayType.part_kinetic_energy \
                or self.resultType == ArrayType.part_mass:
            pos = self.comboBox_Pos.currentIndex()
        else:
            pos = self.comboBox_Pos.currentText()
        self.getOutputDataByCurrnetResultTypeAndCurrentPosChoosen(pos)
        self.drawPlotBasedOnLocationInfo()
        self.getFinalOutputValueByFunc(self.comboBox_OutputFunc.currentText())

    def drawPlotBasedOnLocationInfo(self):
        """根据位置信息获取结果创建图表"""
        # 获取当前输出值选择框的index
        index = self.comboBox_OutputValue.currentIndex()
        self.currentData = ReadLsDynaResultsFile().getCurrentDataByOutputForm(self.outputData, index)
        # 画图
        if self.currentData is None:
            return
        self.showChart()
        self.getFinalOutputValueByFunc(self.comboBox_OutputFunc.currentText())

    def getOutputDataByCurrnetResultTypeAndCurrentPosChoosen(self, pos):
        # 根据结果集中根据位置信息获取结果
        self.outputData = ReadLsDynaResultsFile().getOutputDataByTypeandPosition(self.resultType, pos)
        # 将数组格式化
        self.outputData = np.array(self.outputData)

    def slotcomboBoxOutputValueActivied(self, index):
        self.drawPlotBasedOnLocationInfo()
        #self.getFinalOutputValueByFunc(self.comboBox_OutputFunc.currentText())

    def addItemtocomboBox_OutputValue(self):
        """根据结果集添加item"""
        self.comboBox_OutputValue.clear()
        if self.outputData.ndim >= 2:
            layerNum = self.outputData.shape[1]
        elif self.outputData.ndim == 1:
            layerNum = self.outputData.shape[0]
        else:
            return
        componentList = ReadLsDynaResultsFile().getAllComponentByOutputType(self.resultType, layerNum)
        if componentList:
            self.comboBox_OutputValue.addItems(componentList)

    def addLineToChart(self, x_value, y_value, type, color):
        self.widget_chart.deleteSeriesByObjName(f'line_{type}')
        self.widget_chart.deleteSeriesByObjName(f'scatter_{type}')
        self.widget_chart.addLineSeries(x_value, y_value, type, color)
        self.widget_chart.addScatterSeries(x_value, y_value, type, color)

    def showChart(self):
        self.widget_chart.clearLayoutAllItems()
        if self.currentData is None:
            return
        self.widget_chart.createChart()
        x_values = range(len(self.currentData))
        y_values = self.currentData
        self.widget_chart.createAxis(x_values, y_values)
        self.addLineToChart(x_values, y_values, self.comboBox_OutputType.currentText(), Qt.blue)

    def setOutputFunc(self):
        self.comboBox_OutputFunc.clear()
        self.comboBox_OutputFunc.addItem(OutputFunc.Max.value)
        self.comboBox_OutputFunc.addItem(OutputFunc.Min.value)
        self.comboBox_OutputFunc.addItem(OutputFunc.Mean.value)
        self.comboBox_OutputFunc.addItem(OutputFunc.Sum.value)
        self.comboBox_OutputFunc.addItem(OutputFunc.First.value)
        self.comboBox_OutputFunc.addItem(OutputFunc.Last.value)
        self.comboBox_OutputFunc.addItem(OutputFunc.NO.value)

    def slotcomboBoxValueFuncActivated(self, index):
        curFunc = self.comboBox_OutputFunc.currentText()
        self.getFinalOutputValueByFunc(curFunc)

    def getFinalOutputValueByFunc(self, strFunc):
        if self.currentData is None:
            return
        value = ReadLsDynaResultsFile().getTargetValueByOutputFunc(self.currentData, strFunc)
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

    def markPoint(self, pointNum, value):
        """求最大值、最小值、最初点、最后一个点 时需要标记点"""
        self.doOutPutFuncNone()
        self.widget_chart.addMarkPoint(pointNum, value)
        text = f"(x：{pointNum}；y：{value})"
        self.setSpecialValueLabelText(text)

    def addAverageLines(self, ave):
        """求平均值时，需要添加一条线"""
        self.doOutPutFuncNone()
        xValue = [0, len(self.currentData)-1]
        yValue = [ave, ave]
        self.widget_chart.addMarkLine(xValue, yValue)
        text = f"(mean：{ave})"
        self.setSpecialValueLabelText(text)

    def doOutPutFuncNone(self):
        """选择输出函数为None"""
        self.widget_chart.deleteSeriesByObjName('scatter_mark')
        self.widget_chart.deleteSeriesByObjName('line_mark')
        self.label_specialValue.clear()
        self.label_specialValue.hide()

    def setSpecialValueLabelText(self, text):
        self.label_specialValue.setText(text)
        font = self.label_specialValue.font()
        fm = QFontMetrics(font)
        tmpWidth = fm.boundingRect(text).width()
        self.label_specialValue.setFixedWidth(tmpWidth)
        self.label_specialValue.show()

    def slotBtnYesClicked(self):
        """
        确定按钮槽函数，用于保存响应值信息
        """
        # 检查用户是否选择了一个明确的输出作为响应
        strName = self.lineEdit_name.text() #名称
        outputType = self.comboBox_OutputType.currentData() #输出类型
        if self.resultType == ArrayType.part_internal_energy \
                or self.resultType == ArrayType.part_kinetic_energy \
                or self.resultType == ArrayType.part_mass:
            position = str(self.comboBox_Pos.currentIndex())
        else:
            position = self.comboBox_Pos.currentText() #单元编号
        outputForm = self.comboBox_OutputValue.currentIndex() #输出形式
        outputFunc = self.comboBox_OutputFunc.currentText() #处理函数
        if strName.isspace():
            reply = QMessageBox.question(self, "警告", "请输入变量名称", QMessageBox.Yes, QMessageBox.Yes)
        elif position.isspace():
            reply = QMessageBox.question(self, "警告", "请选择位置信息", QMessageBox.Yes, QMessageBox.Yes)
        elif outputFunc == 'None':
            reply = QMessageBox.question(self, "警告", "请选择处理函数", QMessageBox.Yes, QMessageBox.Yes)
        else:
            data = ReadandWriteTemplateConf().data_FECalcuFile
            responseValueDict = data.responseValue
            if responseValueDict.get(strName) != None:
                reply = QMessageBox.question(self, "警告", "变量名重复，请重新输入",
                                             QMessageBox.Yes, QMessageBox.Yes)
            else:
                tmpValue = {"solver": "LS-DYNA",
                            "fileType": "d3plot",
                            "outputType": outputType,
                            "position": position,
                            "outputForm": outputForm,
                            "outputFunc": outputFunc,
                            "filePath": self.d3plotFilepath}
                responseValueDict[strName] = tmpValue
                ReadandWriteTemplateConf().data_DOE.doe_ResponseName.append(strName) # 向响应数据集中添加响应名称
                self.defineOutputMsg.emit(strName)
                parent = self.parent()
                while not isinstance(parent, myMaskWidget):
                    parent = parent.parent()
                parent.close()


    def slotBtnCancelClicked(self):
        parent = self.parent()
        while not isinstance(parent, myMaskWidget):
            parent = parent.parent()
        parent.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DefineLsDynaOutput()
    ex.loadingFile("D:\\优化平台项目\\opt_platform\\temp\\复合材料三点弯\\7-5\\myD3plot")
    ex.show()
    app.exec_()

