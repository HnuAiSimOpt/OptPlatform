import numpy as np
from AnalyzeProcessTemplates.public import SolverTypeEnum

class DataStruct_DOE():
    """doe 实验设计"""
    def __init__(self):
        self.doe_Method = None #实验设计方法
        self.doe_VariablesNum = 0 #变量个数
        self.doe_VariablesValueRange = {} #变量取值范围
        self.doe_SampleSize = 0 #样本数量
        self.doe_SampleSet = None #采样数据
        self.doe_ResponseSet = None #采样数据的响应值（根据实际的计算而来）
        self.doe_ResponseName = [] # 响应值名称

    """ 判断此数据结构是否为空"""
    def isEmpty(self):
        if (self.doe_Method is None) or (self.doe_SampleSize == 0) or (self.doe_VariablesValueRange is None) or (self.doe_SampleSize == 0):
            return True
        else:
            return False

    def getSamplingSetVariableNum(self):
        if self.doe_Method is not None:
            if isinstance(self.doe_SampleSet, np.ndarray):
                return self.doe_SampleSet.shape[1]
        return 0

    def isSamplingComplete(self):
        """是否采样完成"""
        if isinstance(self.doe_SampleSet, np.array) and self.doe_SampleSize > 0:
            return True
        else:
            return False


    def updateVariableRangeLowByName(self, name, lowValue):
        range =  self.doe_VariablesValueRange.get(name)
        if range is not None:
            range[0] = lowValue

    def updateVariableRangeUpByName(self, name, upValue):
        range = self.doe_VariablesValueRange.get(name)
        if range is not None:
            range[1] = upValue

    def getVariableName(self):
        """
        获取采样数据的变量名称列表
        :return: list of variables name
        """
        namelist = []
        for key in self.doe_VariablesValueRange.keys():
            namelist.append(key)
        return namelist

    """ 将此数据结构清空"""
    def clear(self):
        self.doe_Method = None
        self.doe_VariablesNum = 0
        self.doe_VariablesValueRange = {}
        self.doe_SampleSize = 0
        self.doe_SampleSet = None
        self.doe_ResponseSet = None
        self.doe_ResponseName = []

class DataStruct_SensitiveAnalyse():
    """敏感性分析"""
    def __init__(self):
        self.SA_Name = "" #敏感性分析方法的名称
        self.SA_Result = None #敏感性分析结果

    def clear(self):
        self.SA_Name = ""
        self.SA_Result = None

class DataStruct_SurrogateModel():
    """SurrogateModel 代理模型"""
    def __init__(self):
        self.SM_ModelName = ""  # 模型名称 例如：Kriging
        self.SM_ModelParamSettingWays = None # 模型参数设置方式
        self.SM_Params = {}  # 模型参数 例如：{”相关模型“：高斯}
        self.SM_Model = {} # 拟合得到的模型字典{'name': model}（可能是多个模型）
        self.SM_ValidationWays = None  # 模型验证方法：1、交叉验证； 2、验证集验证
        self.SM_ValidationParams = {}  # 交叉验证用到此参数，{”交叉验证方法“：参数}。交叉验证方法包括：Holdout Method；K-Fold CV；Leave One out CV；Bootstrap Methods
        self.SM_TrainyData = [] # [变量数据, 输出数据, 变量名list, 输出名list]

    def isEmpty(self):
        if (self.SM_ModelName == "") and (self.SM_ValidationWays == None) and (self.SM_ModelParamSettingWays == None):
            return True
        else:
            return False

    def clear(self):
        self.SM_ModelName = ""
        self.SM_Params = {}
        self.SM_Model = {}
        self.SM_ValidationWays = None
        self.SM_ValidationParams = {}
        self.SM_ModelParamSettingWays = None

class DataStruct_Optimization():
    """optimizaztion 优化算法"""
    def __init__(self):
        self.Opt_AlgorithmName = "" # 优化算法名称 例如 PSO、GA、DE
        self.Opt_AlgorithmParams = {} # 优化算法参数 例如：{"粒子数"：100}
        self.Opt_AlgorithmProblem_target = {} #优化问题_优化目标
        self.Opt_AlgorithmProblem_constrains = {} #优化问题_约束
        self.Opt_AlgorithmProblem_variUpLow = {} #优化问题_变量上下限
        self.Opt_AlgorithmProblem_variNameList = [] #变量名
        self.Opt_AlgorithmResult = None # 计算结果

    def isEmpty(self):
        if (self.Opt_AlgorithmName == '') and (not self.Opt_AlgorithmParams):
            return True
        else:
            return False

    def isAlgorithmProblemDefined(self) -> bool:
        """优化问题是否已经定义完成"""
        if self.Opt_AlgorithmProblem_target and self.Opt_AlgorithmProblem_variUpLow:
            return True
        return False

    def clear(self):
        self.Opt_AlgorithmName = ""
        self.Opt_AlgorithmParams = {}
        self.Opt_AlgorithmProblem_target = {}
        self.Opt_AlgorithmProblem_constrains = {}
        self.Opt_AlgorithmProblem_variUpLow = {}
        self.Opt_AlgorithmProblem_variNameList = []
        self.Opt_AlgorithmResult = None
        self.Opt_AlgorithmProblem = None

class DataStruct_DataInput():
    """ dataInput 数据输入"""
    def __init__(self):
        self.DataFile_Path = "" # 训练集文件路径
        self.DataFile_TrainyDataSheetName = ''  # 训练集sheetName
        self.DataFile_TestPath = "" # 测试集文件路径
        self.DataFile_TestDataSheetName = '' # 测试集sheetName
        self.DataFile_VariableNum = 0 # 训练集变量个数
        self.DataFile_OutputNum = 0 # 训练集输出数量
        self.DataFile_SampleNum = 0 # 训练集样本数量
        self.DataFile_TrainingSet_x = None # 训练集x
        self.DataFile_TrainingSet_y = None # 训练集y
        self.DataFile_TestSet_x = None # 测试集x
        self.DataFile_TestSet_y = None # 测试集y
        self.DataFile_TestSetVariableNum = 0 # 测试集变量数
        self.DataFile_TestSetOutputNum = 0 # 测试集输出数
        self.DataFile_TestSetSampleNum = 0 # 测试集样本数
        self.DataFile_TrainyData = None
        self.DataFile_TestData = None
        self.DataFile_VariableNameList = [] #变量名称
        self.DataFile_OutputNameList = [] #输出值名称
        self.DataFile_VariableRange = {} #变量范围

    def isEmpty(self):
        if (self.DataFile_OutputNum == 0) and (self.DataFile_Path == "") \
                and (self.DataFile_VariableNum == 0) and (self.DataFile_SampleNum == 0):
            return True
        else:
            return False

    def isExistTrainingData(self):
        if (self.DataFile_TrainingSet_x is not None) and (self.DataFile_TrainingSet_y is not None):
            return True
        else:
            return False

    def isExistTestData(self):
        if (self.DataFile_TestSet_x is not None) and (self.DataFile_TestSet_y is not None ):
            return True
        else:
            return False

    def clear(self):
        self.DataFile_Path = ""
        self.DataFile_VariableNum = 0
        self.DataFile_OutputNum = 0
        self.DataFile_SampleNum = 0
        self.DataFile_TrainingSet_x = None
        self.DataFile_TrainingSet_y = None
        self.DataFile_TestSet_x = None
        self.DataFile_TestSet_y = None
        self.DataFile_TestSetVariableNum = 0
        self.DataFile_TestSetOutputNum = 0
        self.DataFile_TestSetSampleNum = 0
        self.DataFile_TrainyData = None
        self.DataFile_TestData = None
        self.DataFile_VariableNameList = []
        self.DataFile_OutputNameList = []
        self.DataFile_TrainyDataSheetName = ''
        self.DataFile_TestPath = ""
        self.DataFile_VariableRange = {}

class DataStruct_FiniteElementCalcuFile():
    def __init__(self):
        self.filePath = "" # 计算文件的路径
        self.contents = None # 文件内容
        self.designVariable = {} #设计变量 {变量名：[[lowvalue, upvalue], [row, col], str]} 变量下限、变量上限、变量值在源文件中的行、列、str
        self.responseValue = {} #响应值的计算方式
        self.isTryCalcuCompeleted = False #是否已经完成试计算
        self.resultFileList = [] #试计算完成后，文件夹中的结果文件列表

    def isEmpty(self):
        if self.filePath == "" or self.contents is None:
            return True
        else:
            return False

    def getDesignVariableNum(self):
        return len(self.designVariable)

    def getVariablePosList(self):
        posList = []
        for key, value in self.designVariable.items():
            posList.append(value[1])
        return posList

    def getVariableStr(self):
        strVar = []
        for key, value in self.designVariable.items():
            strVar.append([key, value[2]])
        return strVar

    def getVariableLength(self):
        strLen = []
        for key, value in self.designVariable.items():
            strLen.append(len(value[2]))
        return strLen

    def getVariableDecimal(self):
        decimal = []
        for key, value in self.designVariable.items():
            decimal.append(value[3])
        return decimal

    def getIsScientificNotation(self):
        isSciNotation = []
        for key, value in self.designVariable.items():
            isSciNotation.append(value[4])
        return isSciNotation

    def getDesignVariableRangeByParamName(self, name):
        value = self.designVariable.get(name)
        if value is not None:
            if len(value) == 5:
                return value[0]

    def getDesignVariablePositionByParamName(self, name):
        value = self.designVariable.get(name)
        if value is not None:
            if len(value) == 5:
                return value[1]

    def getDesignVariableOriginalValueByParamName(self, name):
        value = self.designVariable.get(name)
        if value is not None:
            if len(value) == 5:
                return value[2]

    def changeDesignVariableRangeByParamName(self, name, range):
        if isinstance(range, list):
            if len(range) == 2:
                value = self.designVariable.get(name)
                if value is not None:
                    if len(value) == 5:
                        value[0] = range
            else:
                print(f"输入的数据结构错误: {range}")
        else:
            print(f"输入的数据结构错误: {range}")

    def changeDesignVariableLowByParamName(self, name, low):
        value = self.designVariable.get(name)
        if value is not None:
            if len(value) == 5:
                value[0][0] = low

    def changeDesignVariableUpByParamName(self, name, up):
        value = self.designVariable.get(name)
        if value is not None:
            if len(value) == 5:
                value[0][1] = up

    def clear(self):
        self.filePath = ""  # 计算文件的路径
        self.contents = None  # 文件内容
        self.designVariable = {}  # 设计变量 {变量名：[[lowvalue, upvalue], [row, col], str]} 变量下限、变量上限、变量值在源文件中的行、列、str
        self.responseValue = {}  # 响应值的计算方式
        self.isTryCalcuCompeleted = False  # 是否已经完成试计算
        self.resultFileList = []

class DataStruct_Simulation():
    def __init__(self):
        self.solver = SolverTypeEnum.Unknow #求解器
        self.cmd = "" # 执行有限元计算的命令
        self.NProcessor = 1 # 进程数
        self.NCPU = 1
        self.folderPath = "" # 文件夹路径
        self.fileName = '' # 文件名
    def clear(self):
        self.solver = SolverTypeEnum.Unknow
        self.cmd == ""
        self.NProcessor = 1
        self.folderPath = ""
        self.NCPU = 1
        self.fileName = ''