from PyQt5.QtWidgets import QMessageBox, QWidget
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
import os
from PublicTool.myMaskWidget import myMaskWidget
from PublicTool.myMessageDialog import *
from PublicTool.myPublicDialogBackground import myPublicDialogBackground

class closeApp(QWidget):
    def __init__(self, parent=None):
        super(closeApp, self).__init__()
        self.parentWidget = parent

    def clearData(self):
        ReadandWriteTemplateConf().data_DOE.clear()
        ReadandWriteTemplateConf().data_FECalcuFile.clear()
        ReadandWriteTemplateConf().data_DataInput.clear()
        ReadandWriteTemplateConf().data_SurrogateModel.clear()
        ReadandWriteTemplateConf().data_OptimizationAlgorithm.clear()

    def slotCloseAppBtnClicked(self):
        myMessage = myMessageDialog(MessageType.Ask, "确定关闭软件吗？")
        self.mask_message = myMaskWidget(self.parentWidget)
        backgroundWidget_message = myPublicDialogBackground()
        backgroundWidget_message.setTitle(MessageType.Ask.value)
        backgroundWidget_message.setWidget(myMessage, True)
        self.mask_message.layout().addWidget(backgroundWidget_message)
        self.mask_message.show()
        reply = myMessage.exec_()
        self.mask_message.close()
        if reply:
            self.clearData()
            return True
        else:
            return False

