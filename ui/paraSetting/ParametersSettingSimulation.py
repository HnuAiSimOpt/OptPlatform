from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QTableWidget, QHBoxLayout, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from configFile.ReadTemplateConf import *
from ReadingData.ExcelFileReading import *
from ui.paraSetting.myTableWidget import *
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
import psutil

class SimulationParamSetting(myTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.__initUI__()

    def __initUI__(self):
        data = ReadandWriteTemplateConf().data_Simulation
        self.setRowCount(7)
        self.setColumnCount(2)
        self.setMyItem(0, 0, "求解器", False)
        self.setMyItem(0, 1, data.solver.value)
        self.setMyItem(1, 0, "进程数", False)
        self.cell = self.setQLineEditCellWidget(data.NProcessor)
        self.setCellWidget(1, 1, self.cell)
        self.cell.setText(str(ReadandWriteTemplateConf().data_Simulation.NProcessor))
        self.cell.editingFinished.connect(self.__slotCellWidgetChanged)
        self.setMyItem(2, 0, "NCPU", False)
        totalCPU_1 = psutil.cpu_count(logical=False)  # 物理CPU个数
        CPUList = list(range(2, totalCPU_1, 2))
        CPUList.insert(0, 1)
        CPUList.append(totalCPU_1)
        CPUList = [str(i) for i in CPUList]
        combox = self.setQcomboBoxCellWidget(CPUList)
        self.setCellWidget(2, 1, combox)
        combox.setCurrentText(str(ReadandWriteTemplateConf().data_Simulation.NCPU))
        combox.currentTextChanged.connect(self.__slotCellWidgetChanged)
        self.setMyItem(3, 0, "文件路径", False)
        self.setMyItem(3, 1, data.folderPath, False)
        self.setSpan(4, 0, 3, 2)
        self.setMyItem(4, 0, f"提交计算的命令：{data.cmd}", False)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(self.itemHeight)
        self.horizontalHeader().setStretchLastSection(True)

    def __slotCellWidgetChanged(self):
        sender = self.sender()
        if sender.objectName() == "lineEdit":
            nProcessor = self.sender().text()
            ReadandWriteTemplateConf().data_Simulation.NProcessor = int(nProcessor)
        elif isinstance(sender, QComboBox):
            NCPU = self.sender().currentText()
            ReadandWriteTemplateConf().data_Simulation.NCPU = int(NCPU)
            self.__changeCMD(NCPU)
            strcmd = ReadandWriteTemplateConf().data_Simulation.cmd
            self.item(4, 0).setText(f"提交计算的命令：{strcmd}")

    def __changeCMD(self, NCPU):
        """
        NCPU变化，更改命令
        :param NCPU:
        :return:
        """
        data = ReadandWriteTemplateConf().data_Simulation
        if data.cmd == '':
            return
        if data.solver == SolverTypeEnum.LsDyna:
            commandLine = data.cmd
            posStart = commandLine.find('ncpu=') + 5
            if posStart == -1:
                posStart = commandLine.find('-np ') + 4
            posEnd = commandLine[posStart:].find(' ')
            data.cmd = commandLine[:posStart] + NCPU + commandLine[posStart + posEnd:]