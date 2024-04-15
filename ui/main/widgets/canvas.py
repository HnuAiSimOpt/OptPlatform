# -*- coding: utf-8 -*-
import os
import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QDockWidget, QComboBox, QListView
from PyQt5.QtCore import QRect, Qt, pyqtSignal
from ui.main.raw.Ui_canvas import Ui_Canvas
from collections import deque
from AnalyzeProcessTemplates.CreateAnalyzeTemplates import AnalyzeTemplate
from PostProcessing.ResultsWidget import ResultsWidget
from AnalyzeProcessTemplates.public import getQLabelStyleSheet, getCanvasToolBtnStyleSheet
from PublicTool.myMaskWidget import myMaskWidget
from PublicTool.myPublicDialogBackground import myPublicDialogBackground

sys.path.append(os.getcwd())

class CanvasWidget(QWidget, Ui_Canvas):
    sizeChangedSignal = pyqtSignal()
    """画布界面"""
    def __init__(self, parent=None):
        """实例化一个画布窗口

        Args:
            parent ([type], optional): 父窗口. Defaults to None.
        """
        super(CanvasWidget, self).__init__(parent)

        self._OptPlatform = parent
        self.buffer = None  # 当前窗口的数据缓存器

        self.setupUi(self)
        self.__initUI__()
        self.__initConnect__()

    def __initUI__(self):
        self.splitter.setEnabled(True)
        self.splitter.setOpaqueResize(True)
        self.analyseFlowChat = AnalyzeTemplate(self.widget)
        self.widget.setStyleSheet('QWidget{background-color:#555555;}')
        self.label.setStyleSheet("QLabel{font-size:16px; font-family: 'Microsoft YaHei'; color: #ffffff; font-weight: bold; border:None;}")
        self.label_2.setStyleSheet("QLabel{font-size:16px; font-family: 'Microsoft YaHei'; color: #ffffff; font-weight: bold; border:None;}")
        self.widget_2.setStyleSheet('QWidget{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(81, 80, 81, 255), stop:1 rgba(48, 49, 49, 255));}')
        self.widget_3.setStyleSheet(
            'QWidget{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(81, 80, 81, 255), stop:1 rgba(48, 49, 49, 255));}')
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())
        # 给工具栏增加操作按钮
        self.ToolBtn_Connect.setGeometry(QRect(0, 0, 40, 40))

        #设置工具按钮的样式
        self.ToolBtn_SA.setStyleSheet(getCanvasToolBtnStyleSheet())
        self.ToolBtn_Connect.setStyleSheet(getCanvasToolBtnStyleSheet())
        self.ToolBtn_Activation.setStyleSheet(getCanvasToolBtnStyleSheet())
        self.ToolBtn_data.setStyleSheet(getCanvasToolBtnStyleSheet())
        self.ToolBtn_Delete.setStyleSheet(getCanvasToolBtnStyleSheet())
        self.ToolBtn_DOE.setStyleSheet(getCanvasToolBtnStyleSheet())
        self.ToolBtn_Forbiden.setStyleSheet(getCanvasToolBtnStyleSheet())
        self.ToolBtn_Modeling.setStyleSheet(getCanvasToolBtnStyleSheet())
        self.ToolBtn_Opt.setStyleSheet(getCanvasToolBtnStyleSheet())


    def __initConnect__(self):
        self.ToolBtn_Connect.clicked.connect(self.slotConnectFeatureBtnClicked)
        self.analyseFlowChat.Btn_ViewResults.clicked.connect(self.ViewResultsBtnClicked)

    # 创建模板
    def make_template(self, template_type):
        # 删除原来创建的节点和连接线
        self.removeUnwantedNodesAndConnectors()
        # 通过procedure_type创建对应的功能流程
        self.analyseFlowChat.chooseTemplate(template_type)

    # 创建新的模板之前，先删除目前已经创建的流程图中的节点和连接线
    def removeUnwantedNodesAndConnectors(self):
        for btn in self.analyseFlowChat.Dict_DataInputFeatureBtn.values():
            btn.deleteLater()
        for btn in self.analyseFlowChat.Dict_DoeFeatureBtn.values():
            btn.deleteLater()
        for btn in self.analyseFlowChat.Dict_FitFeatureBtn.values():
            btn.deleteLater()
        for btn in self.analyseFlowChat.Dict_optFeatureBtn.values():
            btn.deleteLater()
        for btn in self.analyseFlowChat.Dict_saFeatureBtn.values():
            btn.deleteLater()
        for btn in self.analyseFlowChat.Dict_FECalcuFileBtn.values():
            btn.deleteLater()
        for btn in self.analyseFlowChat.Dict_SimulationBtn.values():
            btn.deleteLater()
        for line in self.analyseFlowChat.Dict_ConnectLines.values():
            line[0].setParent(None)
            self.layout().removeWidget(line[0])

        self.analyseFlowChat.Dict_DataInputFeatureBtn.clear()
        self.analyseFlowChat.Dict_DoeFeatureBtn.clear()
        self.analyseFlowChat.Dict_FitFeatureBtn.clear()
        self.analyseFlowChat.Dict_optFeatureBtn.clear()
        self.analyseFlowChat.Dict_saFeatureBtn.clear()
        self.analyseFlowChat.Dict_FECalcuFileBtn.clear()
        self.analyseFlowChat.Dict_ConnectLines.clear()
        self.analyseFlowChat.Dict_SimulationBtn.clear()

    def paintEvent(self, e):
        if self.analyseFlowChat is not None:
            self.analyseFlowChat.setGeometry(QRect(0, 0, self.widget.width(), self.widget.height()))

    # 槽函数
    def slotConnectFeatureBtnClicked(self):
        self.analyseFlowChat.CreateFeatureBtnConnectionLines()

    def ViewResultsBtnClicked(self):
        try:
            results = ResultsWidget()
        except:
            return
        self.mask = myMaskWidget(self.parent().parent().parent())
        backgroundWidget = myPublicDialogBackground()
        backgroundWidget.setTitle('查看结果')
        backgroundWidget.setWidget(results, False)
        self.mask.layout().addWidget(backgroundWidget)
        self.mask.show()

    def resizeEvent(self, e) -> None:
        self.sizeChangedSignal.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CanvasWidget()
    ex.show()
    app.exec_()


