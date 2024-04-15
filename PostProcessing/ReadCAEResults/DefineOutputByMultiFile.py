from PostProcessing.ReadCAEResults.ui.Ui_defineOutputByMultiFile import Ui_Form
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication
import os, sys
from PostProcessing.ReadCAEResults.ReadLsDynaResultsFile import ReadLsDynaResultsFile as d3plotReader
from PostProcessing.ReadCAEResults.ReadRwforcFile import ReadRwforcFile as rwforcReader
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from enum import Enum, unique
import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QColor
from ReadingData.ExcelFileReading import ExcelReader
from dtw import dtw
from fastdtw import fastdtw
from PyQt5.QtWidgets import QComboBox, QListView, QMessageBox
from AnalyzeProcessTemplates.public import SolverFileTyeEnum, getResultFileType, getBtnStyleString
from PostProcessing.ReadCAEResults.ReadRwforcFile import ReadRwforcFile
from PostProcessing.ReadCAEResults.ReadLsDynaResultsFile import ReadLsDynaResultsFile
import logging
from PublicTool.myMaskWidget import myMaskWidget
from sklearn.linear_model import LinearRegression
from PyQt5.QtChart import QScatterSeries

@unique
class AxisType(Enum): # 坐标轴
    Axis_x = 0
    Axis_y = 1

@unique
class SlopBtn(Enum):
    CAEStart = 0
    CAEEnd   = 1
    InputCurveStart = 2
    InputCurveEnd   = 3

class DefineOutputByMultiFile(QWidget, Ui_Form):
    msg = pyqtSignal(str)
    def __init__(self):
        super(DefineOutputByMultiFile, self).__init__()
        self.setupUi(self)
        self.xAxisData = None
        self.yAxisData = None
        self.compareCurveData = None
        self.whichSlopBtn = None
        self.slopCAEEnd = None
        self.slopCAEStart = None
        self.slopInputCurveEnd = None
        self.slopInputCurveStart = None
        self.resultReader = ReadMultiResultFile()
        self.__initUI__()
        self.__initConnect()

    def __initUI__(self):
        self.setWindowTitle('DefinedByMultiFiles')
        self.lineEdit_outputNme.setText('output_multiFile')
        self.setSimilarityFuncUI(False)
        self.setSlopFuncUI(False)
        self.cbb_func.addItem('Curve Similarity') # 两条曲线相似性
        self.cbb_func.addItem('Slop') # 两条曲线斜率比较
        self.cbb_func.addItem('Curve Area') #两条曲线与x轴的面积比较
        self.label_finalResult.setStyleSheet("color: rgb(216, 0, 0);font: 12pt 'Times New Roman';")
        self.widget_chart.setStyleSheet('background-color:#535353')
        self.btn_cancel.setStyleSheet(getBtnStyleString())
        self.btn_yes.setStyleSheet(getBtnStyleString())
        cbbText = ['FirstNode', 'LastNode', 'MaxValueNode', 'MinValueNode']
        self.cbb_CAESlopStartPos.addItems(cbbText)
        self.cbb_CAESlopEndPos.addItems(cbbText)
        self.cbb_InputCurveSlopStartPos.addItems(cbbText)
        self.cbb_InputCurveSlopEndPos.addItems(cbbText)
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def setSimilarityFuncUI(self, isShow:bool):
        """
        控制曲线相似性比较相关控件的显示或隐藏
        :param isShow: 显示：true;隐藏：false
        :return:
        """
        if isShow:
            self.label_curveFile.show()
            self.lineEdit_curvePath.show()
            self.btn_openCurveFile.show()
        else:
            self.label_curveFile.hide()
            self.lineEdit_curvePath.hide()
            self.btn_openCurveFile.hide()

    def setSlopFuncUI(self, isShow:bool):
        """
        控制曲线段斜率比较相关控件的显示隐藏
        :param isShow:
        :return:
        """
        if isShow:
            self.label_CAESlopEnd.show()
            self.label_CAESlopStart.show()
            self.label_InputCurveSlopEnd.show()
            self.label_InputCurveSlopStart.show()
            self.Btn_chooseCAESlopEnd.show()
            self.Btn_chooseCAESlopStart.show()
            self.Btn_chooseInputCurveEnd.show()
            self.Btn_chooseInputCurveSlopStart.show()
            self.cbb_CAESlopStartPos.show()
            self.cbb_CAESlopEndPos.show()
            self.cbb_InputCurveSlopEndPos.show()
            self.cbb_InputCurveSlopStartPos.show()
        else:
            self.label_CAESlopEnd.hide()
            self.label_CAESlopStart.hide()
            self.label_InputCurveSlopEnd.hide()
            self.label_InputCurveSlopStart.hide()
            self.Btn_chooseCAESlopEnd.hide()
            self.Btn_chooseCAESlopStart.hide()
            self.Btn_chooseInputCurveEnd.hide()
            self.Btn_chooseInputCurveSlopStart.hide()
            self.cbb_CAESlopStartPos.hide()
            self.cbb_CAESlopEndPos.hide()
            self.cbb_InputCurveSlopEndPos.hide()
            self.cbb_InputCurveSlopStartPos.hide()

    def __initConnect(self):
        self.btn_openFile_x.clicked.connect(self.slotBtnOpenFileClicked)
        self.btn_openFile_y.clicked.connect(self.slotBtnOpenFileClicked)
        self.cbb_outputType_x.activated.connect(self.slotCBBOutputTypeActivated)
        self.cbb_outputType_y.activated.connect(self.slotCBBOutputTypeActivated)
        self.cbb_outputPosition_x.activated.connect(self.slotCBBPositionActivated)
        self.cbb_outputPosition_y.activated.connect(self.slotCBBPositionActivated)
        self.cbb_component_x.activated.connect(self.slotCBBComponentActivated)
        self.cbb_component_y.activated.connect(self.slotCBBComponentActivated)
        self.cbb_func.activated.connect(self.slotCBBFunctionActivated)
        self.btn_openCurveFile.clicked.connect(self.slotBtnOpenCurveFileClicked)
        self.Btn_chooseCAESlopEnd.clicked.connect(self.slotSlopBtnClicked)
        self.Btn_chooseCAESlopStart.clicked.connect(self.slotSlopBtnClicked)
        self.Btn_chooseInputCurveEnd.clicked.connect(self.slotSlopBtnClicked)
        self.Btn_chooseInputCurveSlopStart.clicked.connect(self.slotSlopBtnClicked)
        self.widget_chart.msgClickedScatterPos.connect(self.slotScatterPositionGet)
        self.btn_yes.clicked.connect(self.slotBtnYesClicked)
        self.btn_cancel.clicked.connect(self.slotBtnCancelClicked)
        self.cbb_CAESlopStartPos.activated.connect(self.slotCbbSlopPosActivated)
        self.cbb_CAESlopEndPos.activated.connect(self.slotCbbSlopPosActivated)
        self.cbb_InputCurveSlopEndPos.activated.connect(self.slotCbbSlopPosActivated)
        self.cbb_InputCurveSlopStartPos.activated.connect(self.slotCbbSlopPosActivated)

    def slotBtnOpenFileClicked(self):
        """
        打开x/y轴数据文件按钮的槽函数
        :return:
        """
        filepath = self.getDir()
        if filepath:
            if self.sender() == self.btn_openFile_x:
                self.xAxisDataReader = self.getReaderByParsingFile(filepath)
                self.lineEdit_filePath_x.setText(filepath)
                self.getAllOutputTypes(AxisType.Axis_x)

            elif self.sender() == self.btn_openFile_y:
                self.yAxisDataReader = self.getReaderByParsingFile(filepath)
                self.lineEdit_filePath_y.setText(filepath)
                self.getAllOutputTypes(AxisType.Axis_y)

    def getAllOutputTypes(self, Type:AxisType):
        """
        获取当前结果文件中所有的结果类型，并显示到对应的CBB中
        :param Type:
        :return:
        """
        if Type == AxisType.Axis_x:
            obj = self.cbb_outputType_x
            if self.xAxisDataReader is not None:
                outputTypeDict = self.xAxisDataReader.getAllOutputType()
            else:
                return
        else:
            obj = self.cbb_outputType_y
            if self.yAxisDataReader is not None:
                outputTypeDict = self.yAxisDataReader.getAllOutputType()
            else:
                return
        for key, value in outputTypeDict.items():
            obj.addItem(key, value)

    def getReaderByParsingFile(self, filePath:str):
        """
        根据文件路径，解析
        :param filePath: 文件路径
        :return:
        """
        fileName = filePath[filePath.rfind('/') + 1:]
        splitName = fileName.split('.')
        if len(splitName) == 2:
            return None
        else:
            if fileName == 'd3plot':
                self.d3plotReader = d3plotReader(filePath)
                return self.d3plotReader
            elif fileName == 'rwforc':
                self.rwforcReader = rwforcReader(filePath)
                return self.rwforcReader
        return None


    def getDir(self):
        """
        获取用户指定的文件路径
        :return:
        """
        filepath = ReadandWriteTemplateConf().data_FECalcuFile.filePath
        fileNamePos = filepath.rfind('/') + 1
        newFilePath = filepath[:fileNamePos] + 'TryCalculation'
        dir = QFileDialog.getOpenFileName(self,  "选取文件", newFilePath, "All Files (*)") # 设置文件扩展名过滤,用双分号间隔
        return dir[0]

    def slotCBBOutputTypeActivated(self, index):
        """
        选择输出类型的槽函数
        :param index:
        :return:
        """
        resultType = self.sender().itemData(index)
        if self.sender() == self.cbb_outputType_x:
            self.cbb_outputPosition_x.clear()
            posList = self.xAxisDataReader.getAllPositionByOutputType(resultType)
            self.cbb_outputPosition_x.addItems(posList)
            self.xResultType = resultType
            self.updateCBBPositionIndex(AxisType.Axis_x, self.xResultType)
            self.xPositon = self.cbb_outputPosition_x.currentText()
            self.updateCBBComponentIndex(AxisType.Axis_x, self.xResultType, self.xPositon)
            self.xComponent = self.cbb_component_x.currentIndex()
            self.xAxisData = self.xAxisDataReader.getCurrentDataByOutputForm(self.xOutputData, self.xComponent)
        elif self.sender() == self.cbb_outputType_y:
            self.cbb_outputPosition_y.clear()
            posList = self.yAxisDataReader.getAllPositionByOutputType(resultType)
            self.cbb_outputPosition_y.addItems(posList)
            self.yResultType = resultType
            self.updateCBBPositionIndex(AxisType.Axis_y, self.yResultType)
            self.yPositon = self.cbb_outputPosition_y.currentText()
            self.updateCBBComponentIndex(AxisType.Axis_y, self.yResultType, self.yPositon)
            self.yComponent = self.cbb_component_y.currentIndex()
            self.yAxisData = self.yAxisDataReader.getCurrentDataByOutputForm(self.yOutputData, self.yComponent)
        self.plot()

    def slotCBBPositionActivated(self, index):
        """
        选择输出位置的槽函数
        :param index:
        :return:
        """
        if self.sender() == self.cbb_outputPosition_x:
            self.xPositon = self.cbb_outputPosition_x.currentText()
            self.updateCBBComponentIndex(AxisType.Axis_x, self.xResultType, self.xPositon)
            self.xComponent = self.cbb_component_x.currentIndex()
            self.xAxisData = self.xAxisDataReader.getCurrentDataByOutputForm(self.xOutputData, self.xComponent)
        else:
            self.yPositon = self.cbb_outputPosition_y.currentText()
            self.updateCBBComponentIndex(AxisType.Axis_y, self.yResultType, self.yPositon)
            self.yComponent = self.cbb_component_y.currentIndex()
            self.yAxisData = self.yAxisDataReader.getCurrentDataByOutputForm(self.yOutputData, self.yComponent)
        self.plot()

    def slotCBBComponentActivated(self, index):
        """
        component下拉菜单的槽函数
        :param index:
        :return:
        """
        if self.sender() == self.cbb_component_x:
            self.xComponent = index
            self.xAxisData = self.xAxisDataReader.getCurrentDataByOutputForm(self.xOutputData, index)
        else:
            self.yComponent = index
            self.yAxisData = self.yAxisDataReader.getCurrentDataByOutputForm(self.yOutputData, index)
        self.plot()

    def updateCBBPositionIndex(self, axisType, outputType):
        """
        更新position下拉菜单
        :param axisType: 坐标轴
        :param outputType: 输出类型
        :return:
        """
        if axisType == AxisType.Axis_x:
            positionList = self.xAxisDataReader.getAllPositionByOutputType(outputType)
            self.cbb_outputPosition_x.clear()
            self.cbb_outputPosition_x.addItems(positionList)
        else:
            positionList = self.yAxisDataReader.getAllPositionByOutputType(outputType)
            self.cbb_outputPosition_y.clear()
            self.cbb_outputPosition_y.addItems(positionList)

    def updateCBBComponentIndex(self, axisType: AxisType, outputType, position):
        """
        更新component下拉菜单
        :param axisType: 是x轴还是y轴
        :param outputType: 输出类型
        :param position: 位置
        :return:
        """
        if axisType == AxisType.Axis_x:
            self.xResultType = outputType
            self.xOutputData = self.xAxisDataReader.getOutputDataByTypeandPosition(self.xResultType, position)
            self.xOutputData = np.array(self.xOutputData)
            try:
                layerNum = self.xOutputData.shape[1]
            except:
                layerNum = 0
            componentList = self.xAxisDataReader.getAllComponentByOutputType(self.xResultType, layerNum)
            if componentList:
                self.cbb_component_x.clear()
                self.cbb_component_x.addItems(componentList)
        else:
            self.yOutputType = outputType
            self.yOutputData = self.yAxisDataReader.getOutputDataByTypeandPosition(self.yOutputType, position)
            self.yOutputData = np.array(self.yOutputData)
            try:
                layerNum = self.yOutputData.shape[1]
            except:
                layerNum = 0
            componentList = self.yAxisDataReader.getAllComponentByOutputType(self.yResultType, layerNum)
            if componentList:
                self.cbb_component_y.clear()
                self.cbb_component_y.addItems(componentList)

    def slotCBBFunctionActivated(self, index):
        self.curFunc = self.cbb_func.currentText()
        if self.curFunc == 'Curve Similarity':
            self.setSlopFuncUI(False)
            if self.compareCurveData is not None and self.xAxisData is not None and self.yAxisData is not None:
                dist = self.resultReader.getFinalResult(func=self.curFunc, yAxisData=self.yAxisData,
                                                        compareCurveData=self.compareCurveData)
                self.label_finalResult.setText(f"曲线距离：{dist}")
            else:
                self.setSimilarityFuncUI(True)
        elif self.curFunc == 'Curve Area':
            self.setSlopFuncUI(False)
            if self.compareCurveData is not None and self.xAxisData is not None and self.yAxisData is not None:
                areaDifferences = self.resultReader.getFinalResult(func=self.curFunc, xAxisData=self.xAxisData,
                                                                   yAxisData=self.yAxisData,
                                                                   compareCurveData=self.compareCurveData)
                self.label_finalResult.setText(f'曲线面积差：{areaDifferences}')
            else:
                self.setSimilarityFuncUI(True)
        elif self.curFunc == 'Slop':
            if self.compareCurveData is not None and self.xAxisData is not None and self.yAxisData is not None:
                if self.cbb_InputCurveSlopStartPos.isVisible() == False:
                    self.setSlopFuncUI(True)
            else:
                self.setSimilarityFuncUI(True)
                self.setSlopFuncUI(True)


    def slotBtnOpenCurveFileClicked(self):
        filepath = ReadandWriteTemplateConf().data_FECalcuFile.filePath
        dir = QFileDialog.getOpenFileName(self, "选取文件", filepath,
                                          "Excel Files (*.xls);; Excel Files (*.xlsx)")  # 设置文件扩展名过滤,用双分号间隔
        if dir[0]:
            self.lineEdit_curvePath.setText(dir[0])
            self.curveDataReader = ExcelReader(dir[0])
            sheetNameList = self.curveDataReader.getAllSheetsNames()
            self.compareCurveData = self.curveDataReader.getSheetContent(sheetNameList[0])
            try:
                self.addLineToChart(self.compareCurveData[:, 0], self.compareCurveData[:, 1], '对比曲线', Qt.red)
            except:
                self.widget_chart.createChart()
                self.widget_chart.createAxis(self.compareCurveData[:, 0], self.compareCurveData[:, 1])
                self.addLineToChart(self.compareCurveData[:, 0], self.compareCurveData[:, 1], '对比曲线', Qt.red)
            if self.curFunc == 'Curve Similarity':
                dist = self.resultReader.getFinalResult(func=self.curFunc, yAxisData=self.yAxisData,
                                                        compareCurveData=self.compareCurveData)
                self.label_finalResult.setText(f"曲线距离：{dist}")
            elif self.curFunc == 'Curve Area':
                areaDifferencec = self.resultReader.getFinalResult(func=self.curFunc, xAxisData=self.xAxisData,
                                                                   yAxisData=self.yAxisData,
                                                                   compareCurveData=self.compareCurveData)
                self.label_finalResult.setText(f'曲线面积差：{areaDifferencec}')

    def plot(self):
        self.widget_chart.clearLayoutAllItems()
        if self.xAxisData is None or self.yAxisData is None:
            return
        if self.xAxisData.shape != self.yAxisData.shape:
            minlen = min(self.xAxisData.shape[0], self.yAxisData.shape[0])
            self.xAxisData = self.xAxisData[0:minlen]
            self.yAxisData = self.yAxisData[0:minlen]
        self.widget_chart.createChart()
        self.widget_chart.createAxis(self.xAxisData, self.yAxisData)
        self.addLineToChart(self.xAxisData, self.yAxisData, '仿真曲线', Qt.blue)
        if self.compareCurveData is not None:
            self.addLineToChart(self.compareCurveData[:, 0], self.compareCurveData[:, 1], '对比曲线', Qt.red)

    def addLineToChart(self, x_value, y_value, type, color):
        self.widget_chart.deleteSeriesByObjName(f'line_{type}')
        self.widget_chart.deleteSeriesByObjName(f'scatter_{type}')
        self.widget_chart.addLineSeries(x_value, y_value, type, color)
        self.widget_chart.addScatterSeries(x_value, y_value, type, color)

    def slotSlopBtnClicked(self):
        if self.sender() == self.Btn_chooseCAESlopStart:
            self.whichSlopBtn = SlopBtn.CAEStart
        elif self.sender() == self.Btn_chooseCAESlopEnd:
            self.whichSlopBtn = SlopBtn.CAEEnd
        elif self.sender() == self.Btn_chooseInputCurveSlopStart:
            self.whichSlopBtn = SlopBtn.InputCurveStart
        elif self.sender() == self.Btn_chooseInputCurveEnd:
            self.whichSlopBtn = SlopBtn.InputCurveEnd

    def slotScatterPositionGet(self, pointx, pointy):
        if self.whichSlopBtn == SlopBtn.CAEStart:
            self.slopCAEStart = [pointx, pointy]
            self.cbb_CAESlopStartPos.setCurrentText(f'(x:{pointx}; y:{pointy})')
        elif self.whichSlopBtn == SlopBtn.CAEEnd:
            self.slopCAEEnd = [pointx, pointy]
            self.cbb_CAESlopEndPos.setCurrentText(f'(x:{pointx}; y:{pointy})')
        elif self.whichSlopBtn == SlopBtn.InputCurveStart:
            self.slopInputCurveStart = [pointx, pointy]
            self.cbb_InputCurveSlopStartPos.setCurrentText(f'(x:{pointx}; y:{pointy})')
        elif self.whichSlopBtn == SlopBtn.InputCurveEnd:
            self.slopInputCurveEnd = [pointx, pointy]
            self.cbb_InputCurveSlopEndPos.setCurrentText(f'(x:{pointx}; y:{pointy})')
        self.calculateSlopByPoint()
        self.addSlopLineToChart()

    def slotCbbSlopPosActivated(self):
        if self.sender() == self.cbb_CAESlopStartPos:
            self.slopCAEStart = self.sender().currentText()
        elif self.sender() == self.cbb_CAESlopEndPos:
            self.slopCAEEnd = self.sender().currentText()
        elif self.sender() == self.cbb_InputCurveSlopStartPos:
            self.slopInputCurveStart = self.sender().currentText()
        elif self.sender() == self.cbb_InputCurveSlopEndPos:
            self.slopInputCurveEnd = self.sender().currentText()
        self.calculateSlopByPoint()
        self.addSlopLineToChart()


    def calculateSlopByPoint(self):
        self.slopParams = {}
        if (self.slopCAEEnd is not None) and (self.slopCAEStart is not None):
            if isinstance(self.slopCAEEnd, list):
                self.slopParams['slopCAEEndID'] = self.resultReader.findNearestID(self.xAxisData, self.slopCAEEnd[0])
            else:
                if self.slopCAEEnd.__contains__('Value'):
                    self.slopParams['slopCAEEndID'] = self.resultReader.findIDByFunc(self.yAxisData, self.slopCAEEnd)
                else:
                    self.slopParams['slopCAEEndID'] = self.resultReader.findIDByFunc(self.xAxisData, self.slopCAEEnd)
            if isinstance(self.slopCAEStart, list):
                self.slopParams['slopCAEStartID'] = self.resultReader.findNearestID(self.xAxisData, self.slopCAEStart[0])
            else:
                if self.slopCAEStart.__contains__('Value'):
                    self.slopParams['slopCAEStartID'] = self.resultReader.findIDByFunc(self.yAxisData,
                                                                                       self.slopCAEStart)
                else:
                    self.slopParams['slopCAEStartID'] = self.resultReader.findIDByFunc(self.xAxisData, self.slopCAEStart)
        if (self.slopInputCurveEnd is not None) and (self.slopInputCurveStart is not None):
            if isinstance(self.slopInputCurveEnd, list):
                self.slopParams['slopInputCurveEndID'] = self.resultReader.findNearestID(self.compareCurveData[:, 0],
                                                                                         self.slopInputCurveEnd[0])
            else:
                if self.slopInputCurveEnd.__contains__('Value'):
                    self.slopParams['slopInputCurveEndID'] = self.resultReader.findIDByFunc(self.compareCurveData[:, 1],
                                                                                            self.slopInputCurveEnd)
                else:
                    self.slopParams['slopInputCurveEndID'] = self.resultReader.findIDByFunc(self.compareCurveData[:, 0],
                                                                                            self.slopInputCurveEnd)
            if isinstance(self.slopInputCurveStart, list):
                self.slopParams['slopInputCurveStartID'] = self.resultReader.findNearestID(self.compareCurveData[:, 0],
                                                                                           self.slopInputCurveStart[0])
            else:
                if self.slopInputCurveStart.__contains__('Value'):
                    self.slopParams['slopInputCurveStartID'] = self.resultReader.findIDByFunc(
                        self.compareCurveData[:, 1], self.slopInputCurveStart)
                else:
                    self.slopParams['slopInputCurveStartID'] = self.resultReader.findIDByFunc(
                        self.compareCurveData[:, 0], self.slopInputCurveStart)
        self.slopList = self.resultReader.getFinalResult('Slop', self.xAxisData, self.yAxisData, self.compareCurveData,
                                                         self.slopParams)
        if self.slopList is None:
            return
        self.slopInputCurve = self.slopList[1]
        self.slopCAECurve = self.slopList[0]
        if self.slopInputCurve is not None and self.slopCAECurve is not None:
            self.label_finalResult.setText(f'斜率差：{abs(self.slopList[0][0] - self.slopList[1][0])}')

    def addSlopLineToChart(self):
        if (self.slopCAEEnd is not None) and (self.slopCAEStart is not None):
            slopCAEEndID = self.slopParams.get('slopCAEEndID')
            slopCAEStartID = self.slopParams.get('slopCAEStartID')
            self.widget_chart.deleteSeriesByObjName(f'scatter_SlopPoints(CAEResults)')
            self.widget_chart.addScatterSeries(self.xAxisData[slopCAEStartID:slopCAEEndID+1],
                                               self.yAxisData[slopCAEStartID:slopCAEEndID+1],
                                               'SlopPoints(CAEResults)', QColor(0, 67, 200),
                                               QScatterSeries.MarkerShapeRectangle, 10)
            if self.slopCAECurve is not None:
                self.widget_chart.deleteSeriesByObjName(f'line_Slop(CAEResults)')
                self.widget_chart.addLineSeries(self.slopCAECurve[2][0], self.slopCAECurve[2][1],
                                                'Slop(CAEResults)', Qt.black, 3.0, Qt.DashDotLine)
        if (self.slopInputCurveEnd is not None) and (self.slopInputCurveStart is not None):
            if self.slopInputCurve is not None:
                self.widget_chart.deleteSeriesByObjName(f'line_Slop(InputCurve)')
                self.widget_chart.addLineSeries(self.slopInputCurve[2][0], self.slopInputCurve[2][1],
                                                'Slop(InputCurve)', Qt.green, 3.0, Qt.DashDotLine)

    def slotBtnYesClicked(self):
        strName = self.lineEdit_outputNme.text()
        if strName.isspace():
            reply = QMessageBox.question(self, "警告", "请输入变量名称", QMessageBox.Yes, QMessageBox.Yes)
        data = ReadandWriteTemplateConf().data_FECalcuFile
        responseValueDict = data.responseValue
        if responseValueDict.get(strName) != None:
            reply = QMessageBox.question(self, "警告", "变量名重复，请重新输入",
                                         QMessageBox.Yes, QMessageBox.Yes)
        else:
            paramDict = {}
            # x轴数据
            xfilepath = self.lineEdit_filePath_x.text()
            xfileType = getResultFileType(xfilepath)
            xDataParams = self.saveParametersByFileType(xfileType)
            if xDataParams is None:
                QMessageBox.question(self, "警告", "数据输入不完整，请检查！", QMessageBox.Yes, QMessageBox.Yes)
                return
            xDataParams['filePath'] = xfilepath
            paramDict['xDataParams'] = xDataParams
            # y轴数据
            yfilepath = self.lineEdit_filePath_y.text()
            yfileType = getResultFileType(yfilepath)
            yDataParams = self.saveParametersByFileType(yfileType)
            if yDataParams is None:
                QMessageBox.question(self, "警告", "数据输入不完整，请检查！", QMessageBox.Yes, QMessageBox.Yes)
                return
            yDataParams['filePath'] = yfilepath
            paramDict['yDataParams'] = yDataParams
            # 对比数据
            if self.compareCurveData is None:
                QMessageBox.question(self, "警告", "数据输入不完整，请检查！", QMessageBox.Yes, QMessageBox.Yes)
                return
            if self.compareCurveData is None:
                QMessageBox.question(self, "警告", "数据输入不完整，请检查！", QMessageBox.Yes, QMessageBox.Yes)
                return
            paramDict['CompareData'] = self.compareCurveData
            # 函数
            function = self.cbb_func.currentText()
            paramDict['function'] = function
            if function == 'Slop':
                # 仿真曲线上计算斜率的起点与终点的横坐标， 后续根据这两个横坐标点在新的仿真曲线上曲线计算斜率
                if isinstance(self.slopCAEStart, list):
                    StartPoint_CAESlop = self.slopCAEStart[0]
                else:
                    StartPoint_CAESlop = self.slopCAEStart
                if isinstance(self.slopCAEEnd, list):
                    EndPoint_CAESlop = self.slopCAEEnd[0]
                else:
                    EndPoint_CAESlop = self.slopCAEEnd
                Slop_InputCurve = self.slopInputCurve
                paramDict['StartPoint_CAESlop'] = StartPoint_CAESlop
                paramDict['EndPoint_CAESlop'] = EndPoint_CAESlop
                paramDict['Slop_InputCurve'] = Slop_InputCurve
            paramDict['fileType'] = SolverFileTyeEnum.multi.value
            responseValueDict[strName] = paramDict
            ReadandWriteTemplateConf().data_DOE.doe_ResponseName.append(strName)  # 向响应数据集中添加响应名称
            self.msg.emit(strName)
            parent = self.parent()
            while not isinstance(parent, myMaskWidget):
                parent = parent.parent()
            parent.close()

    def saveParametersByFileType(self, fileType):
        """
        通过文件类型保存参数
        :param fileType:文件类型
        :return:
        """
        DataParams = None
        if fileType == SolverFileTyeEnum.d3plot:
            DataParams = {"solver": "LS-DYNA",
                          "fileType": fileType.value,
                          "outputType": self.cbb_outputType_x.currentData(),
                          "position": self.cbb_outputPosition_x.currentText(),
                          "outputForm": self.cbb_component_x.currentIndex(),
                          "outputFunc": None}
        # y轴数据
        elif fileType == SolverFileTyeEnum.rwforc:
            DataParams = {"solver": "LS-DYNA",
                          "fileType": fileType.value,
                          "outputType": self.cbb_outputType_y.currentText(),
                          "rigidID": self.cbb_outputPosition_y.currentText(),
                          "direction": self.cbb_component_y.currentText(),
                          "outputFunc": None}
        return DataParams

    def getOutputParams(self):
        pass

    def slotBtnCancelClicked(self):
        parent = self.parent()
        while not isinstance(parent, myMaskWidget):
            parent = parent.parent()
        parent.close()

class ReadMultiResultFile(QObject):
    def __init__(self):
        super(ReadMultiResultFile, self).__init__()

    def getOutputValueByParameters(self, params:dict):
        xDataParams = params.get('xDataParams')
        yDataParams = params.get('yDataParams')
        compareData = params.get('CompareData')
        function = params.get('function')
        # 获取xData
        xData = self.getDataByParams(xDataParams)
        yData = self.getDataByParams(yDataParams)
        if xData is None or yData is None:
            logging.getLogger().error(f'未从结果文件中获取到数据！')
            return None
        slopParams = {}
        if function == 'Slop':
            if xData.shape != yData.shape:
                minlen = min(xData.shape[0], yData.shape[0])
                xData = xData[0:minlen]
                yData = yData[0:minlen]
            xStart = params.get('StartPoint_CAESlop')
            xEnd = params.get('EndPoint_CAESlop')
            if isinstance(xStart, str):
                if xStart.__contains__('Value'):
                    StartID = self.findIDByFunc(yData, xStart)
                else:
                    StartID = self.findIDByFunc(xData, xStart)
            else:
                StartID = self.findNearestID(xData, xStart)
            if isinstance(xEnd, str):
                if xEnd.__contains__('Value'):
                    EndID = self.findIDByFunc(yData, xEnd)
                else:
                    EndID = self.findIDByFunc(xData, xEnd)
            else:
                EndID = self.findNearestID(xData, xEnd)
            slopParams['slopCAEStartID'] = StartID
            slopParams['slopCAEEndID'] = EndID
            slopParams['slopInputCurve'] = params.get('Slop_InputCurve')
        finalResult = self.getFinalResult(function, xData, yData, compareData, slopParams)
        if function == 'Slop':
            return finalResult[0][0] - finalResult[1][0] # abs(finalResult[0][0] - finalResult[1][0])
        else:
            return finalResult

    def getDataByParams(self, params: dict):
        FileType = params.get('fileType')
        FilePath = params.get('filePath')
        targetValue = None
        if FileType == SolverFileTyeEnum.d3plot.value:
            if getResultFileType(FilePath) == SolverFileTyeEnum.unknow:
                FilePath = FilePath + '/d3plot'
            ReadLsDynaResultsFile().loadResultFile(FilePath)
            targetValue = ReadLsDynaResultsFile().getOutputValueByParameters(params)
        elif FileType == SolverFileTyeEnum.rwforc.value:
            if getResultFileType(FilePath) == SolverFileTyeEnum.unknow:
                FilePath = FilePath + '/rwforc'
            if ReadRwforcFile().praserFile(FilePath):
                targetValue = ReadRwforcFile().getOutputValueByParameters(params)
        return targetValue

    def getFinalResult(self, func, xAxisData=None, yAxisData=None, compareCurveData=None, slopPointDict={}):
        if func == 'Curve Similarity':
            d = self.getDTWValue(compareCurveData[:, 1], yAxisData)
            return d
        elif func == 'Curve Area':
            PosiAndNegaArea_CAE = self.getLineChartArea(xAxisData, yAxisData)
            PosiAndNegaArea_InputCurve = self.getLineChartArea(compareCurveData[:, 0], compareCurveData[:, 1])
            areaDifferencec = abs(PosiAndNegaArea_CAE[0] - PosiAndNegaArea_InputCurve[0]) + \
                              abs(PosiAndNegaArea_CAE[1] - PosiAndNegaArea_InputCurve[1])
            return areaDifferencec
        elif func == 'Slop':
            slopCAE = None #CAE计算得到的曲线的斜率数据
            slopInputCurve = None #输入曲线的斜率数据
            if slopPointDict:
                slopCAEEndID = slopPointDict.get('slopCAEEndID')
                slopCAEStartID = slopPointDict.get('slopCAEStartID')
                if slopCAEEndID is not None and slopCAEStartID is not None:
                    slopCAEDataX = xAxisData[slopCAEStartID:slopCAEEndID + 1]
                    slopCAEDataY = yAxisData[slopCAEStartID:slopCAEEndID + 1]
                    slopCAE = self.getSlopByData(slopCAEDataX, slopCAEDataY)
                slopInputCurve = slopPointDict.get('slopInputCurve')
                if slopInputCurve is None:
                    slopInputCurveEndID = slopPointDict.get('slopInputCurveEndID')
                    slopInputCurveStartID = slopPointDict.get('slopInputCurveStartID')
                    if slopInputCurveEndID is not None and slopInputCurveStartID is not None:
                        slopInputCurveDataX = compareCurveData[:, 0][slopInputCurveStartID : slopInputCurveEndID + 1]
                        slopInputCurveDataY = compareCurveData[:, 1][slopInputCurveStartID : slopInputCurveEndID + 1]
                        slopInputCurve = self.getSlopByData(slopInputCurveDataX, slopInputCurveDataY)
                return slopCAE, slopInputCurve
            return None

    def getDTWValue(self, y1, y2):
        """
        计算链条曲线的距离，用DTW算法
        :param y1:
        :param y2:
        :return:
        """
        y1 = list(y1)
        y2 = list(y2)
        distance_func = lambda y1, y2: np.abs(y1 - y2)
        d, path = fastdtw(y1, y2, dist=distance_func)
        return d

    def getLineChartArea(self, xArray, yArray):
        """
        计算数据点与X轴之间形成的面积
        :param xArray:
        :param yArray:
        :return:
        """
        xList = list(xArray)
        yList = list(yArray)
        dataLen = min(len(xList), len(yList))
        curArea_positive = 0
        curArea_negative = 0
        index = 0
        while index < dataLen - 1:
            firstNode = yList[index]
            secondNode = yList[index + 1]
            height = xList[index + 1] - xList[index]
            if secondNode >= 0 and firstNode >= 0:
                curArea_positive += (firstNode + secondNode) * (height) / 2
            elif secondNode < 0 and firstNode < 0:
                curArea_negative += abs((firstNode + secondNode) * (height) / 2)
            elif secondNode < 0 and firstNode >= 0:
                height1 = firstNode * height / (firstNode + abs(secondNode))
                curArea_positive += height1 * firstNode / 2
                curArea_negative += (height - height1) * abs(secondNode) / 2
            elif secondNode >= 0 and firstNode < 0:
                height1 = abs(firstNode) * height / (abs(firstNode) + secondNode)
                curArea_negative += height1 * abs(firstNode) / 2
                curArea_positive += (height - height1) * secondNode / 2
            index = index + 1
        return curArea_positive, curArea_negative

    def findNearestID(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    def findIDByFunc(self, array, strFunc):
        array = np.asarray(array)
        if strFunc == 'FirstNode':
            return 0
        elif strFunc == 'LastNode':
            return len(array) - 1
        elif strFunc == 'MaxValueNode':
            maxindex = np.argmax(array)
            return maxindex
        elif strFunc == 'MinValueNode':
            minindex = np.argmin(array)
            return minindex


    def getSlopByData(self, xData, yData):
        xData = xData.reshape(-1, 1)
        yData = yData.reshape(-1, 1)
        lineModel = LinearRegression()
        lineModel.fit(xData, yData)
        predictData = lineModel.predict(xData)
        return lineModel.coef_[0][0], lineModel.intercept_[0], [xData, predictData]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DefineOutputByMultiFile()
    ex.show()
    app.exec_()