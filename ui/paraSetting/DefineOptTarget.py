from ui.paraSetting.ui.Ui_DefineOptTarget import Ui_Form
from PyQt5.QtWidgets import QWidget, QRadioButton, QComboBox, QButtonGroup, QListView
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from AnalyzeProcessTemplates.public import TemplateNameEnum

class DefineOptTarget(QWidget, Ui_Form):
    def __init__(self, parent, expression='', func=''):
        super(DefineOptTarget, self).__init__(parent)
        self.setupUi(self)
        self.__initUI__(expression, func)
        self.__initConnect__()

    def __initUI__(self, expression, func):
        self.myRadioBtnGroup = QButtonGroup(self)
        self.myRadioBtnGroup.addButton(self.rB_defineByResponseValue, 0)
        self.myRadioBtnGroup.addButton(self.rB_defineByUsr, 1)
        temp = ReadandWriteTemplateConf().usrChoosnTemplate
        if temp == TemplateNameEnum.Template_opt_FE.value:
            response = ReadandWriteTemplateConf().data_FECalcuFile.responseValue
            for key in response.keys():
                self.cbb_responseValue.addItem(key)
        elif temp == TemplateNameEnum.Template_opt.value:
            response = ReadandWriteTemplateConf().data_DataInput.DataFile_OutputNameList
            self.cbb_responseValue.addItems(response)
        self.cbb_func.addItems(['MIN', 'MAX'])
        self.cbb_func_2.addItems(['MIN', 'MAX'])
        if expression == '':
            self.rB_defineByResponseValue.setChecked(True)
        else:
            self.rB_defineByUsr.setChecked(True)
            self.textEdit_expression.setText(expression)
            self.cbb_func_2.setCurrentText(func)
            self.stackedWidget.setCurrentIndex(1)
        self.setStyleSheet('background-color:transparent')
        qcomboboxList = self.findChildren(QComboBox)
        for cbb in qcomboboxList:
            cbb.setView(QListView())

    def __initConnect__(self):
        self.rB_defineByResponseValue.toggled.connect(self.slotRadioButtonChecked)
        self.rB_defineByUsr.toggled.connect(self.slotRadioButtonChecked)
        self.cbb_responseValue.activated.connect(self.constructOptTarget)
        self.cbb_func.activated.connect(self.constructOptTarget)
        self.cbb_func_2.activated.connect(self.constructOptTarget)

    def slotRadioButtonChecked(self):
        if self.myRadioBtnGroup.checkedId() == 0:
            self.stackedWidget.setCurrentIndex(0)
        if self.myRadioBtnGroup.checkedId() == 1:
            self.stackedWidget.setCurrentIndex(1)

    def constructOptTarget(self):
        """
        构造优化目标
        :return: [表达式, 函数]
        """
        if self.stackedWidget.currentIndex() == 0 and\
                self.myRadioBtnGroup.checkedId() == 0:
            responseName = self.cbb_responseValue.currentText()
            func = self.cbb_func.currentText()
            return responseName, func
        else:
            expression = self.textEdit_expression.toPlainText()
            func = self.cbb_func_2.currentText()
            return expression, func
        return None

    def checkExpressionCorrectness(self) -> bool:
        """
        检查表达式的正确性
        :return: 正确返回True, 错误返回False
        """
        pass

    def setUsr(self):
        self.rB_defineByResponseValue.setCheckable(False)
        self.rB_defineByUsr.setChecked(True)

    def changeSize(self, width, height) -> None:
        self.setFixedWidth(width)
        self.setFixedHeight(height)