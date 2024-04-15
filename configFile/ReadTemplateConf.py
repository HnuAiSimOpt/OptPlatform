import sys
import os
from xml.dom import minidom
from xml.etree import ElementTree as etree
import threading
from CalculationProcess.CalculationProcessData import *
sys.path.append(os.getcwd())

# 用户选择模板时创建此单例类，同时生成一个新的xml文件，用户存储用户选择的模板。
# 新的xml文件读写类创建

class ReadandWriteTemplateConf(object):
    _instance = None
    _lock = threading.Lock()
    _initFlag = False
    totalTemplateFilePath = sys.path[0].replace('\\', '/') + "/configFile/TotalTemplate.conf"
    usrTemplateFilePath = sys.path[0].replace('\\', '/') + "/configFile/template_usr.conf"

    def __new__(cls, *args, **kw):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        with ReadandWriteTemplateConf._lock:
            if not ReadandWriteTemplateConf._initFlag:
                ReadandWriteTemplateConf._initFlag = True
                self.xmlFile = etree.parse(self.totalTemplateFilePath)
                self.root = self.xmlFile.getroot()  # 模板根节点
                self.new_root = None
                self.data_DOE = DataStruct_DOE() # 验设计参数
                self.data_SensitiveAnalyse = DataStruct_SensitiveAnalyse() # 敏感性分析参数
                self.data_SurrogateModel = DataStruct_SurrogateModel() # 代理模型参数
                self.data_OptimizationAlgorithm = DataStruct_Optimization() # 优化算法参数
                self.data_DataInput = DataStruct_DataInput() # 文件导入
                self.data_FECalcuFile = DataStruct_FiniteElementCalcuFile() #有限元计算文件参数
                self.data_Simulation = DataStruct_Simulation() # 仿真参数
                self.usrChoosnTemplate = None
                self.ProgressBar_calculateCompeletedNum = 0
                self.ProgressBar_curCalculateStep = ''
                self.ProgressBar_isAuto = True

    def getTemplateFromTotalTemplateByName(self, name):
        template = self.root.findall("Template")  # 寻找所有匹配子元素
        template_fit = self.findPointByAttributeValue(template, name)
        tree = etree.ElementTree(template_fit)
        tree.write(self.usrTemplateFilePath, encoding="utf-8", xml_declaration=True)  # 根据选择的模板，创建当前用户模板文件
        self.new_root = tree.getroot()

    # 根据 value(Kriging/LSSVR/......) 在模板中查找对应的参数，并在新建文件的对应 node 中添加子节点
    def addChildPointsByName(self, function, value):
        if function == "surrogateModel":
            #在模板文件中找到对应的参数节点
            paramNodes = self.getSurrogateModelParameters(self.root, value)
            if paramNodes is None:
                print("未查找到对应的代理模型参数:", value)
                pass
            # 在新建文件中将chooseModel节点的value属性值改为 参数value
            node_chooseModel = self.new_root.findall("point/chooseModel")
            if node_chooseModel is None:
                print("未查找到对应的代理模型节点tag:chooseModel")
                pass
            # self.setAttibuteValue(node_chooseModel, "value", value)
            # 将子节点删除
            self.deleteNodebytag(node_chooseModel[0], "param")
            # 将paramNodes添加到新建文件对应的节点下
            if paramNodes is not None:
                for param in paramNodes.findall("param"):
                    node_chooseModel[0].append(param)

        elif function == "optimizationAlgorithm":
            paramNodes = self.getOptimizationAlgorithmParameters(self.root, value)
            if paramNodes is None:
                print("未查找到对应的优化算法参数:", value)
                pass
            node_chooseOptiAlgorithm = self.new_root.findall("point/chooseAlgorithm")
            if node_chooseOptiAlgorithm is None:
                print("未查找到对应的代理模型节点tag:chooseAlgorithm")
                pass
            # self.setAttibuteValue(node_chooseOptiAlgorithm, "value", value)
            self.deleteNodebytag(node_chooseOptiAlgorithm[0], "param")
            if paramNodes is not None:
                for param in paramNodes.findall("param"):
                    node_chooseOptiAlgorithm[0].append(param)

        # 重新保存
        tree = etree.ElementTree(self.new_root)
        tree.write(self.usrTemplateFilePath, encoding="utf-8", xml_declaration=True)

    # 修改属性值
    def setAttibuteValue(self, node, key, value):
        atr = node[0].attrib
        atr[key] = value

    # 通过选择的代理模型名称（LSSVR、Kriging、SVR......）在模板文件中查找对应的参数节点
    def getSurrogateModelParameters(self, root, value):
        nodes_surrogateModel = root.findall("SurrogateModel")
        for node in nodes_surrogateModel:
            if list(node.attrib.values())[0] == value:
                return node
        return None

    # 通过选择的优化算法名称（PSO、GA、DE......）在模板文件中查找对应的参数节点
    def getOptimizationAlgorithmParameters(self, root, value):
        nodes_OptimizationAlgorithm = root.findall("OptimizationAlgorithm")
        for node in nodes_OptimizationAlgorithm:
            if list(node.attrib.values())[0] == value:
                return node
        return None


    def getPointDataInput(self, root):
        return self.findPointByAttributeValue(root, "dataInput")


    #通过代理模型名称获取对应的参数节点
    def getPointSurrogateModelByName(self, name):
        SurrogateModel = self.root.findall("surrogateModel")
        return self.findPointByAttributeValue(SurrogateModel, name)


    # 通过 value 值对应的节点
    def findPointByAttributeValue(self, root, value):
        for child in root:
            attributeValue = list(child.attrib.values())[0]
            if attributeValue == value:
                return child
        return None

    def getValueByKey(self, node, key):
        return node.attrib[key]

    # 获取用户选择模板中，所有的子节点
    def getNewTemplateFileSubNodeName(self, points):
        subNodes = self.new_root.findall("point")
        if subNodes:
            for nodes in subNodes:
                points.append(nodes.attrib.values())

    def isCreatedTemplate(self):
        if self.new_root is not None:
            return True
        else:
            return False

    # 从用户文件中获取参数名字及取值列表
    def getParametersNameAndValuesList(self, namePath):
        """namePath:所需参数在template_usr.conf文件中的路径"""
        parameters = self.new_root.findall(namePath)
        paramlist = []
        allParamters = parameters[0].findall("param")
        for param in allParamters:
            paramlist.append(param.attrib)
        return paramlist

    # 删除子节点
    def deleteNodebytag(self, root, tag):
        children = root.findall(tag)
        for child in children:
            root.remove(child)

    # 获取代理模型名称列表
    def getSurrogateModelNameList(self):
        node_chooseModel = self.new_root.findall("point/chooseModel")
        if len(node_chooseModel) == 1:
            modelAttrib = node_chooseModel[0].attrib
            value = modelAttrib["value"]
            return value
        else:
            return None
    # 获取优化算法名称列表
    def getOptimizationAlgorithmNameList(self):
        node_chooseAlgorithm = self.new_root.findall("point/chooseAlgorithm")
        if len(node_chooseAlgorithm) == 1:
            algorithmAttrib = node_chooseAlgorithm[0].attrib
            value = algorithmAttrib["value"]
            return value
        else:
            return None
    # 获取实验设计名称列表
    def getDOENameList(self):
        node_chooseDOEWay = self.new_root.findall("point/chooseDOEWays")
        if len(node_chooseDOEWay) == 1:
            algorithmAttrib = node_chooseDOEWay[0].attrib
            value = algorithmAttrib["value"]
            return value
        else:
            return None

    # 获取敏感性分析方法名称列表
    def getSensitiveAnalyseNameList(self):
        node_chooseSAWay= self.new_root.findall("point/chooseSAWay")
        if len(node_chooseSAWay) == 1:
            SAAttrib = node_chooseSAWay[0].attrib
            value = SAAttrib["value"]
            return value
        else:
            return None

    # 获取代理模型的默认参数值 以dict返回
    def getSurrogateModelDefaultValue(self):
        defaultValueDict = {}
        node_param = self.new_root.findall("point/chooseModel/param")
        if len(node_param) > 0:
            for node in node_param:
                key = node.attrib["name"]
                value = node.attrib["defaultValue"]
                defaultValueDict[key] = value
        return defaultValueDict

    # 获取优化算法的默认参数值 以dict返回
    def getOptimizationAlgorithmDefaultValue(self):
        defaultValueDict = {}
        node_param = self.new_root.findall("point/chooseAlgorithm/param")
        if len(node_param) > 0:
            for node in node_param:
                key = node.attrib["name"]
                value = node.attrib["defaultValue"]
                defaultValueDict[key] = value
        return defaultValueDict

    # 获取指定路径下的属性值
    def getAttribValueByKeyInPath(self, path, key):
        node = self.new_root.findall(path)
        if node is not None:
            return node[0].attrib[key]
        else:
            return None

if __name__ == "__main__":
    aaa = ReadandWriteTemplateConf()
    aaa.addChildPointsByName("surrogateModel", "LSSVR")

