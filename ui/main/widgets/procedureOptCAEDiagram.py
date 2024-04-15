from ui.main.raw.Ui_procedures_opt_CAE import Ui_Form
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize

class ProcedureOptCAEDiagram(QWidget, Ui_Form):
    def __init__(self):
        super(ProcedureOptCAEDiagram, self).__init__()
        self.setupUi(self)
        self.__initUI__()

    def __initUI__(self):
        self.label.setStyleSheet('background-color:transparent; color:white')
        self.label_3.setStyleSheet('background-color:transparent; color:white')
        self.label_4.setStyleSheet('background-color:transparent; color:white')
        self.label_5.setStyleSheet('background-color:transparent; color:white')
        self.label_6.setStyleSheet('background-color:transparent; color:white')
        self.label_7.setStyleSheet('background-color:transparent; color:white')
        self.label_8.setStyleSheet('background-color:transparent; color:white')
        self.pushButton.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_2.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_3.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_4.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_5.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_6.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_7.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_8.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_9.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_10.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_11.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_12.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.pushButton_13.setStyleSheet('QPushButton{background-color:transparent; border:none;}')
        self.btn_1 = QPushButton(self)
        self.btn_2 = QPushButton(self)
        self.btn_3 = QPushButton(self)
        self.addInputAndOutputLabel()

    def addInputAndOutputLabel(self):
        self.iheight = 36
        self.iwidth = 36

        icon_1 = QIcon()
        icon_1.addPixmap(QPixmap(":/pic/icons/示意图_input.png"), QIcon.Normal, QIcon.Off)
        self.btn_1.setIcon(icon_1)
        self.btn_1.setIconSize(QSize(self.iwidth, self.iheight))
        self.btn_1.setFixedWidth(self.iwidth)
        self.btn_1.setFixedHeight(self.iheight)
        self.btn_1.show()
        self.btn_1.setStyleSheet('background-color:transparent;border:none;')

        icon_2 = QIcon()
        icon_2.addPixmap(QPixmap(":/pic/icons/示意图_output.png"), QIcon.Normal, QIcon.Off)
        self.btn_2.setIcon(icon_2)
        self.btn_2.setIconSize(QSize(self.iwidth, self.iheight))
        self.btn_2.setFixedWidth(self.iwidth)
        self.btn_2.setFixedHeight(self.iheight)
        self.btn_2.show()
        self.btn_2.setStyleSheet('background-color:transparent;border:none;')

        icon_3 = QIcon()
        icon_3.addPixmap(QPixmap(":/pic/icons/示意图_output.png"), QIcon.Normal, QIcon.Off)
        self.btn_3.setIcon(icon_3)
        self.btn_3.setIconSize(QSize(self.iwidth, self.iheight))
        self.btn_3.setFixedWidth(self.iwidth)
        self.btn_3.setFixedHeight(self.iheight)
        self.btn_3.show()
        self.btn_3.setStyleSheet('background-color:transparent;border:none;')

    def showEvent(self, e) -> None:
        self.movePos()

    def resizeEvent(self, e) -> None:
        self.movePos()

    def movePos(self):
        pos = self.pushButton.pos()
        self.btn_1.move(pos.x() - self.iwidth / 2, pos.y() - self.iheight / 2)
        pos = self.pushButton_9.pos()
        self.btn_2.move(pos.x() + self.pushButton_9.width() - self.iwidth / 2, pos.y() - self.iheight / 2)
        pos = self.pushButton_11.pos()
        self.btn_3.move(pos.x() + self.pushButton_9.width() - self.iwidth / 2, pos.y() - self.iheight / 2)