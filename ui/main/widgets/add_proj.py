# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddProj.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialogButtonBox, QListView, QComboBox
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QPoint
import sys
import os
sys.path.append(os.getcwd())
from ui.main.raw.Ui_add_proj import Ui_Dialog_add_new
from os import path
import icons_rc
from AnalyzeProcessTemplates.public import getBtnStyleString


class AddProj(QtWidgets.QDialog, Ui_Dialog_add_new):
    """添加项目对话框"""
    def __init__(self, parent=None):
        super(AddProj, self).__init__()

        self._OptPlatform = parent
        self.cwd = os.getcwd()
        self.historydir = [self.cwd + "\\temp"]  #TODO 历史路径问题需要重新搞成系统缓存

        self.setupUi(self)
        self.__correct_ui()
        self.__init_signals()

        self.set_proj_name()

    def __correct_ui(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.buttonBox.button(QDialogButtonBox.Ok).setFixedSize(80, 40)
        self.buttonBox.button(QDialogButtonBox.Cancel).setFixedSize(80, 40)
        self.buttonBox.button(QDialogButtonBox.Ok).setStyleSheet(getBtnStyleString())
        self.buttonBox.button(QDialogButtonBox.Cancel).setStyleSheet(getBtnStyleString())
        self.comboBox.addItems(self.historydir)
        self.comboBox.setView(QListView(self))
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def __init_signals(self):
        self.toolButton.clicked.connect(self.get_dir)

    def get_dir(self):
        """获取项目工作路径

        最多显示5个历史设置路径
        """
        dir = QFileDialog.getExistingDirectory(None, "选择文件夹", self.cwd)
        if dir:
            self.historydir.insert(0, dir)
            self.comboBox.clear()
            self.comboBox.addItems(self.historydir)
            self.comboBox.setMaxVisibleItems(5)
        else:
            pass
    
    def set_proj_name(self):
        self.lineEdit.setText("NewProj")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = AddProj()
    ui.show()
    sys.exit(app.exec_())
