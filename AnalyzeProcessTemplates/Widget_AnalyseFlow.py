import sys
import datetime
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication
from PyQt5.QtCore import Qt
from AnalyzeProcessTemplates.Button_FunctionBtn import CustomizationFunctionBtn
from AnalyzeProcessTemplates.connect_lines import ConnectLines
from AnalyzeProcessTemplates.public import FeatureNodesEnum, isDebug, getBtnStyleString, maskProgress
from CalculationProcess.CreateAnalyzeProcessFactory import BuildCalculateProcess

class AnalyseFlowChat(QWidget):
    CheckedBtns = []
    CtrlPressed = False
    gridSize = 10
    def __init__(self, parent):
        super(AnalyseFlowChat, self).__init__(parent)
        self.__initData()
        self.__initUI()
        self.__initConnect()

    def __initData(self):
        self.Dict_ConnectLines = {}  # 用于存放功能节点之间的连接线 "objectName": ConnectLines
        self.Dict_DataInputFeatureBtn = {}  # 用于存放数据输入节点按钮 "objectName": CustomizationFunctionBtn
        self.Dict_DoeFeatureBtn = {}  # 用于存放实验设计节点按钮 "objectName": CustomizationFunctionBtn
        self.Dict_FitFeatureBtn = {}  # 用于存放建模节点按钮 "objectName": CustomizationFunctionBtn
        self.Dict_optFeatureBtn = {}
        self.Dict_saFeatureBtn = {}
        self.Dict_FECalcuFileBtn = {}
        self.Dict_SimulationBtn = {}
        self.BtnCollector = {}
        self.BtnCollector[FeatureNodesEnum.doeBtn.value] = self.Dict_DoeFeatureBtn
        self.BtnCollector[FeatureNodesEnum.fitBtn.value] = self.Dict_FitFeatureBtn
        self.BtnCollector[FeatureNodesEnum.optBtn.value] = self.Dict_optFeatureBtn
        self.BtnCollector[FeatureNodesEnum.dataInputBtn.value] = self.Dict_DataInputFeatureBtn
        self.BtnCollector[FeatureNodesEnum.saBtn.value] = self.Dict_saFeatureBtn
        self.BtnCollector[FeatureNodesEnum.FECalcuFileBtn.value] = self.Dict_FECalcuFileBtn
        self.BtnCollector[FeatureNodesEnum.SimulationBtn.value] = self.Dict_SimulationBtn

    def __initUI(self):
        self.Btn_ViewResults = QPushButton(self)
        self.Btn_ViewResults.setText("查看结果")
        self.Btn_ViewResults.setFixedSize(100, 50)
        self.Btn_ViewResults.setStyleSheet(getBtnStyleString())
        self.Btn_ViewResults.setHidden(True)
        self.setStyleSheet('QWidget{background-color:#555555;}')

    def __initConnect(self):
        BuildCalculateProcess().msg_CalculateComplete.connect(self.showViewResultsBtn)

    def CreatFeatureFunctionBtn(self, featureName):
        self.Btn = CustomizationFunctionBtn(120, 50, self)
        self.Btn.setBtnFeatureType(featureName)
        now_time = datetime.datetime.now()
        self.Btn.show()
        buttonObjectName = "Button_" + featureName + "_" + now_time.strftime("%Y%m%d%H%M%S")
        self.Btn.setObjectName(buttonObjectName)
        self.Btn.sendmsg.connect(self.saveCheckedButtonObjectName)
        self.Btn.sendmsg_ChangeConnectLine.connect(self.ChangeConnectLinesByBtnMoved)

        if featureName == FeatureNodesEnum.doeBtn.value:
            self.Dict_DoeFeatureBtn[buttonObjectName] = self.Btn
        elif featureName == FeatureNodesEnum.fitBtn.value:
            self.Dict_FitFeatureBtn[buttonObjectName] = self.Btn
        elif featureName == FeatureNodesEnum.dataInputBtn.value:
            self.Dict_DataInputFeatureBtn[buttonObjectName] = self.Btn
        elif featureName == FeatureNodesEnum.optBtn.value:
            self.Dict_optFeatureBtn[buttonObjectName] = self.Btn
        elif featureName == FeatureNodesEnum.FECalcuFileBtn.value:
            self.Dict_FECalcuFileBtn[buttonObjectName] = self.Btn
        elif featureName == FeatureNodesEnum.SimulationBtn.value:
            self.Dict_SimulationBtn[buttonObjectName] = self.Btn
        elif featureName == FeatureNodesEnum.saBtn.value:
            self.Dict_saFeatureBtn[buttonObjectName] = self.Btn

        return self.Btn

    def saveCheckedButtonObjectName(self, objectName):
        if self.CtrlPressed or len(self.CheckedBtns) == 0:
            self.CheckedBtns.append(objectName)
        else:
            self.CheckedBtns.clear()
            self.CheckedBtns.append(objectName)

        strList = objectName.split("_")
        if len(strList) == 3:
           widget_main = self.parent().parent().parent().parent().parent().parent().parent()
           widget_main.show_parameters_setting_table()
           promptString = ''
           if strList[1] == FeatureNodesEnum.FECalcuFileBtn.value:
               promptString = '计算文件：ABAQUS求解器对应.inp文件，LS-DYNA求解器对应.k文件；\n'
               promptString += '定义设计变量：鼠标选中的位置及字符串长度作为后续变量的替换规则；\n'
               promptString += '提交试计算：构造用于求解的cmd，包括求解器位置、批处理文件位置等；\n'
               promptString += '定义响应值：试计算完成后，根据需要在对应的结果文件中选取指定值作为模型的响应输出。'
           elif strList[1] == FeatureNodesEnum.doeBtn.value:
               promptString = '实验设计方法：默认为拉丁超立方采样，用户可自选；\n'
               promptString += '变量个数：用户自定义；\n'
               promptString += '变量名及取值范围：用户自定义；\n'
               promptString += '样本数量：默认值为 20*变量个数，用户可自定义。'
           elif strList[1] == FeatureNodesEnum.SimulationBtn.value:
               promptString = '求解器：根据输入文件自动识别，用户不可修改；\n'
               promptString += '进程数：用户根据电脑性能自定义；\n'
               promptString += 'NCPU：单进程使用CPU个数，用户自定义；\n'
               promptString += '文件路径：当前求解文件路径及后续过程文件存放位置，用户不可修改；\n'
               promptString += '提交计算的命令：与试计算时定义的cmd命令一致，软件自动填充，用户不可修改。'
           elif strList[1] == FeatureNodesEnum.fitBtn.value:
               promptString = '代理模型：默认为支持向量机，用户可自选；\n'
               promptString += '参数设置：代理模型参数设置，默认为网格穷尽搜索，用户可自定义；\n'
               promptString += '模型验证方法：默认为交叉验证，选择此方法时，须指定交叉验证折数；选择测试集验证时，须提前导入验证数据集。\n'
           elif strList[1] == FeatureNodesEnum.optBtn.value:
               promptString = '定义优化问题：定义优化目标、约束条件及变量取值范围；\n'
               promptString += '优化算法：用户自行选取优化算法，并确定算法相关参数。'
           elif strList[1] == FeatureNodesEnum.saBtn.value:
               promptString = '敏感性分析：研究数学模型输出中的不确定性如何被划分和分配到输入的不确定性的不同来源；\n'
               promptString += '分析方法：Morris、RSHDMR、Sobol；\n'
               promptString += '输出：一阶指标（单个输入对输出的贡献）；二阶指标（两个输入相互作用对输出的贡献）。'
           widget_main.setPromptWidgetText(promptString)

        for btn in self.findChildren(QPushButton):
            curObjName = btn.objectName()
            if curObjName.__contains__('Button_'):
                if curObjName == objectName:
                    btn.setBtnCheckedStyleSheet()
                else:
                    btn.setBtnFeatureType(btn.text())

        if isDebug:
            print("CheckedBtns", self.CheckedBtns)

    # 创建两个功能按钮之间的连接线
    def CreateFeatureBtnConnectionLines(self):
        Btn_1 = None
        Btn_2 = None
        if len(self.CheckedBtns) == 2 and self.CheckedBtns[0] != self.CheckedBtns[1]:
            for featureType in self.BtnCollector.keys():
                for objectname in self.BtnCollector[featureType]:
                    if objectname == self.CheckedBtns[0]:
                        Btn_1 = self.BtnCollector[featureType][objectname]
                    elif objectname == self.CheckedBtns[1]:
                        Btn_2 = self.BtnCollector[featureType][objectname]

        if isinstance(Btn_1, QPushButton) and isinstance(Btn_2, QPushButton):
            self.CreateConnectLinesByTwoBtns(Btn_1, Btn_2)

    def CreateConnectLinesByTwoBtns(self, startBtn, endBtn):
        self.connectLines = ConnectLines(startBtn.geometry(), endBtn.geometry(), self)
        self.connectLines.show()
        self.connectLines.setObjectName("ConnectLines_" + startBtn.objectName() + "_" + endBtn.objectName())
        self.Dict_ConnectLines[self.connectLines.objectName()] = [self.connectLines, startBtn.objectName(), endBtn.objectName()]

    def ChangeConnectLinesByBtnMoved(self, objectName):
        btn_1 = None
        btn_2 = None
        for value in self.Dict_ConnectLines.values():
            # 通过objectName 找到与之对应的连接线(value[1]是主节点obj， value[2]是从节点obj)
            if value[1] == objectName or value[2] == objectName:
                featureType_1 = value[1].split("_")[1]
                objName_1 = value[1]
                if featureType_1 in self.BtnCollector.keys():
                    btn_1 = self.BtnCollector[featureType_1][objName_1]
                    btn_1_obj = btn_1.objectName()

                featureType_2 = value[2].split("_")[1]
                objName_2 = value[2]
                if featureType_2 in self.BtnCollector.keys():
                    btn_2 = self.BtnCollector[featureType_2][objName_2]
                    btn_2_obj = btn_2.objectName()

            if isinstance(btn_1, QPushButton) and isinstance(btn_2, QPushButton):
                value[0].ChangeWidgetSize(btn_1.geometry(), btn_2.geometry())
                btn_1 = None
                btn_2 = None

    # 键盘响应
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Control:
            if not e.isAutoRepeat():
                self.CtrlPressed = True

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Control:
            self.CtrlPressed = False

    def showViewResultsBtn(self):
        self.Btn_ViewResults.show()
        self.Btn_ViewResults.move(self.width() - self.Btn_ViewResults.width() - 20, 20)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = AnalyseFlowChat(None)
    ex.show()
    app.exec_()