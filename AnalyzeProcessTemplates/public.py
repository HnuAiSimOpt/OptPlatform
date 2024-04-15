import os
import sys
import re
from enum import Enum, unique
sys.path.append(os.getcwd())

isDebug = True if sys.gettrace() else False
maskProgress = None #进度条
progressPercent = 0 #进度

@unique
class FeatureNodesEnum(Enum): # 功能节点
    dataInputBtn = "dataInput" # 数据输入
    doeBtn       = "doe"  # 实验设计
    SimulationBtn= "Sim"  # 仿真计算
    saBtn        = "sa"   # 敏感性分析
    fitBtn       = "fit"  # 建立代理模型
    optBtn       = "opt"  # 优化
    FECalcuFileBtn = "FECalcuFile" #有限元计算文件输入

@unique
class TemplateNameEnum(Enum): # 模板
    Template_doe    = "doe"
    Template_fit    = "fit"
    Template_opt    = "opt"
    Template_opt_FE = "opt_FECalcu"
    Template_sa     = "sa"
    Template_robust = "robust"
    Template_modify = "modify"

@unique
class SolverTypeEnum(Enum):
    LsDyna = "LsDyna"
    Abaqus = "Abaqus"
    Unknow = "unknow"

@unique
class SolverFileTyeEnum(Enum): #结果文件类型
    d3plot = 'd3plot'
    rwforc = 'rwforc'
    odb    = 'odb'
    multi  = 'multi'
    unknow = "unknow"

@unique
class SurrogateModelParamSettingWayEnum(Enum):
    GridSearch = "网格穷尽搜索"              #网格穷尽搜索
    RamdomizedSearch = "随机参数优化"        #随机参数优化
    Customization = "自定义参数"         #自定义

@unique
class ValidationWayEnum(Enum):
    CrossValidation = "交叉验证"
    TestSetValidation = "测试集验证"

@unique
class OutputFunc(Enum):
    Max          = "Maximun"
    Min          = "Minimum"
    Mean         = "Mean"
    Sum          = "Summation"
    First        = "First Element"
    Last         = "Last Element"
    NO           = "None"

def is_number(num):
    """
    判断字符串是否为数字
    """
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True
    else:
        return False

def findDecimalPointPos(strValue:str):
    """
    查找小数点位数
    :param strValue: 数字字符串
    :return: [小数点位数，是否为科学计数法]
    """
    ePos = strValue.find('e')
    isSciNotation = False
    if ePos != -1:
    # 科学计数法
        isSciNotation = True
    decimalPos = strValue.find('.')
    if decimalPos != -1:
        if isSciNotation:
            num = ePos - decimalPos - 1
        else:
            num = len(strValue) - decimalPos -1
        return num, isSciNotation
    return 0, isSciNotation

def translateStringToFloat(strValue, decimal, isSciNotation):
    """
    将字符串转化为指定格式的数字
    :param strValue: 数字字符串
    :param decimal: 保留的小数点位数
    :param isSciNotation: 是否为科学计数法
    :return: 指定格式的数字
    """
    if not isSciNotation:
        string = '"{' + ':.' + str(decimal) + 'f}".format(' + strValue + ')'
        try:
            value = eval(string)
        except:
            value = None
    else:
        string = '"{' + ':.' + str(decimal) + 'e}".format(' + strValue + ')'
        try:
            value = eval(string)
        except:
            value = None
    return value

def printGetInCurrentFunctionName(currentFunc:str, caller:str, isIn:bool):
    """
    打印当前执行函数
    :param currentFunc: 当前执行的函数名
    :param caller: 调用此函数的函数名
    :param isIn: True:进入该函数，False:退出该函数
    :return: 
    """
    if isIn:
        print(f'Entering function --{currentFunc}. The Caller is {caller}')
    else:
        print(f'Exiting function --{currentFunc}. The Caller is {caller}')

def getBtnStyleString():
    hoverFontColor = '#2a3523'
    clickedFontColor = '#2a3523'
    hoverBackgroundColor = '#a4d188'
    clickedBackgroundColor = '#a4d188'
    string = 'QPushButton {font-family: "Microsoft YaHei";' \
             'font-size: 14px;' \
             'font-weight: bold;' \
             'color: #BDC8E2;' \
             'ext-align: center;' \
             'background-color: #2a63bf;' \
             'border-radius: 12px;}'
    string += 'QPushButton:hover{' + \
              f'color: {hoverFontColor}; border-color: {hoverBackgroundColor}; background-color: {hoverBackgroundColor};' +\
              '}'
    string += 'QPushButton:pressed{' + \
              f'color: {clickedFontColor}; border-color: {clickedBackgroundColor}; background-color: {clickedBackgroundColor};' +\
              '}'
    return string

def getLineEditStyleSheet():
    string = "background-color:#434343; border: #434343 1px; color: #BDC8E2;"
    return string

def getWidgetStyleSheet():
    string = 'QWidget{background-color:#434343; border:None}'
    return string

def getQFrameStyleSheet():
    string = 'QFrame{border: 1px solid #535353; background-color:#535353;}'
    return string

def getQcomboBoxStyleSheet():
    string = 'QComboBox{color:#BDC8E2;' \
             'font-size:14px;' \
             'font-family: "Microsoft YaHei";' \
             'padding: 1px 15px 1px 3px;' \
             'border:1px solid #434343;' \
             'border-radius:2px 2px 2px 2px;' \
             'background-color:#434343;}'
    return string

def getQToolButtonStyleSheet():
    string = 'QToolButton{' \
             'outline: none;' \
             'background-color:transparent;' \
             'border: none;' \
             'color: #BDC8E2;' \
             'font-family: "Microsoft YaHei";' \
             'font-size: 14px;' \
             'font-weight: bold;}'
    string += 'QToolButton:hover{' \
              'color: #2a3523;' \
              'background-color: #a4d188;}'
    string += 'QToolButton:pressed{' \
              'color: #2a3523;' \
              'background-color: #a4d188;}'
    string += 'QToolButton:checked{' \
              'color: #2a3523;' \
              'background-color: #a4d188;}'
    return string

def getQLabelStyleSheet(isNeedRadius=True):
    if isNeedRadius:
        string = 'QLabel{background-color:#f4f6e0;'\
                 'color:#262626;'\
                 'font: bold 16px "Microsoft YaHei";'\
                 'padding-left: 10px;'\
                 'border-top-left-radius: 18px;'\
                 'border-top-right-radius: 18px;}'
    else:
        string = 'QLabel{background-color:#f4f6e0;' \
                 'color:#262626;' \
                 'font: bold 16px "Microsoft YaHei";' \
                 'padding-left: 10px;' \
                 'border-top-left-radius: 0px;' \
                 'border-top-right-radius: 0px;}'
    return string

def getCanvasToolBtnStyleSheet():
    hoverFontColor = '#40444e'
    clickedFontColor = '#40444e'
    hoverBackgroundColor = '#40444e'
    clickedBackgroundColor = '#40444e'
    string = 'QPushButton {font-family: "Microsoft YaHei";' \
             'font-size: 14px;' \
             'font-weight: bold;' \
             'color: #ffffff;' \
             'ext-align: center;' \
             'background-color: transparent;' \
             'border-radius: 4px;}'
    string += 'QPushButton:hover{' + \
              f'color: {hoverFontColor}; background-color: {hoverBackgroundColor};' + \
              'border-radius: 4px; border: 1px solid #ffffff;}'
    string += 'QPushButton:pressed{' + \
              f'color: {clickedFontColor}; background-color: {clickedBackgroundColor};' + \
              'border-radius: 4px; border: 1px solid #ffffff;}'
    return string

def getResultFileType(filePath:str):
    if filePath.__contains__('/'):
        pos = filePath.rfind('/')
        fileName = filePath[pos + 1:]
    else:
        fileName = filePath

    if fileName.__contains__('.'):
        pos = fileName.rfind('.')
        suffix = fileName[pos + 1:]
    else:
        suffix = fileName

    if suffix == SolverFileTyeEnum.rwforc.value:
        return SolverFileTyeEnum.rwforc
    elif suffix == SolverFileTyeEnum.d3plot.value:
        return SolverFileTyeEnum.d3plot
    elif suffix == SolverFileTyeEnum.odb.value:
        return SolverFileTyeEnum.odb
    else:
        return SolverFileTyeEnum.unknow

def getTrainyData():
    """
    获取训练数据集
    :return:
    """
    from configFile.ReadTemplateConf import ReadandWriteTemplateConf
    template = ReadandWriteTemplateConf().usrChoosnTemplate
    trainy_x = None
    trainy_y = None
    trainy_x_namelist = None
    trainy_y_namelist = None
    if template == TemplateNameEnum.Template_opt_FE.value:
        trainy_x = ReadandWriteTemplateConf().data_DOE.doe_SampleSet
        trainy_y = ReadandWriteTemplateConf().data_DOE.doe_ResponseSet
        trainy_x_namelist = ReadandWriteTemplateConf().data_DOE.getVariableName() # 训练集的变量名
        trainy_y_namelist = ReadandWriteTemplateConf().data_DOE.doe_ResponseName # 训练集的响应值的名称
    if template == TemplateNameEnum.Template_opt.value:
        trainy_x = ReadandWriteTemplateConf().data_DataInput.DataFile_TrainingSet_x
        trainy_y = ReadandWriteTemplateConf().data_DataInput.DataFile_TrainingSet_y
        trainy_x_namelist = ReadandWriteTemplateConf().data_DataInput.DataFile_VariableNameList  # 训练集的变量名
        trainy_y_namelist = ReadandWriteTemplateConf().data_DataInput.DataFile_OutputNameList  # 训练集的响应值的名称
    return trainy_x, trainy_y, trainy_x_namelist, trainy_y_namelist