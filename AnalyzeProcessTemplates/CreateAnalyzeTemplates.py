from AnalyzeProcessTemplates.Widget_AnalyseFlow import AnalyseFlowChat
from ui.main.widgets.procedures import TemplateNameEnum
from AnalyzeProcessTemplates.public import FeatureNodesEnum
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from CalculationProcess.CreateAnalyzeProcessFactory import BuildCalculateProcess
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt

class AnalyzeTemplate(AnalyseFlowChat):
    def __init__(self, parent):
        super(AnalyzeTemplate, self).__init__(parent)
        self.Btn_list = [] #存储模板按钮

    def chooseTemplate(self, templateName):
        if templateName == TemplateNameEnum.Template_doe.value:
            self.deoTemplate()
        elif templateName == TemplateNameEnum.Template_fit.value:
            self.fitTemplate()
        elif templateName == TemplateNameEnum.Template_sa.value:
            self.saTemplate()
        elif templateName == TemplateNameEnum.Template_opt.value:
            self.optTemplate()
        elif templateName == TemplateNameEnum.Template_opt_FE.value:
            self.optByFECalcuTemplate()
        elif templateName == TemplateNameEnum.Template_modify.value:
            pass
        elif templateName == TemplateNameEnum.Template_robust.value:
            pass
        ReadandWriteTemplateConf().usrChoosnTemplate = templateName


    def deoTemplate(self):
        tempfile = ReadandWriteTemplateConf()
        tempfile.getTemplateFromTotalTemplateByName("doe")
        # 在界面中画出节点图
        self.createNodeGraphByTemplateFile(tempfile)

        # 创建分析流程
        BuildCalculateProcess().BuildAnalyseProcess("doe")

    def fitTemplate(self):
        tempfile = ReadandWriteTemplateConf()
        tempfile.getTemplateFromTotalTemplateByName("fit")

        # 在界面中画出节点图
        self.createNodeGraphByTemplateFile(tempfile)

        # 创建分析流程
        BuildCalculateProcess().BuildAnalyseProcess("fit")

    def saTemplate(self):
        pass

    def optTemplate(self):
        tempfile = ReadandWriteTemplateConf()
        tempfile.getTemplateFromTotalTemplateByName("optimization")
        # 在界面中画出节点图
        self.createNodeGraphByTemplateFile(tempfile)
        # 创建分析流程
        BuildCalculateProcess().BuildAnalyseProcess("optimization")

    def optByFECalcuTemplate(self):
        tempfile = ReadandWriteTemplateConf()
        tempfile.getTemplateFromTotalTemplateByName("optimization_FECalcu")
        # 在界面中画出节点图
        self.createNodeGraphByTemplateFile(tempfile)
        # 创建分析流程
        BuildCalculateProcess().BuildAnalyseProcess("optimization_FECalcu")

    def modifyTemplate(self):
        pass

    def robustTemplate(self):
        pass

    def createNodeGraphByTemplateFile(self, templateFile):
        """根据配置文件中的节点，创建功能节点按钮，并创建连接线"""
        # 读取文件中的节点并创建按钮
        self.Btn_list.clear()
        points = []
        templateFile.getNewTemplateFileSubNodeName(points)
        for pointName in points:
            if list(pointName)[0] == "doe":
                Btn = self.CreatFeatureFunctionBtn(FeatureNodesEnum.doeBtn.value)
                self.Btn_list.append(Btn)
            if list(pointName)[0] == "dataInput":
                Btn = self.CreatFeatureFunctionBtn(FeatureNodesEnum.dataInputBtn.value)
                self.Btn_list.append(Btn)
            if list(pointName)[0] == "surrogateModel":
                Btn = self.CreatFeatureFunctionBtn(FeatureNodesEnum.fitBtn.value)
                self.Btn_list.append(Btn)
            if list(pointName)[0] == "optimizationAlgorithm":
                Btn = self.CreatFeatureFunctionBtn(FeatureNodesEnum.optBtn.value)
                self.Btn_list.append(Btn)
            if list(pointName)[0] == "FECalcuFile":
                Btn = self.CreatFeatureFunctionBtn(FeatureNodesEnum.FECalcuFileBtn.value)
                self.Btn_list.append(Btn)
            if list(pointName)[0] == "simulation":
                Btn = self.CreatFeatureFunctionBtn(FeatureNodesEnum.SimulationBtn.value)
                self.Btn_list.append(Btn)
            if list(pointName)[0] == "sensitiveAnalyse":
                Btn = self.CreatFeatureFunctionBtn(FeatureNodesEnum.saBtn.value)
                self.Btn_list.append(Btn)
        # 移动位置
        self.changeBtnAndConnectLinesPos()
        # 创建节点之间的连接线
        Btn_num = len(self.Btn_list)
        if Btn_num > 1:
            index = 1
            while index < Btn_num:
                self.CreateConnectLinesByTwoBtns(self.Btn_list[index - 1], self.Btn_list[index])
                index += 1

    def changeBtnAndConnectLinesPos(self):
        """移动按钮在UI的摆放位置"""
        widgetWidth = self.width() # 节点区域宽度
        widgetHeight = self.height() # 节点区域高度
        initWidth = 100
        tmpWidth = initWidth
        for btn in self.Btn_list:
            if tmpWidth + btn.width() <= widgetWidth:
                btn.move(tmpWidth, widgetHeight / 2 - btn.height() / 2)
                tmpWidth += btn.width() + initWidth
            else:
                tmpWidth = tmpWidth - btn.width() - initWidth
                btn.move(tmpWidth, widgetHeight / 2 + btn.height() / 2 + initWidth)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(QColor(98, 98, 98))
        painter.setPen(pen)
        # 计算网格尺寸
        rect = self.rect()
        xmin = rect.left() - rect.left() % self.gridSize - self.gridSize
        ymin = rect.left() - rect.top() % self.gridSize - self.gridSize
        xmax = rect.right() - rect.right() % self.gridSize + self.gridSize
        ymax = rect.bottom() - rect.bottom() % self.gridSize + self.gridSize
        tmpX = xmin
        while tmpX <= xmax:
            painter.drawLine(tmpX, rect.top(), tmpX, rect.bottom())
            tmpX += self.gridSize
        tmpY = ymin
        while tmpY <= ymax:
            painter.drawLine(rect.left(), tmpY, rect.right(), tmpY)
            tmpY += self.gridSize
        # 查看结果按钮
        self.Btn_ViewResults.move(self.width() - self.Btn_ViewResults.width() - 20, 20)