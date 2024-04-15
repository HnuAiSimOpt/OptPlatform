from configFile.ReadTemplateConf import *
from PyQt5.QtCore import QObject
import logging
from AnalyzeProcessTemplates.public import *

class GenerateCalcuFile(QObject):
    """"
    根据实验设计结果生成计算文件
    """
    fileContentsList = []
    def __init__(self):
        super(GenerateCalcuFile, self).__init__()
    def do(self):
        """执行：生成计算文件"""
        confFile = ReadandWriteTemplateConf()
        if self.isDataReasonable() == False:
            return
        designVariablePosition = confFile.data_FECalcuFile.getVariablePosList()
        variableLength = confFile.data_FECalcuFile.getVariableLength()
        decimalList = confFile.data_FECalcuFile.getVariableDecimal()
        isSciNotation = confFile.data_FECalcuFile.getIsScientificNotation()
        doeData = confFile.data_DOE.doe_SampleSet
        for index in range(doeData.shape[0]):
            self.replaceVariableValue(doeData[index], designVariablePosition,
                                      variableLength, decimalList, isSciNotation)
            # self.GenerateCalcuFile(index)

    def isDataReasonable(self):
        """
        1、检查CalcuFile中的设计变量设置是否合理
        2、检查实验设计得到的样本点是否与CalcuFile中的变量相符
        """
        # 检查计算文件中的变量设置
        confFile = ReadandWriteTemplateConf()
        variableNum = confFile.data_FECalcuFile.getDesignVariableNum()
        if variableNum == 0:
            logging.getLogger().error("未设置相关变量，请前往FECalcuFile进行设置！")
            return False
        # 检查DOE
        samplingSetVariableNum = confFile.data_DOE.getSamplingSetVariableNum()
        if samplingSetVariableNum == 0:
            logging.getLogger().error("不存在采样数据，请进行相关设置！")
            return False
        # 检查两者的变量数量是否一致
        if samplingSetVariableNum != variableNum:
            logging.getLogger().error("用户设置的变量数与DOE采样的变量数不一致，请检查！")
            return False
        logging.getLogger().info("设计变量与DOE结果检查无异。")
        return True

    @classmethod
    def replaceVariableValue(cls, variableValueList, positionList, strLenList, decimalList, isSciNotationList):
        """
        替换变量值
        :param variableValueList: 变量值list
        :param positionList: 变量值的横纵坐标list
        :param strLenList: 变量的长度list
        :param decimalList: 小数点位数list
        :param isSciNotationList: 是否为科学计数法list
        :return:
        """
        #变量替换
        cls.fileContentsList = ReadandWriteTemplateConf().data_FECalcuFile.contents[:]
        for index in range(variableValueList.shape[0]):
            pos = positionList[index]
            strChange = cls.fileContentsList[pos[0]]
            endPos = pos[1]
            value = translateStringToFloat(strValue=str(variableValueList[index]),
                                           decimal=decimalList[index],
                                           isSciNotation=isSciNotationList[index])
            valueLen = len(value)
            if valueLen < strLenList[index]:
                string = '"{' + ':>' + str(strLenList[index]) + '}".format(' + value + ')'
                value = eval(string)
                valueLen = len(value)
            startPos = pos[1] - valueLen
            strChange = strChange[: startPos] + str(value) + strChange[endPos:]
            cls.fileContentsList[pos[0]] = strChange
            variableValueList[index] = value # 将修改数据格式后的数据存储到doe数据中

    def getAvaliableVariableLength(self, sourceStr, strPos, strLen):
        index = strPos - strLen - 1
        while index >= 0:
            str = sourceStr[index]
            print(str)
            if str != ' ':
                break
            index -= 1
        tmpLen = strPos - index + 1# 要替换的字符串长度及前方空格数相加
        if tmpLen >= 8 and strLen <= 8:
            tmpLen = 8
        elif tmpLen >= 8 and strLen >= 8:
            tmpLen = strLen
        elif tmpLen < 8 and strLen < 8:
            tmpLen = strLen
        return tmpLen

    @classmethod
    def GenerateCalcuFile(cls, index, addPath=''):
        """
        生成可计算文件
        index: 文件序号（在采样样本中的序号）
        """
        data = ReadandWriteTemplateConf().data_FECalcuFile
        filepath = data.filePath
        fileNamePos = filepath.rfind('/') + 1
        fileName = filepath[fileNamePos:]
        if addPath == '':
            newFilePath = filepath[:fileNamePos] + f"rmpod_{index}"
        else:
            newFilePath = filepath[:fileNamePos] + addPath
        if cls().mkdir(newFilePath):
            newFilePath = newFilePath + "/" + fileName
            f = open(newFilePath, "w")
            for index in range(len(cls.fileContentsList)):
                f.writelines(cls.fileContentsList[index]+'\n')
            f.close

    def mkdir(self, path):
        """创建文件路径
        path: 需要创建的文件路径
        return：创建成功返回True, 否则范围False"""
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path) # 创建文件路径
            logging.getLogger().info(f"文件路径：{path} 创建成功。")
            return True
        else:
            # 删除所有子文件及子文件夹
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            # logging.getLogger().info(f"此文件路径已存在:{path}，先删除后后创建")
            return True





