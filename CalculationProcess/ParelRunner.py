from PyQt5.QtCore import QObject
import os
import time
import logging
from AnalyzeProcessTemplates.public import SolverTypeEnum, isDebug, progressPercent
from PyQt5.QtCore import QThread, QRunnable, QThreadPool
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
import threading
import subprocess
from configFile.ReadTemplateConf import ReadandWriteTemplateConf

class ParelRunner(QObject):
    commucation = None
    def __init__(self, commucation, NCPU, NProcessor, strCMD, solverType, filePath, sampleNum):
        super(ParelRunner, self).__init__()
        self.commucation = commucation
        self.CMD = strCMD
        self.solverType = solverType
        self.NCPU = NCPU
        self.NProcessor = NProcessor
        self.dir = filePath
        self.sampleNum = sampleNum
        self.pool = QThreadPool()
        self.pool.globalInstance()
        ReadandWriteTemplateConf().ProgressBar_calculateCompeletedNum = 0
        ReadandWriteTemplateConf().ProgressBar_isAuto = False
        ReadandWriteTemplateConf().ProgressBar_curCalculateStep = f'{self.solverType.value}批量计算中...'
        # global progressPercent
        # progressPercent = 0

    def start(self):
        self.pool.setMaxThreadCount(self.NProcessor)
        self.runinDir()

    def runinDir(self):
        """
        获取需要执行的文件路径列表，并调用函数执行
        :param dir: 执行文件路径
        :return: 无
        """
        self.fileDirs = []
        subDirs = next(os.walk(self.dir))[1]
        for subDir in subDirs:
            if 'rmpod_' in subDir:
                if int(subDir.split('_')[1]) < int(self.sampleNum):
                    self.fileDirs.append(os.path.join(self.dir, subDir))

        for i in range(len(self.fileDirs)):
            commandLine = self.buildCMD(self.fileDirs[i])
            taskThread = thread()
            taskThread.initVariables(commandLine=commandLine, commucation=self.commucation, solverType=self.solverType, calDir=self.fileDirs[i])
            taskThread.setAutoDelete(True)
            self.pool.start(taskThread)
        self.pool.waitForDone()
        if isDebug:
            print("执行cmd完毕")

    def buildCMD(self, fileDir):
        """
        根据文件路径创建cmd命令
        :param fileDir: 文件路径
        :return: cmd命令
        """
        commandLine = self.CMD
        if self.solverType == SolverTypeEnum.LsDyna:
            # 文件路径
            posStart = commandLine.find('i=') + 2
            posEnd = commandLine.rfind('/')
            tmpcmd = commandLine[: posStart] + fileDir + commandLine[posEnd:]
            # CPU
            posStart = tmpcmd.find('ncpu=') + 5
            if posStart == -1:
                posStart = tmpcmd.find('-np ') + 4
            posEnd = tmpcmd[posStart:].find(' ')
            tmpcmd = tmpcmd[:posStart] + str(self.NCPU) + tmpcmd[posStart+posEnd:]
        elif self.solverType == SolverTypeEnum.Abaqus:
            tmpcmd = commandLine[:commandLine.find('job=') + 4] + commandLine[commandLine.rfind('/') + 1:]
        return tmpcmd

class myThread(QThread):
    def __init__(self, nCPU, filePath, commucation, nProcessor, cmd, solverType, sampleNum):
        super().__init__()
        print('ParelRunner')
        self.task = ParelRunner(NCPU=nCPU,
                                NProcessor=nProcessor,
                                strCMD=cmd,
                                solverType=solverType,
                                filePath=filePath,
                                commucation=commucation,
                                sampleNum=sampleNum)
    def run(self):
        self.task.start()

class thread(QRunnable):
    commucation = None

    def __init__(self):
        super(thread, self).__init__()
        self.thread_logo = None

    def initVariables(self, commandLine, commucation, solverType, calDir='/', repeatTimes=2, d3plotFileTarget=1):
        self.commandLine = commandLine
        self.solverType = solverType
        self.calDir = calDir
        self.repeatTimes = repeatTimes
        self.d3plotFileTarget = d3plotFileTarget
        self.commucation = commucation

    def run(self):
        self.exeCMDRepeat()

    def exeCMDRepeat(self):
        """
        循环执行有限元文件
        :return:
        """
        runTimes = 0
        if self.solverType == SolverTypeEnum.LsDyna:
            self.executeCMD()
            # num = self.calD3plotFileNumber()
            # while (num < self.d3plotFileTarget and runTimes < self.repeatTimes):
            #     self.clearFile()
            #
            #     num = self.calD3plotFileNumber()
            #     runTimes += 1
        elif self.solverType == SolverTypeEnum.Abaqus:
            self.executeAbaqus()

    def executeAbaqus(self):
        subprocess.run(self.commandLine, cwd=self.calDir, capture_output=False, shell=True)

    def executeCMD(self):
        """
        执行有限元仿真
        :param command: 命令cmd
        :param calDir: 执行文件路径
        :param repeatTime: 执行次数
        :return:
        """
        # loginfo = ["calculation start in %s" % threading.current_thread().name, self.calDir, self.commandLine,
        #            '\nrepeatTime: %d\n' % self.repeatTimes]
        # for item in loginfo:
        #     logging.getLogger().info(item)

        # os.chdir(self.calDir)
        subprocess.run(self.commandLine, cwd=self.calDir, capture_output=False, shell=True)
        # logging.getLogger().info(f"当前执行的文件路径：{self.calDir}")
        # os.system(self.commandLine)
        # loginfo = ["calculation finished in %s" % threading.current_thread().name, self.calDir, self.commandLine,
        #            '\nrepeatTime: %d\n' % self.repeatTimes]
        # for item in loginfo:
        #     logging.getLogger().info(item)
        # global progressPercent
        # progressPercent += 1
        ReadandWriteTemplateConf().ProgressBar_calculateCompeletedNum += 1
        if isDebug:
            logging.getLogger().info(f'cpmpeleted number:{ReadandWriteTemplateConf().ProgressBar_calculateCompeletedNum}')
        # self.commucation.CompeletedSignal.emit(str(curNum))

    def calD3plotFileNumber(self):
        """
        lsDyna求解器获取d3plot文件个数
        :return: d3plot文件个数
        """
        files = next(os.walk(self.calDir))[2]
        count = 0
        for file in files:
            if 'myD3plot' in file:
                count += 1
        return count

    def clearFile(self):
        """
        清除除计算文件外的所有文件
        :return: 无
        """
        files = next(os.walk(self.calDir))[2]
        # LSDYNA求解器 K文件
        if self.solverType == SolverTypeEnum.LsDyna:
            for file in files:
                if not file.endswith('.k'):
                    os.remove(os.path.join(self.calDir, file))