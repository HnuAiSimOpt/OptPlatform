from FiniteElementCalculationFileProcessing.ui.Ui_myTextEdit import Ui_myTextEdit
from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QAction, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextBlockFormat, QFontMetrics, QTextCharFormat, QFont, QColor, QTextCursor
import sys
from PyQt5.QtCore import pyqtSignal
from FiniteElementCalculationFileProcessing.widget.Dialog_setVariable import Dialog_setVariable
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from PublicTool.myMaskWidget import myMaskWidget
from AnalyzeProcessTemplates.public import getBtnStyleString, isDebug
from PublicTool.myPublicDialogBackground import myPublicDialogBackground

class myTextEdit(QWidget, Ui_myTextEdit):
    updateParamShowMsg = pyqtSignal()

    def __init__(self, filePath, fileContents):
        super().__init__()
        self.__initUI__(filePath, fileContents)

    def __initUI__(self, filePath, fileContents):
        self.setupUi(self)
        self.textEdit_text.setLineWrapMode(QTextEdit.NoWrap)  # 不自动换行
        # screen = QApplication.primaryScreen()
        # dotsPerInch = screen.logicalDotsPerInch()
        # self.dpi = dotsPerInch / 96
        self.rowHeight = 18
        self.fontSize = 12
        self.textEdit_row.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.textEdit_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font_text = self.textEdit_text.font()
        font_text.setPointSize(self.fontSize)
        #font_text.setFamily("Microsoft YaHei")
        self.textEdit_text.setFont(font_text)
        # self.textEdit_text.setTextBackgroundColor(QColor(88, 88, 88))
        font_row = self.textEdit_row.font()
        font_row.setPointSize(self.fontSize)
        #font_row.setFamily('Microsoft YaHei')
        self.textEdit_row.setFont(font_row)
        # self.textEdit_row.setTextBackgroundColor(QColor(88, 88, 88))

        # self.textEdit_row.setStyleSheet('QTextEdit{background: rgb(88, 88, 88); color: #BDC8E2;}')
        # self.textEdit_text.setStyleSheet('QTextEdit{background: rgb(88, 88, 88); color: #BDC8E2;}')

        self.fileContents = fileContents
        self.fileContentsList = self.fileContents.split("\n")
        ReadandWriteTemplateConf().data_FECalcuFile.contents = list(self.fileContentsList)
        self.installEventFilter(self)
        self.setCustomContextMenu()

        self.showContentsInTextEdit()
        self.showRowsInTextEdit()
        self.setFileNameShow(filePath)

        self.pushButton.setStyleSheet(getBtnStyleString())

    def showContentsInTextEdit(self):
        self.textEdit_text.setText(self.fileContents)
        self.row = self.textEdit_text.document().lineCount()  # 获取文本内容的行数
        self.textEdit_text.verticalScrollBar().setSingleStep(self.rowHeight) # 设置滑动条控件递增递减的步长值
        self.textEdit_text.verticalScrollBar().setPageStep(self.rowHeight)
        self.changeVariableStrStyle()
        self.__initConnect__()

    def showRowsInTextEdit(self):
        text = str(self.textEdit_text.document().lineCount())
        font = self.textEdit_row.font()
        fm = QFontMetrics(font)
        tmpWidth = fm.boundingRect(text).width()
        self.textEdit_row.setFixedWidth(tmpWidth + 20)

    def setTextRowHeight(self, obj, height):
        doc = obj.document()
        textcursor = obj.textCursor()
        textBlockFormat = QTextBlockFormat()
        textBlockFormat.setLineHeight(height, QTextBlockFormat.FixedHeight)
        textcursor.setBlockFormat(textBlockFormat)
        obj.setTextCursor(textcursor)

    def slotCalculateScorollBarPos(self):
        """滚动条的位置更改时的槽函数，用于设置当前的行数"""
        scrollBar = self.textEdit_text.verticalScrollBar()
        pageStep = scrollBar.pageStep()
        singleStep = scrollBar.singleStep()
        currentRow = 1
        textEditHeight = self.textEdit_text.size().height()
        textLineNum = int(textEditHeight / self.rowHeight)
        if scrollBar.isVisible():
            TotalValue = scrollBar.maximum()
            currentValue = scrollBar.value() #当前的滑块距滚动条起点的距离
            currentRow = currentValue/self.rowHeight
            print("滑块位置", currentValue, "行数", currentRow)
            rowNum = textLineNum
        else:
            TotalValue = scrollBar.maximum()
            currentValue = 0
            currentRow = 0
            rowNum = self.row
        self.textEdit_row.clear()
        self.textEdit_row.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # 行数赋值
        for i in range(int(currentRow + 1), int(currentRow + 1) + rowNum):
            self.textEdit_row.append(str(i))
        # 设置文本框中滑块位置，用于将行数与文本对齐
        if currentValue == TotalValue and currentValue != 0:
            self.textEdit_row.verticalScrollBar().setValue(TotalValue)
        elif currentValue < self.rowHeight:
            self.textEdit_text.verticalScrollBar().setValue(0)
            self.textEdit_row.verticalScrollBar().setValue(0)
        else:
            self.textEdit_row.verticalScrollBar().setValue(0)
        self.adjustTextPosition()

    def __initConnect__(self):
        self.textEdit_text.verticalScrollBar().valueChanged.connect(self.slotCalculateScorollBarPos)
        self.textEdit_text.cursorPositionChanged.connect(self.slotCursorPositionChanged)
        self.pushButton.clicked.connect(self.slotYesBtnClicked)

    def adjustTextPosition(self):
        """用于调整文本框中的文本显示位置，使其与行数对齐"""
        current = self.textEdit_text.verticalScrollBar().value()
        err = current % self.rowHeight
        if current % self.rowHeight != 0:
            value = current + (self.rowHeight - err)
            print("滑块调整后的位置", value)
            self.textEdit_text.verticalScrollBar().setValue(value)

    def slotCursorPositionChanged(self):
        cursor = self.textEdit_text.textCursor()
        col = cursor.columnNumber()
        row = cursor.blockNumber()
        str = self.textEdit_text.document().findBlockByLineNumber(row).text()
        self.setcursorLocationInfo(row + 1, col + 1)

    def setFileNameShow(self, strFileName):
        self.label_fileName.setText(strFileName)

    def setcursorLocationInfo(self, row, col):
        str = f"Ln：{row}  Col：{col}  "
        self.label_locaInfo.setText(str)

    def setCustomContextMenu(self):
        self.textEdit_text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.stdMenu = QMenu(self.textEdit_text)
        setVariableAction = QAction("设置成变量", self.textEdit_text)
        self.stdMenu.addAction(setVariableAction)
        deleteVariableAction = QAction("删除该变量", self.textEdit_text)
        self.stdMenu.addAction(deleteVariableAction)
        self.textEdit_text.customContextMenuRequested.connect(self.showContextMenu)
        setVariableAction.triggered.connect(self.createVaribaleByMouseChoosen)
        deleteVariableAction.triggered.connect(self.deleteVariableByMouseChoosen)

    def showContextMenu(self):
        self.stdMenu.move(self.textEdit_text.cursor().pos())
        self.stdMenu.show()

    def createVaribaleByMouseChoosen(self):
        """将鼠标选择的字段设置成变量"""
        str = self.textEdit_text.textCursor().selectedText()
        if str is not None:
            # TODO 判断此str是否已经定义过变量
            cursor = self.textEdit_text.textCursor()
            col = cursor.columnNumber()
            row = cursor.blockNumber()
            self.dialog_setVariable = Dialog_setVariable(row, col, str)
            self.mask = myMaskWidget(self.parent().parent().parent().parent())
            backgroundWidget = myPublicDialogBackground()
            backgroundWidget.setTitle('设置变量名称及范围')
            backgroundWidget.setWidget(self.dialog_setVariable, True)
            self.mask.layout().addWidget(backgroundWidget)
            self.mask.show()
            self.dialog_setVariable.sendmsg.connect(self.replaceVariableStrAndChangeStyle)

    def deleteVariableByMouseChoosen(self):
        """删除变量"""
        str = self.textEdit_text.textCursor().selectedText()
        if str is not None:
            cursor = self.textEdit_text.textCursor()
            col = cursor.columnNumber()
            row = cursor.blockNumber()
            data = ReadandWriteTemplateConf().data_FECalcuFile
            posList = data.getVariablePosList()
            varList = data.getVariableStr()
            index = 0
            for pos in posList:
                if row == pos[0]:
                    if str == varList[index][1]:
                        if data.designVariable.get(varList[index][0]) is not None:
                            del data.designVariable[varList[index][0]]
                            # 该字段恢复原始样式
                            tcf = QTextCharFormat()
                            tcf.setForeground(Qt.black)
                            tcf.setFont(QFont("Times", self.fontSize))
                            cursor.setCharFormat(tcf)
                index += 1

    def replaceVariableStrAndChangeStyle(self):
        """将设置为变量的字段更改其样式以作区分"""
        cursor = self.textEdit_text.textCursor()
        tcf = QTextCharFormat()
        tcf.setForeground(Qt.blue)
        tcf.setFont(QFont("Times", self.fontSize, QFont.Bold))
        tcf.setFontItalic(True)
        cursor.setCharFormat(tcf)
        cursor.clearSelection()#撤销选中
        cursor.movePosition(QTextCursor.EndOfLine)

    def changeVariableStrStyle(self):
        data = ReadandWriteTemplateConf().data_FECalcuFile
        varPosList = data.getVariablePosList()
        varLen = data.getVariableLength()
        document = self.textEdit_text.document()
        index = 0
        for pos in varPosList:
            self.moveCursorToSpecialLine(pos[0], pos[1])
            tc = self.textEdit_text.textCursor()
            cursorPos = QTextCursor.Left
            for i in range(varLen[index]):
                tc.movePosition(cursorPos, QTextCursor.KeepAnchor, 1)
            self.textEdit_text.setTextCursor(tc)
            if isDebug:
                print(tc.selectedText())
            self.replaceVariableStrAndChangeStyle()
            index += 1

    def moveCursorToSpecialLine(self, row, col):
        tc = self.textEdit_text.textCursor()
        position = self.textEdit_text.document().findBlockByNumber(row).position()
        position = position + col
        tc.setPosition(position, QTextCursor.MoveAnchor)
        self.textEdit_text.setTextCursor(tc)


    def slotYesBtnClicked(self, e):
        self.updateParamShowMsg.emit()
        self.parent().parent().parent().close()

if __name__=="__main__":
    app = QApplication(sys.argv)
    with open("D:\\SoftwareInstall\\HyperWorks2022\hwdesktop\\utility\\MD_Plugin\\MotionView\\DEMO_models\\_Excavator\\_2_Flexibility\\arm_opt.fem", "r") as f:
        test = myTextEdit(f.read())
        test.showContentsInTextEdit()
        test.showRowsInTextEdit()
        test.setFileNameShow("arm_opt.fem")
        test.show()
        app.exec_()