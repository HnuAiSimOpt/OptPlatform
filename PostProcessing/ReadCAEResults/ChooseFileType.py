from PostProcessing.ReadCAEResults.ui.Ui_ChooseFileType import Ui_ChooseResultFileType
from PyQt5.QtWidgets import QWidget
from PostProcessing.ReadCAEResults.DefineOutputByD3plotFile import DefineLsDynaOutput
from PostProcessing.ReadCAEResults.DefineOutputByRwforcFile import DefineOutputByRwforcFile
from PostProcessing.ReadCAEResults.DefineOutputByMultiFile import DefineOutputByMultiFile
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
import logging
from PyQt5.QtCore import Qt, pyqtSignal, QVariant
from PyQt5.QtWidgets import QComboBox, QListView, QPushButton
import os
from PublicTool.myPublicDialogBackground import myPublicDialogBackground
from PublicTool.myMaskWidget import myMaskWidget
from AnalyzeProcessTemplates.public import getBtnStyleString

class ChooseFileType(QWidget, Ui_ChooseResultFileType):
    msg = pyqtSignal(str)
    def __init__(self):
        super(ChooseFileType, self).__init__()
        self.setupUi(self)
        self.Btn_rwforc.clicked.connect(self.connectTo)
        self.Btn_d3plot.clicked.connect(self.connectTo)
        self.Btn_multiFile.clicked.connect(self.connectTo)
        for btn in self.findChildren(QPushButton):
            btn.setStyleSheet(getBtnStyleString())
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def connectTo(self):
        if self.sender() == self.Btn_d3plot:
            filePath = ReadandWriteTemplateConf().data_FECalcuFile.filePath
            pos = filePath.rfind(".")
            fileExtension = filePath[pos:]
            if fileExtension == '.k' or fileExtension == ".key":
                # lsdyna查找d3plot文件
                folderPath = filePath[:filePath.rfind('/')] + '/TryCalculation'
                d3plotFilePath = self.seekFile(folderPath, 'd3plot')
                if d3plotFilePath == None:
                    logging.getLogger().error(f"路径：{folderPath} 下未找到d3plot文件，请重新提交计算！")
                    self.close()
                    return
                self.widgetOutputDefine = DefineLsDynaOutput()
                self.mask = myMaskWidget(self.parent().parent().parent().parent())
                backgroundWidget = myPublicDialogBackground()
                backgroundWidget.setTitle('d3plot文件解析及响应值定义')
                backgroundWidget.setWidget(self.widgetOutputDefine)
                self.mask.layout().addWidget(backgroundWidget)
                self.mask.show()
                self.widgetOutputDefine.loadingFile(d3plotFilePath)
                self.widgetOutputDefine.defineOutputMsg.connect(self.msg.emit)
        elif self.sender() == self.Btn_rwforc:
            filePath = ReadandWriteTemplateConf().data_FECalcuFile.filePath
            pos = filePath.rfind(".")
            fileExtension = filePath[pos:]
            if fileExtension == '.k' or fileExtension == ".key":
                # 查找rwforc文件
                folderPath = filePath[:filePath.rfind('/')] + '/TryCalculation'
                rwforcFilePath = self.seekFile(folderPath, 'rwforc')
                if rwforcFilePath == None:
                    logging.getLogger().error(f"路径：{folderPath} 下未找到rwforc文件，请重新提交计算！")
                    self.close()
                    return
            self.widgetOutputDefine = DefineOutputByRwforcFile(rwforcFilePath)
            self.mask = myMaskWidget(self.parent().parent().parent().parent())
            backgroundWidget = myPublicDialogBackground()
            backgroundWidget.setTitle('rwforc文件解析及响应值定义')
            backgroundWidget.setWidget(self.widgetOutputDefine)
            self.mask.layout().addWidget(backgroundWidget)
            self.mask.show()
            self.widgetOutputDefine.msg.connect(self.msg.emit)
        elif self.sender() == self.Btn_multiFile:
            self.widgetOutputDefine = DefineOutputByMultiFile()
            self.mask = myMaskWidget(self.parent().parent().parent().parent())
            backgroundWidget = myPublicDialogBackground()
            backgroundWidget.setTitle('多文件解析及响应值定义')
            backgroundWidget.setWidget(self.widgetOutputDefine)
            self.mask.layout().addWidget(backgroundWidget)
            self.mask.show()
            self.widgetOutputDefine.msg.connect(self.msg.emit)
        parent = self.parent()
        while not isinstance(parent, myMaskWidget):
            parent = parent.parent()
        parent.hide()

    def seekFile(self, path, name):
        """
        查找指定文件
        :param path: 文件路径
        :param name: 需要查找的文件名
        :return: 文件地址
        """
        for root, dirs, files in os.walk(path):
            if name in files:
                return f"{path}/{name}"
        return None

    def close(self) -> bool:
        parent = self.parent()
        index = 0
        while (not isinstance(parent, myMaskWidget)) and index < 10:
            try:
                parent = parent.parent()
                index += 1
            except:
                pass
        parent.close()
