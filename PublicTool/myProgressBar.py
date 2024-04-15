from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QPen, QPainter, QBrush, QPainterPath, QColor, QFont
from PyQt5.QtCore import Qt, QRect, QRectF
import math

class myProgressBar(QPushButton):
    def __init__(self, percent=0):
        super(myProgressBar, self).__init__()
        self.isInit = False
        self.innerCircleRadius = 120
        self.barWidth = 10
        self.percent = percent
        self.barBackgroundColor = QColor(144, 220, 104)
        self.barColor = QColor(94, 144, 68)
        self.innerColor = QColor(212, 212, 212)
        self.outerCircleRadius = self.innerCircleRadius + self.barWidth
        self.setFixedHeight(self.outerCircleRadius * 2 + 2)
        self.setFixedWidth(self.outerCircleRadius * 2 + 2)
        self.text = ''
        self.text_progress = ''

    def drawProgressBar(self):
        # 画外圆
        self.painter.translate(self.width()/2, self.height()/2)
        rect = QRect(-self.out/2, -self.width()/2, self.height(), self.width())
        self.pen.setColor(self.barBackgroundColor)
        self.brush.setColor(self.barBackgroundColor)
        self.painter.setPen(self.pen)
        self.painter.setBrush(self.brush)
        self.painter.drawArc(rect, 0*16, 360*16)
        # 画内圆
        self.painter.setBrush(Qt.NoBrush)
        rect = QRect(-self.innerCircleRadius / 2, -self.innerCircleRadius / 2, self.innerCircleRadius, self.innerCircleRadius)
        self.painter.drawArc(rect, 0 * 16, 360 * 16)
        self.updateProgress(0)

    def updateProgress(self, percent):
        """
        更新进度
        :return:
        """
        # 画进度
        path = QPainterPath()
        path.moveTo(0, - self.height() / 2)
        rect = QRectF(-self.barWidth / 2, -self.outerCircleRadius, self.barWidth, self.barWidth)
        path.arcTo(rect, 90, 180)
        rect = QRectF(-self.innerCircleRadius, -self.innerCircleRadius, self.innerCircleRadius * 2,
                      self.innerCircleRadius * 2)
        path.arcTo(rect, 90, -percent * 360)

        centerRadius = self.innerCircleRadius + self.barWidth / 2
        xPos = centerRadius * math.cos((90 - percent * 360) * math.pi / 180)
        yPos = centerRadius * math.sin((90 - percent * 360) * math.pi / 180)
        rect = QRectF(xPos - self.barWidth / 2, -yPos - self.barWidth / 2, self.barWidth, self.barWidth)
        path.arcTo(rect, (270 - 360 * percent), 180)

        rect = QRectF(-self.outerCircleRadius, -self.outerCircleRadius,
                      self.outerCircleRadius * 2, self.outerCircleRadius * 2)
        path.arcTo(rect, (90 - percent * 360), percent * 360)

        pen = QPen(self.barColor)
        brush = QBrush(self.barColor)
        brush.setStyle(Qt.SolidPattern)
        painter = QPainter(self)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPath(path)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        pen = QPen()
        brush = QBrush()
        if True: #self.isInit == False
            painter.setRenderHints(
                QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.Qt4CompatiblePainting)
            painter.translate(self.width() / 2, self.height() / 2)
            #画内圆
            rect = QRectF(-self.outerCircleRadius, -self.outerCircleRadius,
                          self.outerCircleRadius*2, self.outerCircleRadius*2)
            pen.setColor(self.barBackgroundColor)
            brush.setColor(self.barBackgroundColor)
            brush.setStyle(Qt.SolidPattern)
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawEllipse(rect)
            # 画内圆
            brush.setColor(self.innerColor)
            brush.setStyle(Qt.SolidPattern)
            pen.setColor(self.innerColor)
            painter.setPen(pen)
            painter.setBrush(brush)
            rect = QRectF(-self.innerCircleRadius, -self.innerCircleRadius,
                          self.innerCircleRadius*2, self.innerCircleRadius*2)
            painter.drawEllipse(rect)
            self.isInit = True

        # 画进度
        path = QPainterPath()
        path.moveTo(0, - self.height() / 2)
        rect = QRectF(-self.barWidth / 2, -self.outerCircleRadius, self.barWidth, self.barWidth)
        path.arcTo(rect, 90, 180)
        rect = QRectF(-self.innerCircleRadius, -self.innerCircleRadius, self.innerCircleRadius*2,
                      self.innerCircleRadius*2)
        path.arcTo(rect, 90, -self.percent * 360)

        centerRadius = self.innerCircleRadius + self.barWidth / 2
        xPos = centerRadius * math.cos((90 - self.percent * 360)*math.pi/180)
        yPos = centerRadius * math.sin((90 - self.percent * 360)*math.pi/180)
        rect = QRectF(xPos - self.barWidth / 2, -yPos - self.barWidth / 2, self.barWidth, self.barWidth)
        path.arcTo(rect, (270 - 360 * self.percent), 180)

        rect = QRectF(-self.outerCircleRadius, -self.outerCircleRadius,
                      self.outerCircleRadius*2, self.outerCircleRadius*2)
        path.arcTo(rect, (90 - self.percent * 360), self.percent * 360)

        pen.setColor(self.barColor)
        brush.setColor(self.barColor)
        brush.setStyle(Qt.SolidPattern)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPath(path)

        pen.setColor(QColor(59, 59, 59))
        painter.setPen(pen)
        painter.setFont(QFont('Microsoft YaHei', 16))
        rect_text = QRectF(-self.width()/2, -30, self.width(), 30)
        painter.drawText(rect_text, Qt.AlignCenter, self.text)
        rect_progress = QRectF(-self.width() / 2, 0, self.width(), 30)
        painter.drawText(rect_progress, Qt.AlignCenter, self.text_progress)

    def setProcessorValue(self, percent):
        self.percent = percent
        self.update()

    def drawText(self, text):
        self.text = text

    def drawProgressText(self, text):
        self.text_progress = text





