from PostProcessing.ReadCAEResults.ui.Ui_DefineOutputByAbaqusODBFile import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QComboBox, QListView
import sys
import subprocess, shlex
import numpy as np
from AnalyzeProcessTemplates.public import OutputFunc, SolverFileTyeEnum, getBtnStyleString
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QCategoryAxis, QScatterSeries
from PyQt5.QtGui import QPainter, QPen, QCursor, QFontMetrics
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import math
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
import logging
from PublicTool.myMaskWidget import myMaskWidget

class DefineOutputByODBFile(QWidget, Ui_Form):
    msg = pyqtSignal(str)
    def __init__(self, ODBPath = r'D:\project_optPlatform\opt_platform\temp\V3_modified.odb'):
        super(DefineOutputByODBFile, self).__init__()
        self.setupUi(self)
        self.ODBPath = ODBPath
        self.batPath = r'C:\SIMULIA\Commands\abaqus.bat'
        cmd = self.batPath + 'python ' + self.ODBPath
        self.filePath = r'D:\project_optPlatform\opt_platform\PostProcessing\ReadCAEResults\ReadAbaqusOdbFile.py'
        self.params = 'None'
        self.setType = 0 # 1:instance, 2:nodeset, 4:elementSet
        self.curResultFile = ''
        self.parser = ParsingODBFile()
        self.exePraseODBFile()
        self.__initConnect__()
        self.__initUI__()

    def __initUI__(self):
        self.rB_FieldOutput.setChecked(True)
        self.rB_filterByNum.setChecked(True)
        stepList = self.ODBStructDict.get('_step_list')
        self.cbb_step.clear()
        self.cbb_step.addItems(stepList)
        self.lineEdit_name.setText('output_1')
        self.cbb_insORset.clear()
        if self.ODBStructDict.get('_instance_list'):
            self.cbb_insORset.addItem('_instance_list')
        if self.ODBStructDict.get('_nodeset_list'):
            self.cbb_insORset.addItem('_nodeset_list')
        if self.ODBStructDict.get('_elementset_list'):
            self.cbb_insORset.addItem('_elementset_list')
        self.slotCBBStepActivated()
        self.slotCBBInsORSetActivited()
        self.slotCBBFrameActivated()
        self.valueLabel = QLabel(self)
        self.valueLabel.setStyleSheet(
            "background-color: rgb(52, 134, 57);color: rgb(245, 245, 245);font: 12pt 'Times New Roman';")
        self.valueLabel.setAlignment(Qt.AlignCenter)
        self.valueLabel.hide()

        self.cbb_function_2.clear()
        self.cbb_function_2.addItem(OutputFunc.Max.value)
        self.cbb_function_2.addItem(OutputFunc.Min.value)
        self.cbb_function_2.addItem(OutputFunc.Mean.value)
        self.cbb_function_2.addItem(OutputFunc.Sum.value)
        self.cbb_function_2.addItem(OutputFunc.First.value)
        self.cbb_function_2.addItem(OutputFunc.Last.value)
        self.cbb_function_2.addItem(OutputFunc.NO.value)

        self.cbb_function.clear()
        self.cbb_function.addItem(OutputFunc.Max.value)
        self.cbb_function.addItem(OutputFunc.Min.value)
        # self.cbb_function.addItem(OutputFunc.Mean.value)
        self.cbb_function.addItem(OutputFunc.Sum.value)
        # self.cbb_function.addItem(OutputFunc.First.value)
        # self.cbb_function.addItem(OutputFunc.Last.value)
        # self.cbb_function.addItem(OutputFunc.NO.value)

        self.Btn_cancel.setStyleSheet(getBtnStyleString())
        self.Btn_yes.setStyleSheet(getBtnStyleString())
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def __initConnect__(self):
        self.cbb_step.activated.connect(self.slotCBBStepActivated)
        self.cbb_frame.activated.connect(self.slotCBBFrameActivated)
        self.cbb_insORset.activated.connect(self.slotCBBInsORSetActivited)
        self.cbb_component.activated.connect(self.slotCBBComponentActivated)
        self.cbb_insORsetName.activated.connect(self.slotCBBInsOrNodeNAmeActivited)
        self.cbb_region.activated.connect(self.slotCBBHistoryRegionActivated)
        self.cbb_type.activated.connect(self.slotCBBTypeActivated)
        self.cbb_function_2.activated.connect(self.slotCBBFunctionActivated)
        self.cbb_function.activated.connect(self.slotCBBFunctionActivated)
        self.lineEdit_filter.editingFinished.connect(self.slotFilterEditingFinished)
        self.Btn_yes.clicked.connect(self.slotBtnYesClicked)
        self.Btn_cancel.clicked.connect(self.slotBtnCancelClicked)
        self.lineEdit_filter.editingFinished.connect(self.slotFilterEdtingFinished)
        self.rB_FieldOutput.toggled.connect(self.slotChooseOutputType)
        self.rB_HistoryOutput.toggled.connect(self.slotChooseOutputType)
        self.rB_FieldOutput.toggled.connect(self.slotChooseFilter)
        self.rB_filterByNum.toggled.connect(self.slotChooseFilter)

    def slotCBBFunctionActivated(self):
        if self.rB_HistoryOutput.isChecked():
            self.curFunc = self.cbb_function_2.currentText()
            curData = self.parser.getHistoryTargetValueByOutputFunc(self.resultData[:, 0], self.resultData[:, 1], self.curFunc)
            self.getFinalOutputValueByFunc(self.curFunc, curData)
        else:
            self.curFunc = self.cbb_function.currentText()
            self.curDirec = self.cbb_compDirec.currentIndex()
            self.filter = self.lineEdit_filter.text()
            if self.rB_filterByFunc.isChecked():
                finalResults = self.parser.getFieldTargetValueByOutputFunc(self.resultData, self.curDirec, self.curFunc)
                self.getFinalOutputValueByFunc(self.curFunc, finalResults)
            elif self.rB_filterByNum.isChecked():
                finalResults = self.parser.getFieldTargetValueByOutputNum(self.resultData, self.curDirec, self.filter)
                self.getFinalOutputValueByFunc(self.filter, [self.filter, finalResults])

    def slotFilterEdtingFinished(self):
        if self.rB_FieldOutput.isChecked():
            if self.rB_filterByNum.isChecked():
                self.filter = self.lineEdit_filter.text()

    def slotChooseOutputType(self):
        if self.rB_FieldOutput.isChecked():
            self.stackedWidget.setCurrentIndex(0)
        else:
            self.rB_HistoryOutput.setChecked(True)
            self.stackedWidget.setCurrentIndex(1)
            self.slotCBBStepActivated()
            self.slotCBBHistoryRegionActivated()
            self.slotCBBTypeActivated()
        self.updateParamsAndExe()

    def slotChooseFilter(self):
        if self.rB_filterByFunc.isChecked():
            self.lineEdit_filter.setEnabled(False)
            self.cbb_function.setEnabled(True)
        else:
            self.lineEdit_filter.setEnabled(True)
            self.cbb_function.setEnabled(False)

    def slotCBBInsORSetActivited(self):
        curInsOrSet = self.cbb_insORset.currentText()
        self.cbb_insORsetName.clear()
        if curInsOrSet == '_instance_list':
            self.cbb_insORsetName.addItems(self.ODBStructDict.get('_instance_list'))
        elif curInsOrSet == '_nodeset_list':
            self.cbb_insORsetName.addItems(self.ODBStructDict.get('_nodeset_list'))
        elif curInsOrSet == '_elementset_list':
            self.cbb_insORsetName.addItems(self.ODBStructDict.get('_elementset_list'))
        self.updateParamsAndExe()

    def slotCBBStepActivated(self):
        """
        step combobox的槽函数
        :return:
        """
        curStep = self.cbb_step.currentText()
        if self.rB_FieldOutput.isChecked():
            curFrame = f'_frame_{curStep}'
            curFrameList = self.ODBStructDict[curFrame]
            self.cbb_frame.clear()
            self.cbb_frame.addItems(str(x) for x in curFrameList)
        else:
            curHistoryRegion = '_historyregion_' + str(curStep)
            curRegionList = self.ODBStructDict.get(curHistoryRegion)
            self.cbb_region.clear()
            self.cbb_region.addItems(curRegionList)
        self.updateParamsAndExe()

    def slotCBBHistoryRegionActivated(self):
        curStep = self.cbb_step.currentText()
        curRegion = self.cbb_region.currentText()
        curType = '_histype_' + str(curStep) + '_' + str(curRegion)
        curTypeList = self.ODBStructDict.get(curType)
        self.cbb_type.clear()
        if isinstance(curTypeList, list):
            self.cbb_type.addItems(curTypeList)
            self.updateParamsAndExe()

    def slotCBBTypeActivated(self):
        self.updateParamsAndExe()

    def slotCBBComponentActivated(self):
        self.updateParamsAndExe()

    def slotCBBFrameActivated(self):
        """
        FRAME combobox的槽函数
        :return:
        """
        curStep = self.cbb_step.currentText()
        curFrame = self.cbb_frame.currentText()
        curComponent = f'_component_{curStep}_{curFrame}'
        curComponentList = self.ODBStructDict.get(curComponent)
        self.cbb_component.clear()
        if isinstance(curComponentList, list):
            self.cbb_component.addItems(curComponentList)
            self.updateParamsAndExe()

    def slotCBBInsOrNodeNAmeActivited(self):
        self.updateParamsAndExe()

    def updateCBBComponentDirection(self):
        if self.rB_FieldOutput.isChecked():
            compoDirecNum = None
            if isinstance(self.resultData, dict):
                for value in self.resultData.values():
                    if isinstance(value, np.ndarray):
                        compoDirecNum = len(list(value))
                    elif isinstance(value, list):
                        compoDirecNum = len(value)
                    else:
                        compoDirecNum = 1
                    continue
            curComponent = self.cbb_component.currentText()
            self.cbb_compDirec.clear()
            if curComponent == 'U' and compoDirecNum == 3:
                self.cbb_compDirec.addItems(['U1', 'U2', 'U3', 'Mag'])
            elif curComponent == 'A' and compoDirecNum == 3:
                self.cbb_compDirec.addItems(['A1', 'A2', 'A3', 'Mag'])
            elif curComponent == 'AR' and compoDirecNum == 3:
                self.cbb_compDirec.addItems(['AR1', 'AR2', 'AR3', 'Mag'])
            elif curComponent == 'LE' and compoDirecNum == 4:
                self.cbb_compDirec.addItems(['LE11', 'LE22', 'LE33', 'LE12'])
            elif curComponent == 'LE' and compoDirecNum == 6:
                self.cbb_compDirec.addItems(['LE11', 'LE22', 'LE33', 'LE12', 'LE13', 'LE23'])
            elif curComponent == 'PE' and compoDirecNum == 4:
                self.cbb_compDirec.addItems(['PE11', 'PE22', 'PE33', 'PE12'])
            elif curComponent == 'PE' and compoDirecNum == 6:
                self.cbb_compDirec.addItems(['PE11', 'PE22', 'PE33', 'PE12', 'PE13', 'PE23'])
            elif curComponent == 'S' and compoDirecNum == 4:
                self.cbb_compDirec.addItems(['S11', 'S22', 'S33', 'S12', 'MISES'])
            elif curComponent == 'S' and compoDirecNum == 6:
                self.cbb_compDirec.addItems(['S11', 'S22', 'S33', 'S12', 'S13', 'S23', 'MISES'])
            elif curComponent == 'UR' and compoDirecNum == 3:
                self.cbb_compDirec.addItems(['UR1', 'UR2', 'UR3', 'Mag'])
            elif curComponent == 'V' and compoDirecNum == 3:
                self.cbb_compDirec.addItems(['V1', 'V2', 'V3', 'Mag'])
            elif curComponent == 'VR' and compoDirecNum == 3:
                self.cbb_compDirec.addItems(['VR1', 'VR2', 'VR3', 'Mag'])

    def addLineToChart(self, x_value, y_value, type, color):
        self.widget_chart.deleteSeriesByObjName(f'line_{type}')
        self.widget_chart.deleteSeriesByObjName(f'scatter_{type}')
        self.widget_chart.addLineSeries(x_value, y_value, type, color)
        self.widget_chart.addScatterSeries(x_value, y_value, type, color)

    def showChart(self, x_values, y_values):
        self.widget_chart.clearLayoutAllItems()
        self.widget_chart.createChart()
        self.widget_chart.createAxis(x_values, y_values)
        self.addLineToChart(x_values, y_values, self.cbb_type.currentText(), Qt.blue)

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

    def markPoint(self, pointNum, value):
        """求最大值、最小值、最初点、最后一个点 时需要标记点"""
        if pointNum is None and value is None:
            return
        self.doOutPutFuncNone()
        self.widget_chart.addMarkPoint(pointNum, value)
        text = f"(x：{pointNum}；y：{value})"
        self.setSpecialValueLabelText(text)

    def addAverageLines(self, ave):
        """求平均值时，需要添加一条线"""
        self.doOutPutFuncNone()
        xValue = [self.resultData[:, 0][0], self.resultData[:, 0][-1]]
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
        if self.rB_HistoryOutput.isChecked():
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
        else:
            if strFunc == OutputFunc.Max.value or strFunc == OutputFunc.Min.value:
                text = f"(x：{value[0]}；y：{value[1]})"
                self.label_FieldResult.setText(text)
            elif strFunc == OutputFunc.Sum.value:
                self.label_FieldResult.setText(f"(sum：{value[1]})")
            else:
                # Byfilter
                if value[1] is None:
                    self.label_FieldResult.setText(f'当前输入的节点/单元编号({value[0]})不存在，请重新输入正确的单元/节点编号！')
                else:
                    text = f"(x：{value[0]}；y：{value[1]})"
                    self.label_FieldResult.setText(text)

    def exePraseODBFile(self):
        self.parser.exePraseODBFile(self.batPath, self.filePath, self.ODBPath, self.params, self.setType)
        if self.params == 'None':
            self.ODBStructDict = np.load(self.ODBPath[0: self.ODBPath.rfind('\\') + 1] + 'curStruct.npy', encoding="latin1",
                                         allow_pickle=True).item()
        else:
            try:
                self.resultData = np.load(self.curResultFile.encode(), encoding="latin1", allow_pickle=True).item()
            except:
                self.resultData = np.load(self.curResultFile.encode(), encoding="latin1", allow_pickle=True)
            if self.rB_HistoryOutput.isChecked():
                if self.resultData.shape[1] == 2:
                    self.showChart(self.resultData[:, 0], self.resultData[:, 1])
                    self.curFunc = self.cbb_function_2.currentText()
                    curData = self.parser.getHistoryTargetValueByOutputFunc(self.resultData[:, 0], self.resultData[:, 1], self.curFunc)
                    self.getFinalOutputValueByFunc(self.curFunc, curData)
            else:
                self.updateCBBComponentDirection()

    def updateParamsAndExe(self):
        if self.rB_FieldOutput.isChecked():
            myStep = self.cbb_step.currentText()
            myFrame = self.cbb_frame.currentText()
            myInstance = self.cbb_insORsetName.currentText()
            myInsType = self.cbb_insORset.currentText()
            if myInsType == '_instance_list':
                self.setType = 1
            elif myInsType == '_nodeset_list':
                self.setType = 2
            elif myInsType == '_elementset_list':
                self.setType = 4
            myComponent = self.cbb_component.currentText()
            if myStep and myFrame and myInstance and myComponent:
                self.params = f'{myStep},{myFrame},{myInstance},{myComponent}'
                self.curResultFile = self.ODBPath[0: self.ODBPath.rfind('\\') + 1] +\
                                     'curResults_' + '_'.join(self.params.split(',')) + '.npy'
                self.exePraseODBFile()
        else:
            myStep = self.cbb_step.currentText()
            myHistoryRegion = self.cbb_region.currentText()
            myType = self.cbb_type.currentText()
            if myStep and myHistoryRegion and myType:
                self.params = f'{myStep},{myHistoryRegion},{myType}'
                self.curResultFile = self.ODBPath[0: self.ODBPath.rfind('\\') + 1] +\
                                     'curResults_' + '_'.join(self.params.split(',')) + '.npy'
                self.exePraseODBFile()

    def slotFilterEditingFinished(self):
        self.filter = self.lineEdit_filter.text()
        self.curDirec = self.cbb_compDirec.currentIndex()
        curData = self.parser.getFieldTargetValueByOutputNum(self.resultData, self.curDirec, self.filter)
        self.getFinalOutputValueByFunc(None, [self.filter, curData])

    def slotBtnYesClicked(self):
        if self.parser.isCorrectParams == False:
            reply = QMessageBox.question(self, "警告", "参数设置有误，请重新设置！", QMessageBox.Yes, QMessageBox.Yes)
            return
        strName = self.lineEdit_name.text()
        if strName.isspace():
            reply = QMessageBox.question(self, "警告", "请输入变量名称", QMessageBox.Yes, QMessageBox.Yes)
        data = ReadandWriteTemplateConf().data_FECalcuFile
        responseValueDict = data.responseValue
        if responseValueDict.get(strName) != None:
            reply = QMessageBox.question(self, "警告", "变量名重复，请重新输入",
                                         QMessageBox.Yes, QMessageBox.Yes)
        else:
            if self.rB_FieldOutput.isChecked() and self.rB_filterByFunc.isChecked():
                tmpValue = {"solver": "ABAQUS",
                            "fileType": SolverFileTyeEnum.odb.value,
                            "params": self.params,
                            "componentDirect": self.curDirec,
                            "func": self.curFunc,
                            "setType": self.setType,
                            "batPath": self.batPath,
                            "filePath": self.filePath,
                            "ODBPath": self.ODBPath,
                            "resultFilePath": self.curResultFile}
            elif self.rB_FieldOutput.isChecked() and self.rB_filterByNum.isChecked():
                tmpValue = {"solver": "ABAQUS",
                            "fileType": SolverFileTyeEnum.odb.value,
                            "params": self.params,
                            "componentDirect": self.curDirec,
                            "filter": self.filter,
                            "setType": self.setType,
                            "batPath": self.batPath,
                            "filePath": self.filePath,
                            "ODBPath": self.ODBPath,
                            "resultFilePath": self.curResultFile}
            elif self.rB_HistoryOutput.isChecked():
                tmpValue = {"solver": "ABAQUS",
                            "fileType": SolverFileTyeEnum.odb.value,
                            "params": self.params,
                            "func": self.curFunc,
                            "setType": self.setType,
                            "batPath": self.batPath,
                            "filePath": self.filePath,
                            "ODBPath": self.ODBPath,
                            "resultFilePath": self.curResultFile}
            data.responseValue[strName] = tmpValue
            ReadandWriteTemplateConf().data_DOE.doe_ResponseName.append(strName)  # 向响应数据集中添加响应名称
            logging.getLogger().info(f"响应值（{strName}）创建成功。")
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

class ParsingODBFile(QObject):
    isCorrectParams = False # 参数是否正确
    def __init__(self):
        super(ParsingODBFile, self).__init__()

    def exePraseODBFile(self, batPath:str, filePath:str, ODBPath:str, params:str, setType:int):
        """利用abaqus执行解析文件，获取数据"""
        p = subprocess.Popen([batPath, 'python', filePath, ODBPath, params, str(setType)],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() == None:
            out = p.stdout.readline().strip().decode()
            if out:
                print(out)
        # 子进程返回值
        print(p.returncode)

    def getHistoryTargetValueByOutputFunc(self, currentDataX, currentDataY, strFunc):
        """
        根据函数求取最终目标值
        :param currentData: 当前选择的数据集
        :param strFunc: 目标函数
        :return: 目标值位置/None，目标值
        """
        self.isCorrectParams = True
        if strFunc == OutputFunc.Max.value:
            index = np.argmax(currentDataY)
            value = currentDataY[index]
            index = list(currentDataX)[index]
            return index, value
        elif strFunc == OutputFunc.Min.value:
            index = np.argmin(currentDataY)
            value = currentDataY[index]
            index = list(currentDataX)[index]
            return index, value
        elif strFunc == OutputFunc.Mean.value:
            mean = currentDataY.mean()
            return None, mean
        elif strFunc == OutputFunc.Sum.value:
            sum = currentDataY.sum()
            return None, sum
        elif strFunc == OutputFunc.Last.value:
            lastValue = currentDataY[-1]
            index = list(currentDataX)[-1]
            return index, lastValue
        elif strFunc == OutputFunc.First.value:
            firstValue = currentDataY[0]
            index = list(currentDataX)[0]
            return index, firstValue
        else:
            self.isCorrectParams = False
            return None

    def getFieldTargetValueByOutputNum(self, resultData, curComponentDirec, curNum):
        results = resultData.get(int(curNum))
        if results is None:
            self.isCorrectParams = False
            return None
        else:
            self.isCorrectParams = True
            return results[curComponentDirec]

    def getFieldTargetValueByOutputFunc(self, resultData, curComponentDirec, curFunc):
        finalResult = None
        finalIndex = None
        for key, value in resultData.items():
            if value.ndim <= curComponentDirec:
                return None, None
            if curFunc == OutputFunc.Max.value:
                if finalResult is None:
                    finalResult = value[curComponentDirec]
                    finalIndex = key
                else:
                    if value[curComponentDirec] > finalResult:
                        finalResult = value[curComponentDirec]
                        finalIndex = key
            elif curFunc == OutputFunc.Min.value:
                if finalResult is None:
                    finalResult = value[curComponentDirec]
                    finalIndex = key
                else:
                    if value[curComponentDirec] < finalResult:
                        finalResult = value[curComponentDirec]
                        finalIndex = key
            elif curFunc == OutputFunc.Sum.value:
                if finalResult is None:
                    finalResult = value[curComponentDirec]
                    finalIndex = key
                else:
                    finalResult += value[curComponentDirec]
                    finalIndex = key
            else:
                self.isCorrectParams = False
                return None
        self.isCorrectParams = True
        return finalIndex, finalResult

    def getOutputValueByParameters(self, params:dict):
        """
        通过参数字典，获取对应的输出值
        :param params: 参数
        :return:
        """
        self.exePraseODBFile(params.get('batPath'),
                             params.get('filePath'),
                             params.get('ODBPath'),
                             params.get('params'),
                             params.get('setType'))
        curResultFile = params.get('resultFilePath')
        try:
            resultData = np.load(curResultFile.encode(), encoding="latin1", allow_pickle=True).item()
        except:
            resultData = np.load(curResultFile.encode(), encoding="latin1", allow_pickle=True)
        curFunc = params.get('func')
        curComponentDire = params.get('componentDirect')
        curFilter = params.get('filter')
        curData = None
        if curFunc and curComponentDire is None:
            # 历史输出
            curData = self.getHistoryTargetValueByOutputFunc(resultData[:, 0], resultData[:, 1], curFunc)
        elif curFunc and curComponentDire is not None:
            # 场输出 + function
            curData = self.getFieldTargetValueByOutputFunc(resultData, curComponentDire, curFunc)
        elif curFilter and curComponentDire is not None:
            # 场输出 + filter
            curData = self.getFieldTargetValueByOutputNum(resultData, curComponentDire, curFilter)
        if curData is None:
            logging.getLogger().error(f"获取结果失败，文件路径：{params.get('ODBPath')}")
        if len(curData) == 2:
            return curData[1]
        else:
            return curData

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DefineOutputByODBFile()
    ex.show()
    app.exec_()