"""
功能：创建模板分析流程的工厂，采用工厂模式
由于本软件根据选择模板功能的不同，需要创建组件不同的功能节点，实现具体的模板功能，因此采用工厂模式
"""

from abc import ABCMeta, abstractmethod
from CalculationProcess.CallAlgorithm import *
import threading
from PyQt5.QtCore import pyqtSignal, QObject

class BuildCalculateProcess(QObject):
    _instance = None
    _lock = threading.Lock()
    _initFlag = False
    msg_CalculateComplete = pyqtSignal()
    def __new__(cls, *args, **kw):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        with BuildCalculateProcess._lock:
            if not BuildCalculateProcess._initFlag:
                super().__init__()
                BuildCalculateProcess._initFlag = True

    def BuildAnalyseProcess(self, analyseType):
        self.analyseType = analyseType
        if analyseType == "fit":
            self.BuildFit()
        elif analyseType == "optimization":
            self.BuildOptmization()
        elif analyseType == "sa":
            self.BuildSA()
        elif analyseType == "doe":
            self.BuildDOE()
        elif analyseType == "optimization_FECalcu":
            self.BuildFECalcuOptimization()

    def BuildFit(self):
        self.function_DataInput = CallAlgorithm_DataInput()
        self.function_SA = CallAlgorithm_SA()
        self.function_SurrogateModeL = CallAlgorithm_SurrogateModel()
        self.function_DataInput.setNextProcess(self.function_SA)
        self.function_SA.setNextProcess(self.function_SurrogateModeL)

    def BuildOptmization(self):
        self.function_DataInput = CallAlgorithm_DataInput()
        self.function_SA = CallAlgorithm_SA()
        self.function_SurrogateModeL = CallAlgorithm_SurrogateModel()
        self.function_OptimizationAlgorithm = CallAlgorithm_Optimization()
        self.function_DataInput.setNextProcess(self.function_SA)
        self.function_SA.setNextProcess(self.function_SurrogateModeL)
        self.function_SurrogateModeL.setNextProcess(self.function_OptimizationAlgorithm)

    def BuildFECalcuOptimization(self):
        self.function_FECalcuFile = CallAlgorithm_FECalcuFile()
        self.function_DOE = CallAlgorithm_DOE()
        self.function_Simulation = CallAlgorithm_Simulation()
        self.function_SA = CallAlgorithm_SA()
        self.function_SurrogateModeL = CallAlgorithm_SurrogateModel()
        self.function_OptimizationAlgorithm = CallAlgorithm_Optimization()
        self.function_FECalcuFile.setNextProcess(self.function_DOE)
        self.function_DOE.setNextProcess(self.function_Simulation)
        self.function_Simulation.setNextProcess(self.function_SA)
        self.function_SA.setNextProcess(self.function_SurrogateModeL)
        self.function_SurrogateModeL.setNextProcess(self.function_OptimizationAlgorithm)

    def BuildSA(self):
        self.function_DataInput = CallAlgorithm_DataInput()
        self.function_SA = CallAlgorithm_SA()
        self.function_DataInput.setNextProcess(self.function_SA)

    def BuildDOE(self):
        self.function_DOE = CallAlgorithm_DOE()

    def Run(self):
        try:
            if self.analyseType == "optimization_FECalcu":
                self.function_FECalcuFile.doCalculate()
            else:
                self.function_DataInput.doCalculate()
            self.msg_CalculateComplete.emit()
        except:
            pass


class AnalyseTemplate(metaclass=ABCMeta):
    @abstractmethod
    def CreateTemplate(self):
        pass

class TemplateFit(AnalyseTemplate):
    def CreateTemplate(self):
        self.function_DataInput = CallAlgorithm_DataInput()
        self.function_SurrogateModeL = CallAlgorithm_SurrogateModel()
        self.function_DataInput.setNextProcess(self.function_SurrogateModeL)

class TemplateDoe(AnalyseTemplate):
    def CreateTemplate(self):
        self.function_Doe = CallAlgorithm_DOE()

class TemplateOpt(AnalyseTemplate):
    def CreateTemplate(self):
        self.function_DataInput = CallAlgorithm_DataInput()
        self.function_SurrogateModeL = CallAlgorithm_SurrogateModel()
        self.function_OptimizationAlgorithm = CallAlgorithm_Optimization()
        self.function_DataInput.setNextProcess(self.function_SurrogateModeL)
        self.function_SurrogateModeL.setNextProcess(self.function_OptimizationAlgorithm)

class TemplateSA(AnalyseTemplate):
    def CreateTemplate(self):
        self.function_DataInput = CallAlgorithm_DataInput()
        self.function_SA = CallAlgorithm_SA()
        self.function_DataInput.setNextProcess(self.function_SA)

class TemplateFactory(metaclass=ABCMeta):
    @abstractmethod
    def MakeAnalyseTemplate(self):
        pass

class FitProducer(TemplateFactory):
    def MakeAnalyseTemplate(self):
        return TemplateFit()

class DoeProducer(TemplateFactory):
    def MakeAnalyseTemplate(self):
        return TemplateDoe()

class SAProducer(TemplateFactory):
    def MakeAnalyseTemplate(self):
        return TemplateSA()

class OptProducer(TemplateFactory):
    def MakeAnalyseTemplate(self):
        return TemplateOpt()