from PublicTool.ui.Ui_publicDialogBackground import Ui_maskWidgetBackground
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtGui import QPainter, QPen, QBrush, QPainterPath
from AnalyzeProcessTemplates.public import getWidgetStyleSheet
from AnalyzeProcessTemplates.public import getQLabelStyleSheet

class myPublicDialogBackground(QWidget, Ui_maskWidgetBackground):
    def __init__(self):
        super(myPublicDialogBackground, self).__init__()
        self.setupUi(self)
        self.__initUI__()

    def __initUI__(self):
        self.label_title.setStyleSheet(getQLabelStyleSheet())
        self.widget.setStyleSheet('QWidget{background-color:#434343;}')

    def setTitle(self, strTitle):
        self.label_title.setText(strTitle)

    def setWidget(self, widget, isLimitSize=False):
        layout = QHBoxLayout()
        layout.addWidget(widget)
        if isLimitSize:
            height = widget.height()
            width = widget.width()
            self.label_title.setFixedWidth(width)
            self.label_title.setFixedHeight(40)
            self.widget.setFixedWidth(width)
            self.widget.setFixedHeight(height)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.widget.setLayout(layout)