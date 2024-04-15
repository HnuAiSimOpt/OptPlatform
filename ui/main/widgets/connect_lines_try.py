from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialogButtonBox, QListView, QPushButton, QWidget
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QPoint, Qt
import sys
import os
sys.path.append(os.getcwd())
from ui.main.raw.Connect_lines_try import Ui_Connnect_Lines
import ui.main.widgets.connect_lines as lllines

class ConnectButtonByLines(QWidget):
    def __init__(self, parent=None):
        super(ConnectButtonByLines, self).__init__(parent, Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.button1 = QPushButton("按钮1", self)
        self.button1.setGeometry(100, 100, 100, 30)

        self.button2 = QPushButton("按钮2", self)
        self.button2.setGeometry(400, 300, 100, 30)

        self.connectWidget = lllines.DragWidget((100+100, 100+10), (400, 300+10), self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ConnectButtonByLines()
    ui.show()
    app.exec_()