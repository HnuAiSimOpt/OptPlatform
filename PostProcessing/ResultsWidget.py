from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QDockWidget, QTabWidget
from PostProcessing.ui.Ui_ResultsWidget import Ui_ResultsWidget
from PostProcessing import ModelingResults as MR
from PostProcessing.OptimizatioinResults import *
from PostProcessing.SensitiveAnalyseResults import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QCursor, QFontMetrics
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QLabel, QMessageBox
import math
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QCategoryAxis, QScatterSeries
from PublicTool.myMaskWidget import myMaskWidget
from AnalyzeProcessTemplates.public import TemplateNameEnum, getBtnStyleString

class ResultsWidget(QWidget, Ui_ResultsWidget):
    def __init__(self):
        super(ResultsWidget, self).__init__()
        self.setupUi(self)
        index = self.tabWidget.count() - 1
        while index >= 0:
            self.tabWidget.removeTab(index)
            index -= 1
        curTemplate = ReadandWriteTemplateConf().usrChoosnTemplate
        if curTemplate == TemplateNameEnum.Template_opt_FE.value or curTemplate == TemplateNameEnum.Template_opt.value:
            self.addWidgetToTabWidget('SensitiveAnalyse')
            self.addWidgetToTabWidget("Modeling")
            self.addWidgetToTabWidget("Optimization")
        elif curTemplate == TemplateNameEnum.Template_fit.value:
            self.addWidgetToTabWidget('SensitiveAnalyse')
            self.addWidgetToTabWidget("Modeling")
        self.__initConnect__()
        self.Btn_quit.setStyleSheet(getBtnStyleString())

    def __initConnect__(self):
        self.Btn_quit.clicked.connect(self.close)

    def addWidgetToTabWidget(self, Type):
        if Type == "Modeling":
            modelingResultWidget = MR.ModelingResults()
            self.tabWidget.addTab(modelingResultWidget, "建模结果")
        elif Type == "Optimization":
            optimizationiResultsWidget = OptimizationResults()
            self.tabWidget.addTab(optimizationiResultsWidget, "优化结果")
        elif Type == 'SensitiveAnalyse':
            sensitiveResultWidget = SensitiveAnalyseResults()
            self.tabWidget.addTab(sensitiveResultWidget, '敏感性分析结果')

    def close(self):
        parent = self.parent()
        while not isinstance(parent, myMaskWidget):
            parent = parent.parent()
        parent.close()
        QWidget.close(self)