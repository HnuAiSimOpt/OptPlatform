from doepy import build
from configFile.ReadTemplateConf import *
import logging
from FiniteElementCalculationFileProcessing.GenerateCalculationFile import GenerateCalcuFile
from PyQt5.QtCore import QObject
import numpy as np
import pandas as pd

class doDOE(QObject):
    def __init__(self):
        super(doDOE, self).__init__()

    def do(self):
        """
        执行实验设计
        :return: 无
        """
        self.doeData = ReadandWriteTemplateConf().data_DOE
        self.designRange = ReadandWriteTemplateConf().data_DOE.doe_VariablesValueRange
        if self.doeData.doe_Method == 'LHS':
            self.doeData.doe_SampleSet = build.lhs(self.designRange, num_samples=int(self.doeData.doe_SampleSize)).values
            logging.getLogger().info(f"执行实验设计成功：实验设计方法（{self.doeData.doe_Method}），"
                                     f"变量数（{len(self.designRange)}），采样数（{self.doeData.doe_SampleSize}）")
        self.generateCalculationFile()

    def generateCalculationFile(self):
        """
        根据实验设计结果生成可计算文件
        :return:无
        """
        genFile = GenerateCalcuFile()
        genFile.do()