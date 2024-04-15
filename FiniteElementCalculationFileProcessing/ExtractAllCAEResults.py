import sys
import os
import datetime
import inspect
import numpy as np
import logging
import pandas as pd
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread, QRunnable, QThreadPool
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from AnalyzeProcessTemplates.public import isDebug, printGetInCurrentFunctionName, SolverTypeEnum, SolverFileTyeEnum
from PostProcessing.ReadCAEResults.ReadLsDynaResultsFile import ReadLsDynaResultsFile
from PostProcessing.ReadCAEResults.ReadRwforcFile import ReadRwforcFile
from PostProcessing.ReadCAEResults.DefineOutputByODBFile import ParsingODBFile
from PostProcessing.ReadCAEResults.DefineOutputByMultiFile import ReadMultiResultFile


class ExtractAllCAEResults(QObject):
    def __init__(self):
        super(ExtractAllCAEResults, self).__init__()

    def getSimulationResults(self, solverType, folderPath):
        ReadandWriteTemplateConf().ProgressBar_curCalculateStep = '读取结果文件中...'
        ReadandWriteTemplateConf().ProgressBar_isAuto = True
        printGetInCurrentFunctionName(sys._getframe().f_code.co_name,
                                      inspect.getframeinfo(inspect.currentframe().f_back)[2],
                                      True)
        FEResponseValue = ReadandWriteTemplateConf().data_FECalcuFile.responseValue
        doeData = ReadandWriteTemplateConf().data_DOE
        rowNum = int(doeData.doe_SampleSize)
        colNum = len(doeData.doe_ResponseName)
        if isDebug:
            print(f'---------------------{rowNum}, {colNum}---------------------')
        doeData.doe_ResponseSet = np.zeros(shape=(rowNum, colNum))  # 创建一个指定大小的数组，用于存储响应值
        reaponseValue = np.zeros(shape=(rowNum, colNum))
        if colNum != len(FEResponseValue):
            logging.getLogger().error("模型响应数据有误，请检查代码")
            return

        # if solverType == SolverTypeEnum.LsDyna:
        #     for index_i in range(rowNum):
        #         for index_j in range(colNum):
        #             # 检查计算得到的结果文件是否完整
        #             fileLst = []
        #             for path, dir, files in os.walk(folderPath+f'rmpod_{index_i}'):
        #                 fileLst += files
        #             if fileLst != ReadandWriteTemplateConf().data_FECalcuFile.resultFileList:
        #                 logging.getLogger().info('此结果文件存在问题，无法解析结果：'+folderPath+f'rmpod_{index_i}')
        #                 continue
        #             valueDict = FEResponseValue.get(doeData.doe_ResponseName[index_j])
        #             if valueDict is None:
        #                 logging.getLogger().info("数据错误，程序需中止！")
        #                 return
        #
        #             if valueDict.get('fileType') == SolverFileTyeEnum.d3plot.value:
        #                 d3plotFilePath = folderPath + f'rmpod_{index_i}/d3plot'
        #                 d3plotFilePath.replace('/', '\\')
        #                 print(f'------------------------------------------------------{d3plotFilePath}-----------------------------------------------------\n')
        #                 if os.path.exists(d3plotFilePath):
        #                     if ReadLsDynaResultsFile().loadResultFile(d3plotFilePath):
        #                         if isDebug:
        #                             print(
        #                                 f'---------------------{datetime.datetime.now()},:正在解析的文件编号为{index_i}---------------------\n')
        #                         doeData.doe_ResponseSet[index_i, index_j] = ReadLsDynaResultsFile().getOutputValueByParameters(valueDict)
        #                         #ReadandWriteTemplateConf().data_DOE.doe_ResponseSet[self.index_i, self.index_j] = 1+1
        #
        #             elif valueDict.get('fileType') == SolverFileTyeEnum.rwforc.value:
        #                 rwforcFilePath = folderPath + f'/rmpod_{index_i}/rwforc'
        #                 if os.path.exists(rwforcFilePath):
        #                     reader = ReadRwforcFile(rwforc_path=rwforcFilePath)
        #                     ReadandWriteTemplateConf().data_DOE.doe_ResponseSet[index_i, index_j] = \
        #                         reader.getOutputValueByParameters(valueDict)
        #
        #             elif valueDict.get('fileType') == SolverFileTyeEnum.multi.value:
        #                 newFolderPath = folderPath + f"/rmpod_{index_i}"
        #                 if os.path.exists(newFolderPath):
        #                     valueDict['xDataParams']['filePath'] = newFolderPath
        #                     valueDict['yDataParams']['filePath'] = newFolderPath
        #                     ReadandWriteTemplateConf().data_DOE.doe_ResponseSet[index_i, index_j] = \
        #                         ReadMultiResultFile().getOutputValueByParameters(valueDict)
        if solverType == SolverTypeEnum.LsDyna:
            thread = ReadResutsThread(solverType, folderPath, rowNum, colNum)
            thread.start()
            thread.wait()
        if solverType == SolverTypeEnum.Abaqus:
            fileName = ReadandWriteTemplateConf().data_Simulation.fileName
            global odbParing
            odbParing = ParsingODBFile()
            for index_i in range(rowNum):
                for index_j in range(colNum):
                    valueDict = FEResponseValue.get(doeData.doe_ResponseName[index_j])
                    if valueDict is None:
                        logging.getLogger().info("数据错误，程序需中止！")
                        return
                    if valueDict.get('fileType') == SolverFileTyeEnum.odb.value:
                        ODBFilePath = folderPath + f'/rmpod_{index_i}/{fileName}' + '.odb'
                        if os.path.exists(ODBFilePath):
                            valueDict['ODBPath'] = ODBFilePath
                            reaponseValue[index_i, index_j] = odbParing.getOutputValueByParameters(valueDict)
                        else:
                            logging.getLogger().error(f'未找到结果文件：{ODBFilePath}')
            doeData.doe_ResponseSet = reaponseValue  # 响应值数组
        finalTrainyData = np.hstack((doeData.doe_SampleSet, doeData.doe_ResponseSet))
        dataDF = pd.DataFrame(data=finalTrainyData)
        nameList = list(doeData.doe_VariablesValueRange.keys())
        nameList.extend(doeData.doe_ResponseName)
        dataDF.columns = nameList
        writer = pd.ExcelWriter(folderPath + '/TrainyData.xlsx')
        dataDF.to_excel(writer, 'Data')
        writer.save()
        writer.close()
        printGetInCurrentFunctionName(sys._getframe().f_code.co_name,
                                      inspect.getframeinfo(inspect.currentframe().f_back)[2],
                                      False)

class myTask(QObject):
    def __init__(self, solverType, folderPath, rowNum, colNum):
        super(myTask, self).__init__()
        self.threadpool = QThreadPool()
        self.threadpool.globalInstance()
        self.threadpool.setMaxThreadCount(1)
        self.solverType = solverType
        self.rowNum = rowNum
        self.colNum = colNum
        self.folderPath = folderPath

    def start(self):
        if self.solverType == SolverTypeEnum.LsDyna:
            for index_i in range(self.rowNum):
                for index_j in range(self.colNum):
                    # 检查计算得到的结果文件是否完整
                    fileLst = []
                    for path, dir, files in os.walk(self.folderPath+f'rmpod_{index_i}'):
                        fileLst += files
                    if fileLst != ReadandWriteTemplateConf().data_FECalcuFile.resultFileList:
                        logging.getLogger().info('此结果文件存在问题，无法解析结果：'+self.folderPath+f'rmpod_{index_i}')
                        continue
                    valueDict = ReadandWriteTemplateConf().data_FECalcuFile.responseValue.get(ReadandWriteTemplateConf().data_DOE.doe_ResponseName[index_j])
                    if valueDict is None:
                        logging.getLogger().info("数据错误，程序需中止！")
                        return
                    taskThread = Worker(valueDict.get('fileType'), self.folderPath, valueDict, index_i, index_j)
                    taskThread.setAutoDelete(True)
                    self.threadpool.start(taskThread)
            self.threadpool.waitForDone()

class Worker(QRunnable):
    def __init__(self, fileType, folderPath, params, index_i, index_j):
        super(Worker, self).__init__()
        self.fileType = fileType
        self.folderPath = folderPath
        self.params = params
        self.index_i = index_i
        self.index_j = index_j

    def run(self):
        if self.fileType == SolverFileTyeEnum.d3plot.value:
            d3plotFilePath = self.folderPath + f'rmpod_{self.index_i}/d3plot'
            d3plotFilePath.replace('/', '\\')
            print(f'------------------------------------------------------{d3plotFilePath}-----------------------------------------------------\n')
            if os.path.exists(d3plotFilePath):
                if ReadLsDynaResultsFile().loadResultFile(d3plotFilePath):
                    if isDebug:
                        print(
                            f'---------------------{datetime.datetime.now()},:正在解析的文件编号为{self.index_i}，{QThread.currentThreadId()}---------------------\n')
                    ReadandWriteTemplateConf().data_DOE.doe_ResponseSet[self.index_i, self.index_j] = \
                        ReadLsDynaResultsFile().getOutputValueByParameters(self.params)
                    #ReadandWriteTemplateConf().data_DOE.doe_ResponseSet[self.index_i, self.index_j] = 1+1

        elif self.fileType == SolverFileTyeEnum.rwforc.value:
            rwforcFilePath = self.folderPath + f'/rmpod_{self.index_i}/rwforc'
            if os.path.exists(rwforcFilePath):
                if ReadRwforcFile().praserFile(rwforcFilePath):
                    ReadandWriteTemplateConf().data_DOE.doe_ResponseSet[self.index_i, self.index_j] = \
                        ReadRwforcFile().getOutputValueByParameters(self.params)

        elif self.fileType == SolverFileTyeEnum.multi.value:
            newFolderPath = self.folderPath + f"/rmpod_{self.index_i}"
            if os.path.exists(newFolderPath):
                self.params['xDataParams']['filePath'] = newFolderPath
                self.params['yDataParams']['filePath'] = newFolderPath
                ReadandWriteTemplateConf().data_DOE.doe_ResponseSet[self.index_i, self.index_j] = \
                    ReadMultiResultFile().getOutputValueByParameters(self.params)

class ReadResutsThread(QThread):
    def __init__(self, solverType, folderPath, rowNum, colNum):
        super(ReadResutsThread, self).__init__()
        self.task = myTask(solverType, folderPath, rowNum, colNum)

    def run(self):
        self.task.start()
