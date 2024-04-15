# -*- coding: utf-8 -*-
import os
import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QDockWidget, QComboBox, QListView
from PyQt5.QtCore import QRect, Qt
from ui.main.raw.Ui_CreateProj import Ui_CreateProj

class CreateProj(QWidget, Ui_CreateProj):
    def __init__(self, parent=None):
        super(CreateProj, self).__init__(parent)
        self.setupUi(self)
        self.__initUI__()

    def __initUI__(self):
        # self.Btn_CreateNewProj.setStyleSheet("border:None; text-aligm:left; background-color:transparent")
        # self.Btn_CreateNewProj_icon.setStyleSheet("border:None; background-color:transparent")
        # self.Btn_OpenFile.setStyleSheet("border:None; text-aligm:left; background-color:transparent")
        # self.Btn_OpenFile_icon.setStyleSheet("border:None; background-color:transparent")
        # self.Btn_OpenProj.setStyleSheet("border:None; text-aligm:left; background-color:transparent")
        # self.Btn_OpenProj_icon.setStyleSheet("border:None; background-color:transparent")
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())