from PyQt5.QtCore import QObject
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from numpy.core.fromnumeric import ptp
sys.path.append(os.getcwd())
from SensitiveAnalyseAlgorithm import Morris, RSHDMR, Sobol
from configFile.ReadTemplateConf import *
from AnalyzeProcessTemplates.public import getTrainyData
import logging

class DoSensitiveAnalyse(QObject):
    def __init__(self):
        super(DoSensitiveAnalyse, self).__init__()

    def run(self):
        ReadandWriteTemplateConf().ProgressBar_curCalculateStep = '敏感性分析中...'
        ReadandWriteTemplateConf().ProgressBar_isAuto = True
        self.SASortBox = []
        self.SiBox = []
        self.SaBox = []

        trainyData = getTrainyData()
        trainy_x = trainyData[0]
        trainy_y = trainyData[1]
        variableNameList = trainyData[2]
        outputNameList = trainyData[3]
        if (trainy_x is None) or (trainy_y is None) or (variableNameList is None) or (outputNameList is None):
            logging.getLogger().error("未找到用于敏感性分析的数据，请检查！")
            return
        nResponse = trainy_y.shape[1]
        SAMethodName = ReadandWriteTemplateConf().data_SensitiveAnalyse.SA_Name
        if SAMethodName == "RSHDMR":
            for index in range(nResponse):
                SaSort, Si, Sa = RSHDMR.rs_hdmr(trainy_x, trainy_y[:, index])
                self.SASortBox.append(SaSort)
                self.SiBox.append(Si)
                self.SaBox.append(Sa)
        elif SAMethodName == "Morris":
            for index in range(nResponse):
                SaSort, Si, Sa = Morris.morris_model(trainy_x, trainy_y[:, index])
                self.SASortBox.append(SaSort)
                self.SiBox.append(Si)
                self.SaBox.append(Sa)
        elif SAMethodName == "Sobol":
            for index in range(nResponse):
                SaSort, Si, Sa = Sobol.sobol_model(trainy_x, trainy_y[:, index])
                self.SASortBox.append(SaSort)
                self.SiBox.append(Si)
                self.SaBox.append(Sa)
        SAResultsDict = {}
        SAResultsDict["SASortBox"] = self.SASortBox
        SAResultsDict["SiBox"] = self.SiBox
        SAResultsDict["SaBox"] = self.SaBox
        SAResultsDict["variableNameList"] = variableNameList
        SAResultsDict["outputNameList"] = outputNameList
        ReadandWriteTemplateConf().data_SensitiveAnalyse.SA_Result = SAResultsDict