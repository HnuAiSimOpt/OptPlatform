import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from ui.main.widgets.optplatform import OptPlatform
import sys
import icons_rc


if __name__ == "__main__":
    print(sys.setrecursionlimit(2000))
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 适应高分辨率
    app = QtWidgets.QApplication(sys.argv)
    with open("qss/darkStyle.qss", encoding="utf-8") as f:
        style = f.read()
    app.setStyleSheet(style)
    ui = OptPlatform()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/pic/icons/软件icon.png"),  QtGui.QIcon.Normal, QtGui.QIcon.Off)
    ui.setWindowIcon(icon)
    ui.show()
    sys.exit(app.exec_())
