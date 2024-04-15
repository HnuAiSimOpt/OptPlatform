from PostProcessing.ReadCAEResults.ui.Ui_SubmitCalculation import Ui_SubmitCalculation
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
import sys
import os
import psutil
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QComboBox, QListView
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from AnalyzeProcessTemplates.public import SolverTypeEnum
from FiniteElementCalculationFileProcessing.GenerateCalculationFile import *
import random
import logging
import threading
from PublicTool.myMaskWidget import myMaskWidget
from AnalyzeProcessTemplates.public import isDebug, getBtnStyleString
from itertools import groupby

class SubmitCalculation(QWidget, Ui_SubmitCalculation):
    calcuCompeleteMsg = pyqtSignal()
    sizeChangedSignal = pyqtSignal()
    def __init__(self, strFilePath):
        super(SubmitCalculation, self).__init__()
        self.setupUi(self)
        self.__initConnect__()
        self.__initUI__(strFilePath)

    def __initConnect__(self):
        self.Btn_findSolver.clicked.connect(self.getDir)
        self.Btn_findBat.clicked.connect(self.getDir)
        self.lineEdit_filePath.textChanged.connect(self.changeCMD)
        self.cbB_batPath.currentTextChanged.connect(self.changeCMD)
        self.cbB_solverPath.currentTextChanged.connect(self.changeCMD)
        self.CBb_NCPU.currentTextChanged.connect(self.changeCMD)
        self.CBb_MEMORY.currentTextChanged.connect(self.changeCMD)
        self.rBtn_inputCmd.clicked.connect(self.setCMDTextEditEnable)
        self.Btn_submit.clicked.connect(self.doCalculate)
        self.Btn_cancel.clicked.connect(self.slotBtnCancelClicked)

    def __initUI__(self, strFilePath):
        # 从文件后缀判断求解器类型
        suffix = strFilePath[strFilePath.rfind('.') + 1:]
        if suffix == 'k' or suffix == 'K':
            ReadandWriteTemplateConf().data_Simulation.solver = SolverTypeEnum.LsDyna
            self.solverType = SolverTypeEnum.LsDyna
            self.setDefaultBatPath()
            self.setDefaultSolverPath()
            self.setMemoryCBBNum()
        elif suffix == 'inp':
            ReadandWriteTemplateConf().data_Simulation.solver = SolverTypeEnum.Abaqus
            self.solverType = SolverTypeEnum.Abaqus
            self.cbB_batPath.setEnabled(False)
            self.cbB_solverPath.setEnabled(False)
            self.Btn_findBat.setEnabled(False)
            self.Btn_findSolver.setEnabled(False)
        else:
            logging.getLogger().info("暂不支持该文件的求解，请联系开发人员。")
            self.Btn_submit.setEnabled(False)
            return

        self.setCPUCBBNum()
        # 文件路径
        self.lineEdit_filePath.setText(strFilePath)
        # 设置文本框不可编辑
        self.textEdit_cmd.setEnabled(False)
        self.Btn_cancel.setStyleSheet(getBtnStyleString())
        self.Btn_submit.setStyleSheet(getBtnStyleString())
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def setCPUCBBNum(self):
        # CPU数
        totalCPU_1 = psutil.cpu_count(logical=False)  # 物理CPU个数
        totalCPU_2 = psutil.cpu_count()  # 逻辑CPU个数
        CPUList = range(2, totalCPU_1, 2)
        self.CBb_NCPU.addItem("1")
        for i in CPUList:
            self.CBb_NCPU.addItem(f"{i}")
        self.CBb_NCPU.addItem(f"{totalCPU_1}")

    def setMemoryCBBNum(self):
        # 物理内存
        aaa = psutil.virtual_memory().free/1024/1024/1024
        self.CBb_MEMORY.addItem("20m")
        self.CBb_MEMORY.addItem("100m")
        self.CBb_MEMORY.addItem("200m")
        self.CBb_MEMORY.addItem("400m")

    def setDefaultBatPath(self):
        self.cbB_batPath.addItem(
            "D:\\SoftwareInstall\\ANSYS Inc\\v221\\ansys\\bin\\winx64\\lsprepost47\\lsdynaintelvar.bat")
        self.cbB_batPath.addItem(
            "D:\software\\anasys2022\\ANSYS Inc\\v221\\ansys\\bin\winx64\\lsprepost47\\lsdynaintelvar.bat")

    def setDefaultSolverPath(self):
        self.cbB_solverPath.addItem("D:\\SoftwareInstall\\ANSYS Inc\\v221\\ansys\\bin\winx64\\lsdyna_sp.exe")
        self.cbB_solverPath.addItem("D:\\software\\anasys2022\\ANSYS Inc\\v221\\ansys\\bin\\winx64\\lsdyna_sp.exe")

    def getDir(self):
        dir = QFileDialog.getOpenFileName(self,  "选取文件", os.getcwd(), "All Files (*)") # 设置文件扩展名过滤,用双分号间隔
        if dir[0]:
            if self.sender() == self.Btn_findSolver:
                self.cbB_solverPath.insertItem(0, dir[0])
                self.cbB_solverPath.setCurrentIndex(0)
            elif self.sender() == self.Btn_findBat:
                self.cbB_batPath.insertItem(0, dir[0])
                self.cbB_batPath.setCurrentIndex(0)

    def doCalculate(self):
        """根据用户设置的变量范围生成新的计算文件，并提交计算"""
        # 生成遮罩，提示正在进行计算
        ReadandWriteTemplateConf().ProgressBar_curCalculateStep = '计算中，请等待...'
        self.progressBar = myMaskWidget(self, True)
        self.progressBar.show()
        # 生成新的计算文件
        FEData = ReadandWriteTemplateConf().data_FECalcuFile
        variable = FEData.designVariable
        designVariablePosition = FEData.getVariablePosList()
        variableLength = FEData.getVariableLength()
        decimalList = FEData.getVariableDecimal()
        isSciNotation = FEData.getIsScientificNotation()
        tmpData = np.zeros(len(designVariablePosition))
        index = 0
        for key, value in variable.items():
            tmpData[index] = random.uniform(value[0][0], value[0][1])
            index += 1
        GenerateCalcuFile.replaceVariableValue(tmpData, designVariablePosition,
                                  variableLength, decimalList, isSciNotation)
        # try:
        #     GenerateCalcuFile.GenerateCalcuFile(0, 'TryCalculation')
        # except:
        #     self.progressBar.close()
        #     logging.getLogger().error("无法正常创建试计算文件及文件夹（TryCalculation），提交试计算失败。")
        #     return
        #提交计算
        mythread = threading.Thread(target=self.execCMD)
        mythread.start()

    def execCMD(self):
        # 提交计算
        cmd = self.textEdit_cmd.toPlainText()
        filedir = self.lineEdit_filePath.text()
        pos = filedir.rfind("/")
        if pos == -1:
            pos = filedir.rfind("\\")
        newPath = filedir[:pos] + '/TryCalculation'
        if self.solverType == SolverTypeEnum.LsDyna:
            tmpcmd = cmd.replace(filedir[:pos], newPath)
        elif self.solverType == SolverTypeEnum.Abaqus:
            tmpcmd = cmd.replace(filedir[:pos + 1], '')
        os.chdir(newPath)
        # os.system(tmpcmd)
        # if isDebug:
        #     print("计算完成")
        logging.getLogger().info('试计算运行结束')

        # 将仿真相关参数存储
        ReadandWriteTemplateConf().data_Simulation.cmd = cmd
        filepath = ReadandWriteTemplateConf().data_FECalcuFile.filePath
        fileNamePos = filepath.rfind('/') + 1
        ReadandWriteTemplateConf().data_Simulation.folderPath = filepath[:fileNamePos]
        # 存储试计算文件夹中的结果文件列表
        fileLst = []
        for path, dir, files in os.walk(newPath):
            fileLst += files
        ReadandWriteTemplateConf().data_FECalcuFile.resultFileList = fileLst

        self.calcuCompeleteMsg.emit()
        self.progressBar.close()
        self.parent().parent().parent().close()


    def changeCMD(self):
        batPath = self.cbB_batPath.currentText()
        filePath = self.lineEdit_filePath.text()
        solverPath = self.cbB_solverPath.currentText()
        ncpu = self.CBb_NCPU.currentText()
        memory = self.CBb_MEMORY.currentText()
        if self.solverType == SolverTypeEnum.LsDyna:
            if batPath != -1:
                cmd = f"call \"{batPath}\" && \"{solverPath}\" i={filePath} ncpu={ncpu} memory={memory}"
            else:
                cmd = f"\"{solverPath}\" i={filePath} ncpu={ncpu} memory={memory}"
        elif self.solverType == SolverTypeEnum.Abaqus:
            jobName = filePath[:filePath.rfind('.')]
            cmd = f'abaqus cpus={ncpu} job={jobName} int'
        self.textEdit_cmd.clear()
        self.textEdit_cmd.append(cmd)
        ReadandWriteTemplateConf().data_Simulation.NCPU = ncpu

    def setCMDTextEditEnable(self):
        if self.rBtn_inputCmd.isChecked():
            self.textEdit_cmd.setEnabled(True)
        else:
            self.textEdit_cmd.setEnabled(False)

    def slotBtnCancelClicked(self):
        self.parent().parent().parent().close()

    def resizeEvent(self, e) -> None:
        self.sizeChangedSignal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SubmitCalculation("D:\\优化平台项目\\opt_platform\\temp\\ls-dyna\\1\\1.k")
    ex.show()
    app.exec_()