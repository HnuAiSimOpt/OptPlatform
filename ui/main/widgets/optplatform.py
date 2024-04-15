import logging
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtWidgets
from ui.main.raw.Ui_OptPlatform import Ui_OptPlatform
from ui.main.widgets.add_proj import AddProj
from ui.main.widgets.canvas import CanvasWidget
from ui.main.widgets.procedures import SelectMode, TemplateNameEnum
from utils.database import *
from utils.logit import TextBrowserLogger
from ui.paraSetting.ParametersSettingDataInput import DataInputParamSetting
from ui.paraSetting.ParametersSettingSurrogateModel import SurrogateModelParamSetting
from ui.paraSetting.ParametersSettingOptimization import OptimizationAlgorithmParamSetting
from ui.paraSetting.ParametersSettingFECalculationFile import FECalcuFileParamSetting
from ui.paraSetting.ParametersSettingSensitiveAnalyse import SensitiveAnalyseParamSetting
from ui.paraSetting.ParametersSettingDOE import DOEParamSetting
from configFile.ReadTemplateConf import *
from CalculationProcess.CreateAnalyzeProcessFactory import BuildCalculateProcess
from ui.main.widgets.createProj import CreateProj
import closeApp
from ui.paraSetting.ParametersSettingSimulation import SimulationParamSetting
from PublicTool.myMaskWidget import myMaskWidget
from PublicTool.myPublicDialogBackground import myPublicDialogBackground
from AnalyzeProcessTemplates.public import *
from PublicTool.myMessageDialog import *

class OptPlatform(QMainWindow, Ui_OptPlatform):
    """basic ui

    Args:
        QMainWindow (widgets): qt mainwindow widgets
        Ui_Optplatform (_type_): compliled ui filed
    """
    sizeChangedSignal = QtCore.pyqtSignal()
    def __init__(self) -> None:
        super(OptPlatform, self).__init__()
        self.database = Database
        self.maskProgress = None
        self.logger = []
        self.setupUi(self)
        self.__correct_ui()
        self.__init_signals()

    def __correct_ui(self):
        """将默认的UI界面按实际需要情况修正显示"""
        self.resize(QtCore.QSize(1600, 900))
        self.button_feedback = QToolButton()
        self.button_feedback.setIcon(QIcon(":/pic/icons/用户反馈.png"))
        self.button_feedback.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.button_feedback.setStyleSheet("border-style: flat")
        self.button_feedback.setCursor(Qt.CursorShape.PointingHandCursor)
        menu = QMenu()
        self.action_bug = QtWidgets.QAction(QIcon(":/pic/icons/bug.png"), "提交Bug", self)
        self.action_user = QtWidgets.QAction(QIcon(":/pic/icons/笑脸.png"), "反馈用户体验", self)
        menu.addAction(self.action_bug)
        menu.addAction(self.action_user)
        self.button_feedback.setMenu(menu)
        self.statusBar().showMessage("欢迎使用OptPlatform")
        self.statusBar().addPermanentWidget(self.button_feedback)
        # self.statusBar().setStyleSheet("QStatusBar::item{border: 0px}")

        # 生成创建新项目界面
        self.createProj_widget = CreateProj(self.widget_main)
        horiLayout = QHBoxLayout()
        horiLayout.addWidget(self.createProj_widget)
        horiLayout.setSpacing(0)
        self.widget_main.setLayout(horiLayout)
        self.createProj_widget.Btn_CreateNewProj.clicked.connect(self.add_setup_widget)
        self.createProj_widget.Btn_CreateNewProj_icon.clicked.connect(self.add_setup_widget)

        for btn in self.createProj_widget.findChildren(QPushButton):
            btn.setStyleSheet('QPushButton{background-color:transparent;}'
                              'QPushButton:hover{color: #a4d188;}')

        # 隐藏参数设置和提示框
        self.dockWidget_paramSetting.setHidden(True)
        self.dockWidget_prompt.setHidden(True)

        self.dockWidget_prompt.setWindowTitle('功能说明')
        self.dockWidget_paramSetting.setWindowTitle('参数设置')
        self.initPromptDockWidget()
        self.menubar.setFixedHeight(26)
        self.toolBar.setFixedHeight(60)
        self.toolBar.removeAction(self.action_close_proj)
        self.toolBar.removeAction(self.action_open_proj)
        self.toolBar.setIconSize(QtCore.QSize(35, 35))
        self.toolBar.setFixedHeight(66)
        self.toolBar.setStyleSheet('QToolBar{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(100, 99, 100, 255), stop:1 rgba(48, 49, 48, 255));}')
        self.toolBar.layout().setSpacing(20)

        self.dockWidget_prompt.setAutoFillBackground(True)
        self.dockWidget_paramSetting.setAutoFillBackground(True)


        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def __init_signals(self):
        """初始化所有信号"""
        self.action_add_new.triggered.connect(self.add_setup_widget)
        self.action_select_mode.triggered.connect(self.select_mode)
        self.action_apply.triggered.connect(self.action_operation)

    def add_setup_widget(self):
        """添加初始的项目界面

        新建项目，初始化界面。#TODO: 生成项目所需的系统文件，用户文件等
        """
        add_new = AddProj(self)
        self.mask = myMaskWidget(self)
        backgroundWidget = myPublicDialogBackground()
        backgroundWidget.setTitle('新建项目')
        backgroundWidget.setWidget(add_new, True)
        self.mask.layout().addWidget(backgroundWidget)
        self.mask.show()
        reply = add_new.exec_()
        if reply:
            proj_label = add_new.lineEdit.text()
            workdir = add_new.comboBox.currentText()
            # 生成工作目录
            proj_dir = workdir + "/" + proj_label
            
            if not os.path.exists(proj_dir):
                os.makedirs(proj_dir)
                os.makedirs(proj_dir + "/" + "modules/" + "setup")
                os.makedirs(proj_dir + "/" + "_mod_settings")
                reply = 16384  # 就是QMessageBox.Yes的int值， 2^14
            else:
                myMessage = myMessageDialog(MessageType.Ask, "当前工作目录已存在, 可能覆盖原有项目, 是否继续？")
                self.mask_message = myMaskWidget(self)
                backgroundWidget_message = myPublicDialogBackground()
                backgroundWidget_message.setTitle(MessageType.Ask.value)
                backgroundWidget_message.setWidget(myMessage, True)
                self.mask_message.layout().addWidget(backgroundWidget_message)
                self.mask_message.show()
                reply = myMessage.exec_()
                if reply:
                    itemlist = list(range(self.widget_main.layout().count()))
                    itemlist.reverse()
                    for i in itemlist:
                        item = self.widget_main.layout().itemAt(i)
                        self.widget_main.layout().removeItem(item)
                        if item is not None:
                            if item.widget():
                                item.widget().deleteLater()
                    # self.widget_main.setStyleSheet("background-color: rgb(57, 57, 57);")
                    # 生成主交互窗口
                    self.canvas_widget = CanvasWidget(self.widget_main)
                    self.widget_main.layout().addWidget(self.canvas_widget)
                    self.widget_main.layout().setSpacing(0)
                    self.widget_main.layout().setContentsMargins(0, 0, 0, 0)
                    self.canvas_widget.setEnabled(True)
                    # 显示参数设置与提示框
                    self.dockWidget_paramSetting.setHidden(False)
                    self.dockWidget_prompt.setHidden(False)
                    # 生成数据
                    self.database = Database(proj_dir, None, self)
                    # 界面调整
                    self.action_model_tree.setChecked(True)
                    self.action_message_log.setChecked(True)
                    self.action_save.setEnabled(True)
                    self.action_save_as.setEnabled(True)
                    self.action_select_mode.setEnabled(True)
                    self.action_apply.setEnabled(True)
                    self.action_last.setEnabled(True)
                    self.action_next.setEnabled(True)
                    self.action_close.setEnabled(True)
                    # QModelIndex不能单独使用，只能通过View或QStandardModel获取, index(row, column, parent=QModelIndex())
                    self.logger.append(TextBrowserLogger(self.canvas_widget, proj_dir + "/log.log"))
                    logging.getLogger().info("生成项目: {} 成功, 路径: {}".format(proj_label, proj_dir))
                    self.statusBar().showMessage("请选择工作模板")
                self.mask_message.close()
        else:
            pass
        add_new.deleteLater()
        self.mask.close()
    
    def select_mode(self):
        """
        选择工作模板(doe fit opt sa robust modify)
        """
        select_mode = SelectMode(self)
        self.mask = myMaskWidget(self)
        backgroundWidget = myPublicDialogBackground()
        backgroundWidget.setTitle('选择工作模板')
        backgroundWidget.setWidget(select_mode, True)
        self.mask.layout().addWidget(backgroundWidget)
        self.mask.show()
        select_mode.msg.connect(self.slotSelectMode)
        reply = select_mode.exec_()
        if reply:
            print('正在更换模板。')
            self.mask.close()

    def slotSelectMode(self, templateName):
        self.canvas_widget.setEnabled(True)
        # make node database from template
        if templateName in TemplateNameEnum._value2member_map_:
            # 删除现有数据
            ReadandWriteTemplateConf().data_DataInput.clear()
            ReadandWriteTemplateConf().data_OptimizationAlgorithm.clear()
            ReadandWriteTemplateConf().data_SurrogateModel.clear()
            ReadandWriteTemplateConf().data_DOE.clear()
            ReadandWriteTemplateConf().data_FECalcuFile.clear()
            if templateName == TemplateNameEnum.Template_modify:
                self.canvas_widget.make_modify()
            else:
                self.canvas_widget.make_template(templateName)

    
    def action_operation(self):
        """工具栏中的“主要操作按钮”的操作定义
        
        包括导入、应用以及运行的不同身份，在不同界面下执行不同的功能
        """
        mythread = threading.Thread(target=BuildCalculateProcess().Run)
        mythread.start()
        BuildCalculateProcess().msg_CalculateComplete.connect(self.closeMaskProgress)
        self.maskProgress = myMaskWidget(self, True, False)
        self.maskProgress.show()

    def closeMaskProgress(self):
        if self.maskProgress is not None:
            self.maskProgress.close()

    def show_parameters_setting_table(self):
        """ 参数设置 """
        # 删除现有表格
        if self.dockWidgetContents_param.layout() is not None:
            itemlist = list(range(self.dockWidgetContents_param.layout().count()))
            itemlist.reverse()
            for i in itemlist:
                item = self.dockWidgetContents_param.layout().itemAt(i)
                self.dockWidgetContents_param.layout().removeItem(item)
                if item is not None:
                    if item.widget():
                        item.widget().deleteLater()

        # 新建一个表格
        if self.dockWidgetContents_param.layout() is not None:
            horiLyout = self.dockWidgetContents_param.layout()
        else:
            horiLyout = QHBoxLayout()
        tmplist = self.sender().objectName().split("_")
        if len(tmplist) != 3:
            return
        if tmplist[1] == FeatureNodesEnum.dataInputBtn.value:
            horiLyout.addWidget(DataInputParamSetting(self.dockWidgetContents_param))
        elif tmplist[1] == FeatureNodesEnum.saBtn.value:
            horiLyout.addWidget(SensitiveAnalyseParamSetting(self.dockWidgetContents_param))
        elif tmplist[1] == FeatureNodesEnum.fitBtn.value:
            horiLyout.addWidget(SurrogateModelParamSetting(self.dockWidgetContents_param))
        elif tmplist[1] == FeatureNodesEnum.optBtn.value:
            horiLyout.addWidget(OptimizationAlgorithmParamSetting(self.dockWidgetContents_param))
        elif tmplist[1] == FeatureNodesEnum.FECalcuFileBtn.value:
            horiLyout.addWidget(FECalcuFileParamSetting(self.dockWidgetContents_param))
        elif tmplist[1] == FeatureNodesEnum.doeBtn.value:
            horiLyout.addWidget(DOEParamSetting(self.dockWidgetContents_param))
        elif tmplist[1] == FeatureNodesEnum.SimulationBtn.value:
            horiLyout.addWidget(SimulationParamSetting(self.dockWidgetContents_param))

        if self.dockWidgetContents_param.layout() is None:
            self.dockWidgetContents_param.setLayout(horiLyout)
            self.dockWidgetContents_param.setMinimumWidth(300)
            horiLyout.setContentsMargins(0, 0, 0, 0)

    def initPromptDockWidget(self):
        """
        初始化：功能说明
        :return:
        """
        if self.dockWidgetContents_prompt.layout() is not None:
            itemlist = list(range(self.dockWidgetContents_prompt.layout().count()))
            itemlist.reverse()
            for i in itemlist:
                item = self.dockWidgetContents_prompt.layout().itemAt(i)
                self.dockWidgetContents_prompt.layout().removeItem(item)
                if item is not None:
                    if item.widget():
                        item.widget().deleteLater()
        if self.dockWidgetContents_prompt.layout() is not None:
            horiLyout = self.dockWidgetContents_prompt.layout()
        else:
            horiLyout = QHBoxLayout()
        self.promptTextEdit = QTextEdit(self.dockWidgetContents_prompt)
        self.promptTextEdit.setStyleSheet('QTextEdit{background-color:transparent; border: 1px solid #f4f6e0}')
        horiLyout.addWidget(self.promptTextEdit)
        horiLyout.setContentsMargins(0, 0, 0, 0)
        self.dockWidgetContents_prompt.setLayout(horiLyout)

    def setPromptWidgetText(self, promptStr:str):
        """
        向功能说明窗口添加字符串
        :param promptStr:
        :return:
        """
        self.initPromptDockWidget()
        self.promptTextEdit.setText(promptStr)
        doc = self.promptTextEdit.document()
        textCursor = self.promptTextEdit.textCursor()
        curDoc = doc.begin()
        while curDoc != doc.end():
            blockFormat = curDoc.blockFormat()
            blockFormat.setLineHeight(8, QTextBlockFormat.LineDistanceHeight)
            textCursor.setPosition(curDoc.position())
            textCursor.setBlockFormat(blockFormat)
            self.promptTextEdit.setTextCursor(textCursor)
            # 更改样式
            textCursor.setPosition(curDoc.position())
            textLength = curDoc.text().find('：')
            cursorOpe = QTextCursor.Right
            textCursor.movePosition(cursorOpe, QTextCursor.KeepAnchor, textLength)
            self.changeTextEditSpecialStringStyle(textCursor)
            curDoc = curDoc.next()

    def changeTextEditSpecialStringStyle(self, cursor):
        """设定指定字符串样式"""
        tcf = QTextCharFormat()
        tcf.setForeground(QColor(164, 209, 136))
        tcf.setFont(QFont("Times", 12, QFont.Bold))
        tcf.setFontItalic(True)
        cursor.setCharFormat(tcf)

    def closeEvent(self, e) -> None:
        close = closeApp.closeApp(self)
        isClose = close.slotCloseAppBtnClicked()
        if isClose == True:
            e.accept()
        else:
            e.ignore()

    def resizeEvent(self, e) -> None:
        self.sizeChangedSignal.emit()

    def showEvent(self, e):
        self.dockWidgetContents_prompt.setMinimumHeight(self.widget_main.height() * 0.3)