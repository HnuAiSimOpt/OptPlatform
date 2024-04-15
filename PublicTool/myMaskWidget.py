from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PublicTool.myProgressBar import myProgressBar
import sys
from AnalyzeProcessTemplates.public import progressPercent
from configFile.ReadTemplateConf import ReadandWriteTemplateConf

class myMaskWidget(QWidget):
    def __init__(self, parent=None, isProgress=False, isAuto = True):
        super(myMaskWidget, self).__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName('maskWidget')
        self.setStyleSheet('QWidget#maskWidget{background-color:rgba(212,212,212,105);}')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(0, 0, 1000, 800)
        self.isAuto = isAuto
        self.compeletedNum = 0
        self.timer = None
        layout = QHBoxLayout()
        self.setLayout(layout)
        if isProgress:
            self.addProgressBar()
        self.__initConnect__()

    def __initConnect__(self):
        try:
            self.parent().sizeChangedSignal.connect(self.changeSize)
        except:
            pass

    def addProgressBar(self):
        self.progressBar = myProgressBar()
        barPos_x = int(self.width() / 2 - self.progressBar.width() / 2)
        barPos_y = int(self.height()/2 - self.progressBar.height()/2)
        self.progressBar.move(barPos_x, barPos_y)
        layout = self.layout()
        layout.addWidget(self.progressBar)
        self.setAuto(self.isAuto)

    def updateProgressAuto(self):
        if ReadandWriteTemplateConf().ProgressBar_isAuto == False:
            self.setAuto(False)
            return
        self.progressBar.drawText(ReadandWriteTemplateConf().ProgressBar_curCalculateStep)
        self.progressBar.text_progress = ''
        self.percent += 0.001
        if self.percent <= 1:
            self.progressBar.setProcessorValue(self.percent)
        else:
            self.percent = 0
            self.progressBar.setProcessorValue(self.percent)

    def updateProgressByPercent(self):
        if ReadandWriteTemplateConf().ProgressBar_isAuto == True:
            self.setAuto(True)
            return
        self.percent = round(ReadandWriteTemplateConf().ProgressBar_calculateCompeletedNum / self.totalNum, 3)
        self.progressBar.setProcessorValue(self.percent)
        curPercecnt = "%.1f%%" % (self.percent * 100)
        self.progressBar.drawText(ReadandWriteTemplateConf().ProgressBar_curCalculateStep)
        self.progressBar.drawProgressText(f'当前完成进度：{curPercecnt}')

    def show(self):
        if self.parent() is None:
            super().show()
        else:
            parentRect = self.parent().geometry()
            self.setGeometry(0, 0, parentRect.width(), parentRect.height())
            super().show()

    def changeSize(self) -> None:
        parentRect = self.parent().geometry()
        self.setGeometry(0, 0, parentRect.width(), parentRect.height())

    def setAuto(self, bAuto):
        self.isAuto = bAuto
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
        if self.isAuto:
            self.timer = QTimer()
            self.timer.timeout.connect(self.updateProgressAuto)
            self.percent = 0
            self.timer.start(1)
        else:
            self.timer = QTimer()
            self.totalNum = ReadandWriteTemplateConf().data_DOE.doe_SampleSize
            self.timer.timeout.connect(self.updateProgressByPercent)
            self.percent = 0
            self.timer.start(100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = myMaskWidget()
    ex.show()
    app.exec_()