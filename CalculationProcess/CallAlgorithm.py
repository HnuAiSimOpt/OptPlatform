from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from CalculationProcess.doDOE import doDOE
import logging
from CalculationProcess.doSimulation import DoSimulation
from CalculationProcess.doModeling import DoModeling
from CalculationProcess.doOptimization import DoOptimization
from CalculationProcess.doSensitiveAnalyse import DoSensitiveAnalyse
import threading
import inspect
import sys
from AnalyzeProcessTemplates.public import printGetInCurrentFunctionName, isDebug
from FiniteElementCalculationFileProcessing.ExtractAllCAEResults import ExtractAllCAEResults

class CallAlgorithm():
    nextProcess = None

    def setNextProcess(self, nextProcess):
        """设置下一个处理流程
        nextProcess:下一个流程
        """
        self.nextProcess = nextProcess

    def doCalculate(self):
        """计算
        calculationData：需要计算的数据
        """
        pass

class CallAlgorithm_DataInput(CallAlgorithm):
    """ 数据输入 DataInput"""
    def doCalculate(self):
        """检查输入的数据是否完整，可用于后续计算"""
        inputData = ReadandWriteTemplateConf().data_DataInput
        if (inputData.DataFile_TrainingSet_x is not None) and (inputData.DataFile_TrainingSet_y is not None) and (inputData.DataFile_TrainingSet_x.ndim == inputData.DataFile_TrainingSet_y.ndim):
            logging.getLogger().info("输入数据检查无误，继续进行后续分析")
        else:
            logging.getLogger().error("检测到输入数据不正确，计算已经中止！")
            return

        if self.nextProcess is not None:
            print("继续执行下一步")
            self.nextProcess.doCalculate()

class CallAlgorithm_FECalcuFile(CallAlgorithm):
    """ 导入计算文件"""
    def doCalculate(self):
        Data = ReadandWriteTemplateConf().data_FECalcuFile
        if Data.isEmpty() == False and len(Data.designVariable) > 0:
            logging.getLogger().info("设计变量检查无误，继续后续分析")
        else:
            logging.getLogger().error("检测到未从有限元计算文件中设置相关设计变量，请进行相关设置，计算中止！")
            return

        if self.nextProcess is not None:
            print("继续执行下一步")
            self.nextProcess.doCalculate()

class CallAlgorithm_DOE(CallAlgorithm):
    """ 实验设计DOE """
    def doCalculate(self):
        printGetInCurrentFunctionName(sys._getframe().f_code.co_name,
                                      inspect.getframeinfo(inspect.currentframe().f_back)[2],
                                      True)
        if not ReadandWriteTemplateConf().data_DOE.isEmpty():
            doe = doDOE()
            doe.do()
            logging.getLogger().info("实验设计成功")
        else:
            logging.getLogger().error("请先设置完成DOE相关参数！")
            return
        if self.nextProcess is not None:
            print("继续执行下一步")
            self.nextProcess.doCalculate()
        pass

class CallAlgorithm_Simulation(CallAlgorithm):
    """ 仿真计算 """
    def doCalculate(self):
        if isDebug:
            print("beforeSim threading id: %d" % threading.current_thread().ident)
        sim = DoSimulation()
        sim.exeCalculation()
        del sim
        if isDebug:
            print("afterSim threading id: %d" % threading.current_thread().ident)
        CAEResults = ExtractAllCAEResults()
        solverType = ReadandWriteTemplateConf().data_Simulation.solver
        folderPath = ReadandWriteTemplateConf().data_Simulation.folderPath
        CAEResults.getSimulationResults(solverType, folderPath)
        del CAEResults
        if isDebug:
            print("aftergetresults threading id: %d" % threading.current_thread().ident)
        logging.getLogger().info('批量求解完成！')
        # todo 判断数据是否可用
        if self.nextProcess is not None:
            print("sim to do nextthreading id: %d" % threading.current_thread().ident)
            self.nextProcess.doCalculate()

class CallAlgorithm_SA(CallAlgorithm):
    """ 敏感性分析 (SA)"""
    def doCalculate(self):
        if isDebug:
            print("敏感性分析SA")
            DoSensitiveAnalyse().run()
        if self.nextProcess is not None:
            print("继续执行下一步")
            self.nextProcess.doCalculate()
        pass

class CallAlgorithm_SurrogateModel(CallAlgorithm):
    """ 代理模型建模（SurrogateModel）"""
    def doCalculate(self):
        if isDebug:
            print("do modeling")
        DoModeling()
        logging.getLogger().info('完成代理模型拟合！')
        if self.nextProcess is not None:
            print("继续执行下一步")
            self.nextProcess.doCalculate()
        pass

class CallAlgorithm_Optimization(CallAlgorithm):
    """ 优化算法 （Optimization）"""
    def doCalculate(self):
        DoOptimization().do()
        logging.getLogger().info('优化算法执行结束！')
        if isDebug:
            print("执行优化算法")
        if self.nextProcess is not None:
            print("继续执行下一步")
            self.nextProcess.doCalculate()
        pass


    def myFunction(self, x):
        return ReadandWriteTemplateConf().data_SurrogateModel.SM_Model.predict(x.reshape(1, -1))




