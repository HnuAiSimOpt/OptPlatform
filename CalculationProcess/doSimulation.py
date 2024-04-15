from CalculationProcess.ParelRunner import *
from AnalyzeProcessTemplates.public import maskProgress

class DoSimulation(QObject):
    def __init__(self):
        super(DoSimulation, self).__init__()
        self.sampleNum = ReadandWriteTemplateConf().data_DOE.doe_SampleSize

    def exeCalculation(self):
        """执行有限元计算"""
        data = ReadandWriteTemplateConf().data_Simulation
        # thread = myThread(nCPU=data.NCPU, filePath=data.folderPath,
        #                   commucation=maskProgress, nProcessor=data.NProcessor,
        #                   cmd=data.cmd, solverType=data.solver, sampleNum=self.sampleNum)
        # thread.start()
        # thread.wait()