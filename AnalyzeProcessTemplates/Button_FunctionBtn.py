import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLineEdit
from PyQt5.QtCore import Qt, QMimeData, QPoint, pyqtSignal, QObject, QRect
from PyQt5.QtGui import QDrag, QPainter, QPen, QBrush
from enum import Enum, unique
from AnalyzeProcessTemplates.public import isDebug

class CustomizationFunctionBtn(QPushButton):
    sendmsg = pyqtSignal(str)
    sendmsg_ChangeConnectLine = pyqtSignal(str)
    def __init__(self, btnWidth, btnHeight, parent):
        super(CustomizationFunctionBtn, self).__init__(parent)
        self.PressCoordinate = [0, 0]
        self.__initUI(btnWidth, btnHeight)
        self.__initConnect()

    # 初始化UI
    def __initUI(self, btnWidth, btnHeight):
        self.setFixedHeight(btnHeight)
        self.setFixedWidth(btnWidth)
        self.setCheckable(True)
        self.setStyleSheet("QPushButton:checked{background-color:blue;}")

    # 初始化连接（信号和槽）
    def __initConnect(self):
        pass

    # 设置步骤名称（doe|fit|SA|......）
    def setBtnFeatureType(self, fratureName):
        borderRadius = 10 # 按钮圆角半径
        backgroundColor = '#2E3648' #背景色
        borderColor = '#2E3648' #边框颜色
        fontSize = 14 #字体大小
        fontColor = '#BDC8E2' #字体颜色
        hoverBackgroundColor = '#a4d188'
        clickedBackgroundColor = '#a4d188'
        hoverFontColor = '#2a3523'
        clickedFontColor = '#2a3523'
        self.setText(fratureName)
        if fratureName == "doe":
            backgroundColor = '#365cc5'
            borderColor = '#2e4ea6'
        elif fratureName == "dataInput":
            backgroundColor = '#8857c5'
            borderColor = '#5a3a84'
        elif fratureName == "fit":
            backgroundColor = '#6175bd'
            borderColor = '#48588c'
        elif fratureName == "opt":
            backgroundColor = '#665c9e'
            borderColor = '#3d375f'
        elif fratureName == "FECalcuFile":
            backgroundColor = '#00a6a6'
            borderColor = '#004b4b'
        elif fratureName == "Sim":
            backgroundColor = '#aa7100'
            borderColor = '#704b00'
        stringBtnStyle = f'font-family: "Microsoft YaHei"; font-size: {fontSize}px; font-style: italic; font-weight: bold;'
        stringBtnStyle += f'color: {fontColor}; font: bold italic 18px "Microsoft YaHei";'
        stringBtnStyle += f'border-style: solid; border-width: 2px; border-color: {borderColor}; border-radius: {borderRadius}px;'
        stringBtnStyle += f'background-color: {backgroundColor};'

        string = 'QPushButton {' + stringBtnStyle + '}'
        string += 'QPushButton:hover{' + \
                  f'color: {hoverFontColor}; border-color: {hoverBackgroundColor}; background-color: {hoverBackgroundColor};' +\
                  '}'
        string += 'QPushButton:pressed{' + \
                  f'color: {clickedFontColor}; border-color: {clickedBackgroundColor}; background-color: {clickedBackgroundColor};' +\
                  '}'
        string += 'QPushButton:clicked{' + \
                  f'color: {clickedFontColor}; border-color: {clickedBackgroundColor}; background-color: {clickedBackgroundColor};' + \
                  '}'
        self.setStyleSheet(string)

    def setBtnCheckedStyleSheet(self):
        fontSize = 14  # 字体大小
        clickedFontColor = '#2a3523'
        clickedBackgroundColor = '#a4d188'
        borderRadius = 10  # 按钮圆角半径
        borderColor = '#2a3523'  # 边框颜色
        stringBtnStyle = f'font-family: "Microsoft YaHei"; font-size: {fontSize}px; font-style: italic; font-weight: bold;'
        stringBtnStyle += f'color: {clickedFontColor}; font: bold italic 18px "Microsoft YaHei";'
        stringBtnStyle += f'border-style: solid; border-width: 2px; border-color: {borderColor}; border-radius: {borderRadius}px;'
        stringBtnStyle += f'background-color: {clickedBackgroundColor};'
        string = 'QPushButton {' + stringBtnStyle + '}'
        self.setStyleSheet(string)

    # 对应步骤选择的模型/方法, 将其显示在按钮上
    def setBtnFeatureWays(self, ways):
        pass

    def mousePressEvent(self, e):
        if isDebug:
            print("FunctionBtnPress", e.pos())
        self.PressCoordinate[0] = e.x()
        self.PressCoordinate[1] = e.y()
        self.sendmsg.emit(self.objectName())

    def enterEvent(self, e):
        return super(CustomizationFunctionBtn, self).enterEvent(e)

    def mouseMoveEvent(self, e):
        if isDebug:
            print("FunctionBtnMove", e.pos)
        cor = QPoint(0, 0)

        # 将父窗口及鼠标点转化成全局坐标
        widgetGlobalPos = self.parent().mapToGlobal(QPoint(0, 0))
        widgetWidth = self.parent().geometry().width()
        widgetHeight = self.parent().geometry().height()
        widgetGlobalGeo = QRect(widgetGlobalPos.x(), widgetGlobalPos.y(), widgetWidth, widgetHeight)
        eGlobalPos = e.globalPos()

        if widgetGlobalGeo.contains(eGlobalPos):
            dis_x = e.x() - self.PressCoordinate[0]
            dis_y = e.y() - self.PressCoordinate[1]
            cor.setX(dis_x)
            cor.setY(dis_y)
            self.move(self.mapToParent(cor))
            # 发消息给父界面，更改连接线
            self.sendmsg_ChangeConnectLine.emit(self.objectName())