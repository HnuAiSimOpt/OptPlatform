from PublicTool.ui.Ui_messageDialog import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtGui import QIcon, QPixmap
from AnalyzeProcessTemplates.public import getBtnStyleString
from enum import Enum, unique

@unique
class MessageType(Enum):
    Ask    = "询问"
    Prompt    = "提示"
    Error    = "报错"

class myMessageDialog(QDialog, Ui_Dialog):
    def __init__(self, messageType:MessageType, promptStr:str):
        super(myMessageDialog, self).__init__()
        self.setupUi(self)
        self.messageType = messageType
        self.promptStr = promptStr
        self.__initUI__()

    def __initUI__(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.button(QDialogButtonBox.Ok).setFixedSize(80, 40)
        self.buttonBox.button(QDialogButtonBox.Cancel).setFixedSize(80, 40)
        self.buttonBox.button(QDialogButtonBox.Ok).setStyleSheet(getBtnStyleString())
        self.buttonBox.button(QDialogButtonBox.Cancel).setStyleSheet(getBtnStyleString())
        if self.messageType == MessageType.Ask:
            icon = QPixmap(":/pic/icons/询问.png")
        elif self.messageType == MessageType.Prompt:
            icon = QPixmap(":/pic/icons/提示.png")
        else:
            icon = QPixmap(":/pic/icons/错误圈.png")
        self.label_pic.setScaledContents(True)
        self.label_pic.setPixmap(icon)
        self.label_message.setText(self.promptStr)