import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLineEdit
from PyQt5.QtCore import Qt, QMimeData, QPoint, pyqtSignal, QObject, QRect
from PyQt5.QtGui import QDrag, QPainter, QPen, QBrush, QPolygon, QRegion, QColor, QPolygonF
from enum import Enum, unique
import time

@unique
class LineEnum(Enum):
    Horizontal = "Hori"
    Vertical = "Vert"

@unique
class LineNumber(Enum):
    One = "one"
    Two = "two"
    Three = "three"

class ButtonRelativePos(Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8

class DraggableButton(QPushButton):
    sendMsg = pyqtSignal(LineNumber, int, int)     # 线条1移动时发送到信号
    def __init__(self, director, number, lineWidth, parent):
        super().__init__(parent)
        self.Number = number          #线段编号
        self.Director = director
        self.PressCoordinate = [0, 0]    #存储需要移动的距离
        self.StartX = 0
        self.StartY = 0
        self.EndX = 0
        self.EndY = 0
        self.LineWidth = lineWidth

    def paintEvent(self, evt):
        painter = QPainter(self)
        pen = QPen(Qt.red, self.LineWidth, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin)

        painter.setRenderHint(QPainter.Antialiasing)
        brush = QBrush()
        brush.setColor(QColor(192, 192, 16))
        pen.setColor(QColor(192, 192, 16))
        brush.setStyle(Qt.SolidPattern)
        painter.setPen(pen)
        painter.setBrush(brush)

        # 在按钮上画线
        if self.Director == LineEnum.Vertical:
            StartY = int(self.geometry().height()/2)
            painter.drawLine(0, StartY, self.geometry().width(), StartY)
        if self.Director == LineEnum.Horizontal:
            StartX = int(self.geometry().width()/2)
            painter.drawLine(StartX, 0, StartX, self.geometry().height())

    def mousePressEvent(self, e):
        print("ConnectLinesPress", e.pos())
        self.PressCoordinate[0] = e.x()
        self.PressCoordinate[1] = e.y()
        return super(DraggableButton, self).mousePressEvent(e)

    def enterEvent(self, e):
        if self.Director == LineEnum.Vertical:
            self.setCursor(Qt.SizeVerCursor)
        if self.Director == LineEnum.Horizontal:
            self.setCursor(Qt.SizeHorCursor)
        return super(DraggableButton, self).enterEvent(e)

    def mouseMoveEvent(self, e):
        cor = QPoint(0, 0)
        # 将父窗口及鼠标点转化成全局坐标
        widgetGlobalPos = self.parent().mapToGlobal(QPoint(0, 0))
        widgetWidth = self.parent().geometry().width()
        widgetHeight = self.parent().geometry().height()
        widgetGlobalGeo = QRect(widgetGlobalPos.x(), widgetGlobalPos.y(), widgetWidth, widgetHeight)
        eGlobalPos = e.globalPos()

        if self.Director == LineEnum.Horizontal and self.Number == LineNumber.Two:
            if widgetGlobalGeo.contains(eGlobalPos):
                dis_x = e.x() - self.PressCoordinate[0]  # 计算垂直的线段在X方向上的位移
                cor.setX(dis_x)
                self.move(self.mapToParent(cor))  # 需要maptoparent一下才可以的,否则只是相对位置。
            else:
                if e.x() > 0:
                    self.move(QPoint(self.parent().geometry().width() - (self.width() + self.LineWidth)/2,
                                     self.mapToParent(QPoint(0, 0)).y()))
                else:
                    self.move(QPoint((self.width() - self.LineWidth)/2, self.mapToParent(QPoint(0, 0)).y()))

        if self.Director == LineEnum.Vertical and self.Number == LineNumber.Two:
            if widgetGlobalGeo.contains(eGlobalPos):
                dis_y = e.y() - self.PressCoordinate[1]  # 计算水平的线段在Y方向上的位移
                cor.setY(dis_y)
                self.move(self.mapToParent(cor))  # 需要maptoparent一下才可以的,否则只是相对位置。
            else:
                if e.y() > 0:
                    self.move(QPoint(self.mapToParent(QPoint(0, 0)).x(),
                                     self.parent().geometry().height() - (self.height() + self.LineWidth) / 2))
                else:
                    self.move(QPoint(self.mapToParent(QPoint(0, 0)).x(), -(self.height() - self.LineWidth) / 2))

        #改变其余线段的位置
        self.sendMsg.emit(self.Number, self.pos().x(), self.pos().y())

class ConnectLines(QWidget):
    def __init__(self, startGeo, endGeo, parent):
        super(ConnectLines, self).__init__(parent, Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.LineWidth = 3
        self.ButtonWidth = 3
        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口透明背景
        self.StartPos = [0, 0]
        self.EndPos = [0, 0]
        self.translateGeometoryToPoints(startGeo, endGeo)
        self.point1 = QPoint(0, 0)
        self.point2 = QPoint(0, 0)
        self.point3 = QPoint(0, 0)
        self.point4 = QPoint(0, 0)
        self.button1 = None
        self.button2 = None
        self.button3 = None
        self.__initUI__()
        self.__Connect__()

    def __initUI__(self):
        # 从起始和终止点创建需要的四个节点
        self.getLinesPoints()
        # 创建连接线
        self.CreateLine()
        # 设置线的尺寸
        self.ChangeButtonSizeByPoints()

    def translateGeometoryToPoints(self, startGeo, endGeo):
        self.relativePos = None
        # 坐标点位置转换
        if (endGeo.x() <= startGeo.x() + startGeo.width()) and (endGeo.x() >= startGeo.x()):
            if startGeo.y() > endGeo.y():
                self.StartPos[0] = startGeo.x() + startGeo.width()/2 - self.ButtonWidth/2
                self.StartPos[1] = startGeo.y()
                self.EndPos[0] = endGeo.x() + endGeo.width()/2 - self.ButtonWidth/2
                self.EndPos[1] = endGeo.y() + endGeo.height()
                self.setGeometry(self.StartPos[0], self.EndPos[1],
                                 self.EndPos[0] - self.StartPos[0] + self.ButtonWidth, self.StartPos[1] - self.EndPos[1])
                self.relativePos = ButtonRelativePos.eight
            else:
                self.StartPos[0] = startGeo.x() + startGeo.width()/2 - self.ButtonWidth/2
                self.StartPos[1] = startGeo.y() + startGeo.height()
                self.EndPos[0] = endGeo.x() + endGeo.width()/2 + self.ButtonWidth/2
                self.EndPos[1] = endGeo.y()
                self.setGeometry(self.StartPos[0], self.StartPos[1],
                                 self.EndPos[0] - self.StartPos[0], self.EndPos[1] - self.StartPos[1])
                self.relativePos = ButtonRelativePos.five
        elif (startGeo.x() > endGeo.x()) and (startGeo.x() < endGeo.x() + endGeo.width()):
            if startGeo.y() >= endGeo.y():
                self.StartPos[0] = endGeo.x() + endGeo.width()/2 - self.ButtonWidth/2
                self.StartPos[1] = endGeo.y() + endGeo.height()
                self.EndPos[0] = startGeo.x() + startGeo.width()/2 + self.ButtonWidth/2
                self.EndPos[1] = startGeo.y()
                self.setGeometry(self.StartPos[0], self.StartPos[1],
                                 self.EndPos[0] - self.StartPos[0], self.EndPos[1] - self.StartPos[1])
                self.relativePos = ButtonRelativePos.seven
            else:
                self.StartPos[0] = endGeo.x() + endGeo.width()/2 - self.ButtonWidth/2
                self.StartPos[1] = startGeo.y() + startGeo.height()
                self.EndPos[0] = startGeo.x() + startGeo.width()/2 + self.ButtonWidth/2
                self.EndPos[1] = endGeo.y()
                self.setGeometry(self.StartPos[0], self.StartPos[1],
                                 self.EndPos[0] - self.StartPos[0], self.EndPos[1] - self.StartPos[1])
                self.relativePos = ButtonRelativePos.six
        # 第一象限
        elif startGeo.x() <= endGeo.x() and startGeo.y() <= endGeo.y():
            self.StartPos[0] = startGeo.x() + startGeo.width()
            self.StartPos[1] = startGeo.y() + startGeo.height() / 2
            self.EndPos[0] = endGeo.x()
            self.EndPos[1] = endGeo.y() + endGeo.height() / 2
            self.setGeometry(self.StartPos[0], self.StartPos[1],
                             self.EndPos[0] - self.StartPos[0], self.EndPos[1] - self.StartPos[1] + self.ButtonWidth)
            self.relativePos = ButtonRelativePos.one
        # 第四象限
        elif startGeo.x() <= endGeo.x() and startGeo.y() >= endGeo.y():
            self.StartPos[0] = startGeo.x() + startGeo.width()
            self.StartPos[1] = startGeo.y() + startGeo.height() / 2
            self.EndPos[0] = endGeo.x()
            self.EndPos[1] = endGeo.y() + endGeo.height() / 2
            self.setGeometry(self.StartPos[0], self.EndPos[1],
                             self.EndPos[0] - self.StartPos[0], self.StartPos[1] - self.EndPos[1] + self.ButtonWidth)
            print("startPos,EndPos", self.StartPos, self.EndPos)
            self.relativePos = ButtonRelativePos.four
        # 第二象限
        elif startGeo.x() >= endGeo.x() and startGeo.y() <= endGeo.y():
            self.StartPos[0] = endGeo.x() + endGeo.width()
            self.StartPos[1] = startGeo.y() + startGeo.height()/2 - self.ButtonWidth/2
            self.EndPos[0] = startGeo.x()
            self.EndPos[1] = endGeo.y() + endGeo.height()/2 + self.ButtonWidth/2
            self.setGeometry(self.StartPos[0], self.StartPos[1],
                                 self.EndPos[0] - self.StartPos[0], self.EndPos[1] - self.StartPos[1])
            self.relativePos = ButtonRelativePos.two
        # 第三象限
        elif startGeo.x() >= endGeo.x() and startGeo.y() >= endGeo.y():
            self.StartPos[0] = endGeo.x() + endGeo.width()
            self.StartPos[1] = endGeo.y() + endGeo.height()/2 - self.ButtonWidth/2
            self.EndPos[0] = startGeo.x()
            self.EndPos[1] = startGeo.y() + startGeo.height()/2 + self.ButtonWidth/2
            self.setGeometry(self.StartPos[0], self.StartPos[1],
                             self.EndPos[0] - self.StartPos[0], self.EndPos[1] - self.StartPos[1])
            self.relativePos = ButtonRelativePos.three

    def getLinesPoints(self):
        self.length = self.EndPos[0] - self.StartPos[0]
        self.height = self.EndPos[1] - self.StartPos[1]

        print("self.geo", self.geometry())

        if self.relativePos == ButtonRelativePos.eight:
            self.point1 = QPoint(0, abs(self.height))
            self.point2 = QPoint(0, abs(self.height/2) - self.ButtonWidth/2)
            self.point3 = QPoint(abs(self.length) + self.ButtonWidth, abs(self.height/2) - self.ButtonWidth/2)
            self.point4 = QPoint(abs(self.length), 0)
        elif self.relativePos == ButtonRelativePos.five:
            self.point1 = QPoint(0, 0)
            self.point2 = QPoint(0, abs(self.height)/2 - self.ButtonWidth/2)
            self.point3 = QPoint(abs(self.length) - self.ButtonWidth, abs(self.height)/2 - self.ButtonWidth/2)
            self.point4 = QPoint(abs(self.length) - self.ButtonWidth, abs(self.height))
        elif self.relativePos == ButtonRelativePos.seven:
            self.point1 = QPoint(0, 0)
            self.point2 = QPoint(0, abs(self.height)/2 - self.ButtonWidth/2)
            self.point3 = QPoint(abs(self.length) - self.ButtonWidth, abs(self.height) / 2 - self.ButtonWidth / 2)
            self.point4 = QPoint(abs(self.length) - self.ButtonWidth, abs(self.height))
        elif self.relativePos == ButtonRelativePos.six:
            self.point1 = QPoint(abs(self.length) - self.ButtonWidth, 0)
            self.point2 = QPoint(abs(self.length) - self.ButtonWidth, abs(self.height / 2) - self.ButtonWidth / 2)
            self.point3 = QPoint(0, abs(self.height / 2) - self.ButtonWidth / 2)
            self.point4 = QPoint(0, abs(self.height))
        # 第一象限
        elif self.relativePos == ButtonRelativePos.one:
            self.point1 = QPoint(0, 0)
            self.point2 = QPoint(self.length / 2, 0)
            self.point3 = QPoint(self.length / 2, self.height)
            self.point4 = QPoint(self.length, self.height)
        # 第二象限
        elif self.relativePos == ButtonRelativePos.two:
            self.point1 = QPoint(0, abs(self.height) - self.ButtonWidth)
            self.point2 = QPoint(self.length / 2 - self.ButtonWidth/2, abs(self.height) - self.ButtonWidth)
            self.point3 = QPoint(self.length / 2 - self.ButtonWidth/2, 0)
            self.point4 = QPoint(self.length, 0)
        # 第三象限
        elif self.relativePos == ButtonRelativePos.three:
            self.point1 = QPoint(0, 0)
            self.point2 = QPoint(abs(self.length)/2 - self.ButtonWidth/2, 0)
            self.point3 = QPoint(abs(self.length)/2 - self.ButtonWidth/2, abs(self.height) - self.ButtonWidth)
            self.point4 = QPoint(abs(self.length), abs(self.height) - self.ButtonWidth)
        # 第四象限
        elif self.relativePos == ButtonRelativePos.four:
            self.point1 = QPoint(0, abs(self.height))
            self.point2 = QPoint(self.length / 2, abs(self.height))
            self.point3 = QPoint(self.length / 2, 0)
            self.point4 = QPoint(self.length, 0)

    def CreateLine(self):
        if self.relativePos is not None:
            if self.relativePos.value >= ButtonRelativePos.five.value:
                self.__CreateLines_()
            else:
                self.__CreateLines__()

    def __CreateLines__(self):# 水平 + 竖直 + 水平
        if self.button1 is not None:
            self.button1.deleteLater()
        self.button1 = DraggableButton(LineEnum.Vertical, LineNumber.One, self.LineWidth, self)
        self.button1.show()

        if self.button2 is not None:
            self.button2.deleteLater()
        self.button2 = DraggableButton(LineEnum.Horizontal, LineNumber.Two, self.LineWidth, self)
        self.button2.setObjectName("SecondLine")
        self.button2.show()

        if self.button3 is not None:
            self.button3.deleteLater()
        self.button3 = DraggableButton(LineEnum.Vertical, LineNumber.Three, self.LineWidth, self)
        self.button3.show()

    def __CreateLines_(self): # 竖直 + 水平 + 竖直
        if self.button1 is not None:
            self.button1.deleteLater()
        self.button1 = DraggableButton(LineEnum.Horizontal, LineNumber.One, self.LineWidth, self)
        self.button1.show()

        if self.button2 is not None:
            self.button2.deleteLater()
        self.button2 = DraggableButton(LineEnum.Vertical, LineNumber.Two, self.LineWidth, self)
        self.button2.setObjectName("SecondLine")
        self.button2.show()

        if self.button3 is not None:
            self.button3.deleteLater()
        self.button3 = DraggableButton(LineEnum.Horizontal, LineNumber.Three, self.LineWidth, self)
        self.button3.show()

    def ChangeButtonSizeByPoints(self):
        offsetX = (self.ButtonWidth - self.LineWidth) / 2
        offsetY = (self.ButtonWidth - self.LineWidth) / 2
        if self.relativePos == ButtonRelativePos.eight:
            self.button1.setGeometry(self.point2.x(), self.point2.y(), self.ButtonWidth, self.point1.y() - self.point2.y())
            self.button2.setGeometry(self.point2.x(), self.point2.y(), self.point3.x() - self.point2.x(), self.ButtonWidth)
            self.button3.setGeometry(self.point4.x(), self.point4.y(), self.ButtonWidth,  self.point3.y() - self.point4.y())
        elif self.relativePos == ButtonRelativePos.five:
            self.button1.setGeometry(self.point1.x(), self.point1.y(), self.ButtonWidth, self.point2.y() - self.point1.y())
            self.button2.setGeometry(self.point2.x(), self.point2.y(), self.point3.x() - self.point2.x(), self.ButtonWidth)
            self.button3.setGeometry(self.point3.x(), self.point3.y(), self.ButtonWidth, self.point4.y() - self.point3.y())
        elif self.relativePos == ButtonRelativePos.seven:
            self.button1.setGeometry(self.point1.x(), self.point1.y(), self.ButtonWidth, self.point2.y() - self.point1.y())
            self.button2.setGeometry(self.point2.x(), self.point2.y(), self.point3.x() - self.point2.x(), self.ButtonWidth)
            self.button3.setGeometry(self.point3.x(), self.point3.y(), self.ButtonWidth, self.point4.y() - self.point3.y())
        elif self.relativePos == ButtonRelativePos.six:
            self.button1.setGeometry(self.point1.x(), self.point1.y(), self.ButtonWidth, self.point2.y() - self.point1.y())
            self.button2.setGeometry(self.point3.x(), self.point3.y(), self.point2.x() - self.point3.x() + self.ButtonWidth, self.ButtonWidth)
            self.button3.setGeometry(self.point3.x(), self.point3.y(), self.ButtonWidth, self.point4.y() - self.point3.y())
        # 第一象限
        elif self.relativePos == ButtonRelativePos.one:
            self.button1.setGeometry(self.point1.x(), self.point1.y(), self.point2.x() - self.point1.x(), self.ButtonWidth)
            self.button2.setGeometry(self.point2.x() - offsetX, self.point2.y() + offsetY, self.ButtonWidth, self.point3.y() - self.point2.y())
            self.button3.setGeometry(self.point3.x(), self.point3.y(), self.point4.x() - self.point3.x() + offsetX, self.ButtonWidth)
        # 第二象限
        elif self.relativePos == ButtonRelativePos.two:
            self.button1.setGeometry(self.point1.x(), self.point1.y(), self.point2.x() - self.point1.x(), self.ButtonWidth)
            self.button2.setGeometry(self.point3.x(), self.point3.y(), self.ButtonWidth, self.point2.y() - self.point3.y() + self.ButtonWidth)
            self.button3.setGeometry(self.point3.x(), self.point3.y(), self.point4.x() - self.point3.x(), self.ButtonWidth)
        # 第三象限
        elif self.relativePos == ButtonRelativePos.three:
            self.button1.setGeometry(self.point1.x(), self.point1.y(), self.point2.x() - self.point1.x(), self.ButtonWidth)
            self.button2.setGeometry(self.point2.x(), self.point2.y(), self.ButtonWidth, self.point3.y() - self.point2.y())
            self.button3.setGeometry(self.point3.x(), self.point3.y(), self.point4.x() - self.point3.x(), self.ButtonWidth)
        # 第四象限
        elif self.relativePos == ButtonRelativePos.four:
            self.button1.setGeometry(self.point1.x(), self.point1.y(), self.point2.x() - self.point1.x(), self.ButtonWidth)
            self.button2.setGeometry(self.point3.x() - offsetX, self.point3.y() + offsetY, self.ButtonWidth,
                                     abs(self.point3.y() - self.point2.y()) + self.ButtonWidth / 2 + self.LineWidth / 2)
            self.button3.setGeometry(self.point3.x(), self.point3.y(), self.point4.x() - self.point3.x() + offsetX,
                                     self.ButtonWidth)


    def ChangeWidgetSize(self, startGeo, endGeo):
        self.translateGeometoryToPoints(startGeo, endGeo)
        # 从起始和终止点计算出需要的四个节点
        self.getLinesPoints()
        # 创建连接线
        self.CreateLine()
        self.__Connect__()
        # 设置线的尺寸
        self.ChangeButtonSizeByPoints()

    def __Connect__(self):
        self.button1.sendMsg.connect(self.ChangeButtonPos)
        self.button2.sendMsg.connect(self.ChangeButtonPos)
        self.button3.sendMsg.connect(self.ChangeButtonPos)

    def mouseMoveEvent(self, e):
        print('ConnectLineMove', e.x(), e.y())

    def ChangeButtonPos(self, LineNumber, posX, posY):
        if LineNumber == LineNumber.Two:
            if self.relativePos.value >= ButtonRelativePos.five.value:
                self.point2.setY(posY)
                self.point3.setY(posY)
            else:
                self.point2.setX(posX)
                self.point3.setX(posX)
        self.ChangeButtonSizeByPoints()

    def paintEvent(self, e):
        if self.findChild(QPushButton, "SecondLine"):
            MaskWidgetPoints = None
            if self.relativePos == ButtonRelativePos.one:
                MaskWidgetPoints = [QPoint(self.button1.x(), self.button1.y()),
                                    QPoint(self.button2.x() + self.button2.width(), self.button1.y()),
                                    QPoint(self.button2.x() + self.button2.width(), self.button3.y()),
                                    QPoint(self.button2.x() + self.button2.width() + self.button3.width(), self.button3.y()),
                                    QPoint(self.button2.x() + self.button2.width() + self.button3.width(), self.button3.y() + self.button3.height()),
                                    QPoint(self.button2.x(), self.button2.y() + self.button3.y() + self.button3.height()),
                                    QPoint(self.button2.x(), self.button2.y() + self.button1.height()),
                                    QPoint(self.button1.x(), self.button1.y() + self.button1.height())]
            elif self.relativePos == ButtonRelativePos.two:
                MaskWidgetPoints = [QPoint(self.button1.x(), self.button1.y()),
                                    QPoint(self.button2.x(), self.button1.y()),
                                    QPoint(self.button2.x(), self.button2.y()),
                                    QPoint(self.button2.x() + self.button3.width(), self.button3.y()),
                                    QPoint(self.button2.x() + self.button3.width(), self.button3.y() + self.button3.height()),
                                    QPoint(self.point2.x() + self.button2.width(), self.button3.y() + self.button3.height()),
                                    QPoint(self.point2.x() + self.button2.width(), self.button1.y() + self.button1.height()),
                                    QPoint(self.button1.x(), self.button1.y() + self.button1.height())]
            elif self.relativePos == ButtonRelativePos.three:
                MaskWidgetPoints = [QPoint(self.button1.x(), self.button1.y()),
                                    QPoint(self.button2.x() + self.ButtonWidth, self.button1.y()),
                                    QPoint(self.button2.x() + self.ButtonWidth, self.button3.y()),
                                    QPoint(self.button3.x() + self.button3.width(), self.button3.y()),
                                    QPoint(self.button3.x() + self.button3.width(), self.button3.y() + self.button3.height()),
                                    QPoint(self.button3.x(), self.button3.y() + self.button3.height()),
                                    QPoint(self.button3.x(), self.button1.y() + self.button1.height()),
                                    QPoint(self.button1.x(), self.button1.y() + self.button1.height())]
            elif self.relativePos == ButtonRelativePos.four:
                MaskWidgetPoints = [QPoint(self.button1.x(), self.button1.y()),
                                    QPoint(self.button2.x(), self.button1.y()),
                                    QPoint(self.button2.x(), self.button3.y()),
                                    QPoint(self.button2.x() + self.button2.width() + self.button3.width(),
                                           self.button3.y()),
                                    QPoint(self.button2.x() + self.button2.width() + self.button3.width(),
                                           self.button3.y() + self.button3.height()),
                                    QPoint(self.button2.x() + self.button2.width(),
                                           self.button2.y() + self.button3.y() + self.button3.height()),
                                    QPoint(self.button2.x() + self.button2.width(), self.button1.y() + self.button1.height()),
                                    QPoint(self.button1.x(), self.button1.y() + self.button1.height())]
            elif self.relativePos == ButtonRelativePos.five:
                MaskWidgetPoints = [QPoint(self.button1.x(), self.button1.y()),
                                    QPoint(self.button2.x() + self.ButtonWidth, self.button1.y()),
                                    QPoint(self.button2.x() + self.ButtonWidth, self.button3.y()),
                                    QPoint(self.button3.x() + self.button3.width(), self.button3.y()),
                                    QPoint(self.button3.x() + self.button3.width(), self.button3.y() + self.button3.height()),
                                    QPoint(self.button3.x(), self.button3.y() + self.button3.height()),
                                    QPoint(self.button2.x() + self.button2.width(), self.button2.y() + self.button2.height()),
                                    QPoint(self.button2.x(), self.button2.y() + self.button2.height())]
            elif self.relativePos == ButtonRelativePos.six:
                MaskWidgetPoints = [QPoint(self.button1.x(), self.button1.y()),
                                    QPoint(self.button1.x() + self.button1.width(), self.button1.y()),
                                    QPoint(self.button1.x() + self.button1.width(), self.button2.y() + self.button2.height()),
                                    QPoint(self.button2.x() + self.button3.width(), self.button2.y() + self.button2.height()),
                                    QPoint(self.button2.x() + self.button3.width(), self.button3.y() + self.button3.height()),
                                    QPoint(self.button3.x(), self.button3.y() + self.button3.height()),
                                    QPoint(self.button3.x(), self.button3.y()),
                                    QPoint(self.button1.x(), self.button1.y() + self.button1.height())]
            elif self.relativePos == ButtonRelativePos.seven:
                MaskWidgetPoints = [QPoint(self.button1.x(), self.button1.y()),
                                    QPoint(self.button1.x() + self.button1.width(), self.button1.y()),
                                    QPoint(self.button1.x() + self.button1.width(), self.button2.y()),
                                    QPoint(self.button3.x() + self.button3.width(), self.button2.y()),
                                    QPoint(self.button3.x() + self.button3.width(), self.button3.y() + self.button3.height()),
                                    QPoint(self.button3.x(), self.button3.y() + self.button3.height()),
                                    QPoint(self.button3.x(), self.button2.y() + self.button2.height()),
                                    QPoint(self.button2.x(), self.button2.y() + self.button2.height())]
            elif self.relativePos == ButtonRelativePos.eight:
                MaskWidgetPoints = [QPoint(self.button1.x(), self.button1.y() + self.button1.height()),
                                    QPoint(self.button1.x(), self.button1.y()),
                                    QPoint(self.button3.x(), self.button2.y()),
                                    QPoint(self.button3.x(), self.button3.y()),
                                    QPoint(self.button3.x() + self.button3.width(), self.button3.y()),
                                    QPoint(self.button3.x() + self.button3.width(), self.button2.y() + self.button2.height()),
                                    QPoint(self.button2.x() + self.button2.width(), self.button2.y() + self.button2.height()),
                                    QPoint(self.button1.x() + self.button1.width(), self.button1.y() + self.button1.height())]
            if not MaskWidgetPoints is None:
                # print("MaskWidgetPoints:", MaskWidgetPoints)
                MaskArea = QPolygon(MaskWidgetPoints)
                self.setMask(QRegion(MaskArea))
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ConnectLines((300, 400), (600, 0))
    ex.show()
    app.exec_()

