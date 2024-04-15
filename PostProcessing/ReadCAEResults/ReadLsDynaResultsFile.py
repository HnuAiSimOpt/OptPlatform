from PyQt5.QtCore import QObject
from lasso.dyna import D3plot, ArrayType, FilterType
import numpy as np
import logging
from enum import Enum, unique
from AnalyzeProcessTemplates.public import OutputFunc
from PyQt5.QtCore import Qt, pyqtSignal, QVariant
import threading

class ReadLsDynaResultsFile(QObject):
    myD3plot = None
    currentFilePath = ''
    _instance = None
    _lock = threading.Lock()
    _initFlag = False

    def __init__(self, filepath=''):
        with ReadLsDynaResultsFile._lock:
            if not ReadLsDynaResultsFile._initFlag:
                ReadLsDynaResultsFile._initFlag = True
                self.loadResultFile(filepath)

    def __new__(cls, *args, **kw):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def clear(self):
        del self.myD3plot

    def loadResultFile(self, filepath):
        if filepath == '':
            return False
        if filepath == self.currentFilePath:
            if self.myD3plot is not None:
                return True
            else:
                return False
        self.myD3plot = D3plot(filepath)
        if self.myD3plot is not None:
            self.currentFilePath = filepath
            self.getBadStep()
        return True

    def clear(self):
        del self.myD3plot

    def getNodeList(self, strElementType):
        """根据单元类型找到对应的单元节点"""
        if strElementType == FilterType.SHELL: #如果是壳单元
            self.myD3plot.arrays[ArrayType.element_shell_node_indexes]

    def getAllNodeNum(self):
        """
        功能：获取所有的节点编号
        :return: 节点编号
        """
        return self.myD3plot.arrays[ArrayType.node_ids]

    def getAllShellNum(self):
        return self.myD3plot.arrays[ArrayType.element_shell_ids]

    def getAllSolidNum(self):
        return self.myD3plot.arrays[ArrayType.element_solid_ids]

    def getAllPartTitles(self):
        return self.myD3plot.arrays[ArrayType.part_titles]

    def getAllPartTitlesIDs(self):
        return self.myD3plot.arrays[ArrayType.part_titles_ids]

    def getBadStep(self):
        """获取没有结果的迭代步"""
        timestep = self.myD3plot.arrays[ArrayType.global_timesteps]
        index = np.where(timestep <= -999999.00000)
        self.badStep = index[0]

    def getNodeDisplacementByNodeNum(self, NodeNum):
        """
        功能：返回节点编号对应节点的位移
        参数：NodeNum: 节点编号
        返回值: list of node displacement [[dis_x, dis_y, dis_z] 。。。。。。]
        """
        nodePos = np.where(self.myD3plot.arrays[ArrayType.node_ids] == int(NodeNum))
        nodeDisplacement = self.myD3plot.arrays[ArrayType.node_displacement]
        displacementListofNode = self.getNodeResultArrayAndAddMagnitude(nodeDisplacement, nodePos[0])
        return displacementListofNode

    def getNodeVelocityByNodeNum(self, NodeNum):
        """
        功能： 返回节点编号对应节点的速度
        :param NodeNum:节点编号
        :return:list of node velocity [[v_x, v_y, v_z] ......]
        """
        nodePos = np.where(self.myD3plot.arrays[ArrayType.node_ids] == int(NodeNum))
        nodeVelocity = self.myD3plot.arrays[ArrayType.node_velocity]
        velocityListofNode = self.getNodeResultArrayAndAddMagnitude(nodeVelocity, nodePos[0])
        return velocityListofNode

    def getNodeAccelerationByNodeNum(self, NodeNum):
        """
        功能：获取节点编号对应节点的加速度
        :param NodeNum: 节点编号
        :return: list of node acceleration [[a_x, a_y, a_z] ......]
        """
        nodePos = np.where(self.myD3plot.arrays[ArrayType.node_ids] == int(NodeNum))
        nodeAcceleration = self.myD3plot.arrays[ArrayType.node_acceleration]
        accelerationListofNode = self.getNodeResultArrayAndAddMagnitude(nodeAcceleration, nodePos[0])
        return accelerationListofNode

    def getShellElementStressByID(self, ShellID):
        """
        功能：获取shellID对应的shell单元的应力
        :param shellID: 壳单元的编号
        :return: list of shell element stress [[6×6] 。。。。。。]
        """
        shellPos = np.where(self.myD3plot.arrays[ArrayType.element_shell_ids] == int(ShellID))
        shellStress = self.myD3plot.arrays[ArrayType.element_shell_stress]
        if len(shellPos) > 0:
            stressListofShell = self.getElementResultArrayAndAddVonMises(shellStress, shellPos[0])
            return stressListofShell
        return None

    def getSolidElementStressByID(self, SolidID):
        """
        功能：获取SolidID对应的Solid单元的应力
        :param SolidID: 实体单元的编号
        :return: list of solid element stress
        """
        solidPos = np.where(self.myD3plot.arrays[ArrayType.element_solid_ids] == int(SolidID))
        solidStress = self.myD3plot.arrays[ArrayType.element_solid_stress]
        stressdListofSolid = self.getElementResultArrayAndAddVonMises(solidStress, solidPos[0])
        return stressdListofSolid

    def getShellElementStrainByID(self, ShellID):
        """
        功能：获取shellID对应的shell单元的应变
        :param shellID: 壳单元的编号
        :return: list of shell element strain [[2×6] 。。。。。。]  LOWER UPPER
        """
        shellPos = np.where(self.myD3plot.arrays[ArrayType.element_shell_ids] == int(ShellID))
        shellStrain = self.myD3plot.arrays[ArrayType.element_shell_strain]
        strainListofShell = self.getElementResultArrayAndAddVonMises(shellStrain, shellPos[0])
        return strainListofShell

    def getSolidElementStrainByID(self, SolidID):
        """
        功能：获取SolidID对应的Solid单元的应变
        :param SolidID: 实体单元的编号
        :return: list of solid element strain
        """
        solidPos = np.where(self.myD3plot.arrays[ArrayType.element_solid_ids] == int(SolidID))
        solidStrain = self.myD3plot.arrays[ArrayType.element_solid_strain]
        straindListofSolid = self.getElementResultArrayAndAddVonMises(solidStrain, solidPos[0])
        return straindListofSolid

    def getShellInternalEnergyByID(self, ShellID):
        """
        功能：获取ShellID对应的壳单元的internel_energy
        :param ShellID: 壳单元ID
        :return: list of shell internal energy
        """
        shellPos = np.where(self.myD3plot.arrays[ArrayType.element_shell_ids] == int(ShellID))
        shellInternalEnergy = self.myD3plot.arrays[ArrayType.element_shell_internal_energy]
        internalEnergyListofShell = []
        for index in range(shellInternalEnergy.shape[0]):
            if not self.badStep.__contains__(index):
                internalEnergyListofShell.append(shellInternalEnergy[index][shellPos[0][0]])
        return internalEnergyListofShell

    def getPartInternalEnergy(self, partID):
        """
        功能：获取partID对应的部件的内能
        :param partID:
        :return:
        """
        partInternalEnergy = self.myD3plot.arrays[ArrayType.part_internal_energy]
        totalInternalEnergy = np.sum(partInternalEnergy, axis=1)
        InternalEnergyArray = np.c_[partInternalEnergy, totalInternalEnergy]
        internalEnergyListofPart = list(InternalEnergyArray[:, int(partID)])
        return internalEnergyListofPart

    def getPartKineticEnergy(self, partID):
        """
        功能：获取partID对应的部件的动能
        :param partID:
        :return:
        """
        partKineticEnergy = self.myD3plot.arrays[ArrayType.part_kinetic_energy]
        totalKineticEnergy = np.sum(partKineticEnergy, axis=1)
        KineticEnergyArray = np.c_[partKineticEnergy, totalKineticEnergy]
        kineticEnergyListofPart = list(KineticEnergyArray[:, int(partID)])
        return kineticEnergyListofPart

    def getPartMassByID(self, partID):
        """
        功能：获取partID对应的部件的质量
        :param partID:
        :return:
        """
        partMass = self.myD3plot.arrays[ArrayType.part_mass]
        totalMass = np.sum(partMass, axis=1)
        massArray = np.c_[partMass, totalMass]
        return list(massArray[:, int(partID)])

    def getElementResultArrayAndAddVonMises(self, arrays, elementPos):
        """根据指定位置的xx,yy,zz方向上的数据计算vonMises"""
        if (elementPos.ndim <= 0) or (arrays.ndim < 2):
            return None
        strainListofShell = []
        tmpnum = arrays.shape[0] # 时间步
        for index in range(tmpnum):
            if not self.badStep.__contains__(index):
                try:
                    print(elementPos.astype(np.int_)[0])
                except:
                    pass
                value = arrays[index][elementPos.astype(np.int_)[0]] # 指定时间步、单元位置
                tmpnum = value.shape[0] #单个时间步下，某个单元的结果集的行数
                vonMisesArray = np.empty([tmpnum, 1], dtype=float)
                for index in range(tmpnum):
                    vonMisesArray[index] = self.getVonMises(value[index, 0:6])
                value = np.concatenate([value, vonMisesArray], axis=1)
                strainListofShell.append(value)
        return strainListofShell

    def getNodeResultArrayAndAddMagnitude(self, array, nodePos):
        accelerationListofNode = []
        startValue = array[0][nodePos.astype(np.int_)[0]]
        for index in range(array.shape[0]):
            if not self.badStep.__contains__(index):
                value = array[index][nodePos.astype(np.int_)[0]] - startValue
                mag = self.getMagnitude(value)
                value = np.append(value, mag)
                accelerationListofNode.append(value)
        return accelerationListofNode

    def getMagnitude(self, listValue):
        """
        功能：计算三维矢量幅度
        :param listValue: 三维矢量
        :return: 幅度值
        """
        if isinstance(listValue, np.ndarray):
            listValue = listValue.tolist()
        if len(listValue) != 3:
            return None
        sum = 0
        for index in range(len(listValue)):
            sum += listValue[index] ** 2
        magnitude = np.sqrt(sum)
        return magnitude

    def getVonMises(self, listValue):
        """
        功能：求解 von Mises 等效应力/应变
        :param listValue:
        :return:
        """
        if len(listValue) != 6:
            return None
        value = (listValue[0] - listValue[1]) ** 2
        value += (listValue[1] - listValue[2]) ** 2
        value += (listValue[2] - listValue[0]) ** 2
        value += 6 * (listValue[3] ** 2 + listValue[4] ** 2 + listValue[5] ** 2)
        vonMises = np.sqrt(value) / np.sqrt(2)
        return vonMises

    def getOutputValueByParameters(self, dictParameters: dict):
        solver = dictParameters.get("solver")
        outputType = dictParameters.get("outputType")
        position = dictParameters.get("position")
        outputForm = dictParameters.get("outputForm")
        outputFunc = dictParameters.get("outputFunc")
        if (solver is None) or (position is None) or (outputType is None) or (outputForm is None):
            logging.getLogger().error("输出定义不完整，请重新定义")
            return
        outputData = self.getOutputDataByTypeandPosition(outputType, position)
        outputData = np.array(outputData)
        currentData = self.getCurrentDataByOutputForm(outputData, outputForm)
        if outputFunc is not None:
            targetValue = self.getTargetValueByOutputFunc(currentData, outputFunc)
            if targetValue is not None:
                return targetValue[1]
            else:
                return None
        else:
            return currentData

    def getOutputDataByTypeandPosition(self, outputType, position):
        """
        根据指定的输出类型及位置，获取结果
        :param outputType: 输出类型
        :param position: 位置
        :return: 结果集
        """
        if isinstance(position, str):
            if position[0] == 'N' or position[0] == 'E':
                position = position[1:]
        if outputType == ArrayType.node_displacement:
            return self.getNodeDisplacementByNodeNum(int(position))
        elif outputType == ArrayType.node_velocity:
            return self.getNodeVelocityByNodeNum(int(position))
        elif outputType == ArrayType.node_acceleration:
            return self.getNodeAccelerationByNodeNum(int(position))
        elif outputType == ArrayType.element_shell_stress:
            return self.getShellElementStressByID(int(position))
        elif outputType == ArrayType.element_shell_strain:
            return self.getShellElementStrainByID(int(position))
        elif outputType == ArrayType.element_solid_stress:
            return self.getSolidElementStressByID(int(position))
        elif outputType == ArrayType.element_solid_strain:
            return self.getSolidElementStrainByID(int(position))
        elif outputType == ArrayType.element_shell_internal_energy:
            return self.getShellInternalEnergyByID(int(position))
        elif outputType == ArrayType.global_timesteps:
            return self.myD3plot.arrays[ArrayType.global_timesteps]
        elif outputType == ArrayType.global_internal_energy:
            return self.myD3plot.arrays[ArrayType.global_internal_energy]
        elif outputType == ArrayType.global_kinetic_energy:
            return self.myD3plot.arrays[ArrayType.global_kinetic_energy]
        elif outputType == ArrayType.global_total_energy:
            return self.myD3plot.arrays[ArrayType.global_total_energy]
        elif outputType == ArrayType.part_internal_energy:
            return self.getPartInternalEnergy(int(position)) #需要添加总内能
        elif outputType == ArrayType.part_kinetic_energy:
            return self.getPartKineticEnergy(int(position)) #需要添加总动能
        elif outputType == ArrayType.part_mass:
            return self.getPartMassByID(int(position)) #todo 需要添加总质量
        else:
            return None

    def getCurrentDataByOutputForm(self, outputData, index):
        """
        根据输出形式获取对应的响应值
        :param OutputData: 指定类型及位置的结果集
        :param index: 输出形式的index
        :return: 指定输出形式的结果
        """
        if (index == -1) or (outputData.ndim == 0):
            return None
        shape = outputData.shape
        if len(shape) == 3:
            index_row = index // shape[2]
            index_col = index % shape[2]
            return outputData[:, index_row, index_col]
        elif len(shape) == 1:
            return outputData
        else:
            return outputData[:, index]

    def getTargetValueByOutputFunc(self, currentData, strFunc):
        """
        根据函数求取最终目标值
        :param currentData: 当前选择的数据集
        :param strFunc: 目标函数
        :return: 目标值位置/None，目标值
        """
        if strFunc == OutputFunc.Max.value:
            index = np.argmax(currentData)
            return index, currentData[index]
        elif strFunc == OutputFunc.Min.value:
            index = np.argmin(currentData)
            return index, currentData[index]
        elif strFunc == OutputFunc.Mean.value:
            mean = currentData.mean()
            return None, mean
        elif strFunc == OutputFunc.Sum.value:
            sum = currentData.sum()
            return None, sum
        elif strFunc == OutputFunc.Last.value:
            lastValue = currentData[-1]
            index = len(currentData)
            return index-1, lastValue
        elif strFunc == OutputFunc.First.value:
            firstValue = currentData[0]
            return 0, firstValue
        else:
            return None
    # 计算位移MAG
    # 计算速度MAG
    # 计算加速度MAG
    # 2D xx yy zz xy yz zx stress vonMises (layer1-6)
    # 3D xx yy zz xy yz zx stress vonMises
    # 2D xx yy zz xy yz zx strain vonMises (LOWER, UPPER, MID)
    # 3D xx yy zz xy yz zx strain vonMises

    def getAllOutputType(self) -> dict:
        """
        获取文件中包含的所有结果类型
        :return:
        """
        outputTypeDict = {}
        if self.myD3plot.header.has_node_displacement:
            var = QVariant(ArrayType.node_displacement)
            outputTypeDict["Displacement"] = var
        if self.myD3plot.header.has_node_velocity:
            var = QVariant(ArrayType.node_velocity)
            outputTypeDict["Velocity"] = var
        if self.myD3plot.header.has_node_acceleration:
            var = QVariant(ArrayType.node_acceleration)
            outputTypeDict["Acceleration"] = var
        if self.myD3plot.header.has_shell_tshell_stress:
            var = QVariant(ArrayType.element_shell_stress)
            outputTypeDict["Stress(2D)"] = var
        if self.myD3plot.header.has_solid_stress:
            var = QVariant(ArrayType.element_solid_stress)
            outputTypeDict["Stress(3D)"] = var
        if self.myD3plot.header.has_shell_tshell_pstrain:
            var = QVariant(ArrayType.element_shell_strain)
            outputTypeDict["Strain(2D)"] = var
        if self.myD3plot.header.has_solid_pstrain:
            var = QVariant(ArrayType.element_solid_strain)
            outputTypeDict["Strain(3D)"] = var
        if self.myD3plot.arrays[ArrayType.element_shell_internal_energy].any():
            var = QVariant(ArrayType.element_shell_internal_energy)
            outputTypeDict["Element Internal energy(2D)"] = var
        if self.myD3plot.arrays[ArrayType.global_timesteps].any():
            var = QVariant(ArrayType.global_timesteps)
            outputTypeDict['TimeSteps'] = var
        if self.myD3plot.arrays[ArrayType.global_internal_energy].any():
            var = QVariant(ArrayType.global_internal_energy)
            outputTypeDict['Global Internal Energy'] = var
        if self.myD3plot.arrays[ArrayType.global_kinetic_energy].any():
            var = QVariant(ArrayType.global_kinetic_energy)
            outputTypeDict['Global Kinetic Energy'] = var
        if self.myD3plot.arrays[ArrayType.global_total_energy].any():
            var = QVariant(ArrayType.global_total_energy)
            outputTypeDict['Global Total Energy'] = var
        if self.myD3plot.arrays[ArrayType.part_internal_energy].any():
            var = QVariant(ArrayType.part_internal_energy)
            outputTypeDict['Part Internal Energy'] = var
        if self.myD3plot.arrays[ArrayType.part_kinetic_energy].any():
            var = QVariant(ArrayType.part_kinetic_energy)
            outputTypeDict['Part Kinetic Energy'] = var
        if self.myD3plot.arrays[ArrayType.part_mass].any():
            var = QVariant(ArrayType.part_mass)
            outputTypeDict['Part Mass'] = var
        return outputTypeDict

    def getAllPositionByOutputType(self, outputType) -> list:
        """
        获取当前输出类型的所有位置
        :param outputType: 输出类型
        :return:
        """
        if outputType == ArrayType.node_displacement or \
                outputType == ArrayType.node_velocity or \
                outputType == ArrayType.node_acceleration:
            return self.getAllNumberByFilter(FilterType.NODE)
        elif outputType == ArrayType.element_shell_strain or\
                outputType == ArrayType.element_shell_stress or\
                outputType == ArrayType.element_shell_internal_energy:
            return self.getAllNumberByFilter(FilterType.SHELL)
        elif outputType == ArrayType.element_solid_strain \
                or outputType == ArrayType.element_solid_stress:
            return self.getAllNumberByFilter(FilterType.SOLID)
        elif outputType == ArrayType.part_internal_energy \
                or outputType == ArrayType.part_kinetic_energy \
                or outputType == ArrayType.part_mass:
            return self.getAllNumberByFilter(FilterType.PART)
        elif outputType == ArrayType.global_kinetic_energy or\
                outputType == ArrayType.global_total_energy or \
                outputType == ArrayType.global_timesteps or \
                outputType == ArrayType.global_internal_energy:
            return None

    def getAllNumberByFilter(self, filter) -> list:
        """
        获取节点/单元编号
        :param filter: 节点/单元
        :return:
        """
        positionList = []
        if filter == FilterType.NODE:
            self.posList = self.getAllNodeNum()
            NodeNum = self.posList.shape[0]
            for index in range(NodeNum):
                positionList.append(f"N{self.posList[index]}")
        elif filter == FilterType.PART:
            self.posList = self.getAllPartTitles()
            if len(self.posList) >= 1:
                if isinstance(self.posList[0], np.bytes_):
                    positionList = np.array([s.decode('UTF-8') for s in self.posList]).tolist()
            if len(self.posList) >= 2:
                    positionList.append('Total')
        else:
            if filter == FilterType.SHELL:
                self.posList = self.getAllShellNum()
            elif filter == FilterType.SOLID:
                self.posList = self.getAllSolidNum()
            ShellNum = self.posList.shape[0]
            for index in range(ShellNum):
                positionList.append(f"E{self.posList[index]}")
        return positionList

    def getAllComponentByOutputType(self, outputType, layerNum = 0) -> list:
        """
        根据输出类型，获取所有的component
        :param outputType: 输出类型
        :param layerNum: 结果层数
        :return:
        """
        if outputType == ArrayType.node_displacement or \
                outputType == ArrayType.node_velocity or \
                outputType == ArrayType.node_acceleration:
            componentList = ["XX", "YY", "ZZ", "Mag"]
        elif outputType == ArrayType.element_shell_stress or \
                outputType == ArrayType.element_shell_strain or \
                outputType == ArrayType.element_solid_stress or \
                outputType == ArrayType.element_solid_strain:
            if layerNum == 1:
                componentList = ["XX", "YY", "ZZ", "XY", "YZ", "ZX", "vonMises"]
            else:
                componentList = []
                for index in range(1, layerNum + 1):
                    componentList.append(f"XX(layer{index})")
                    componentList.append(f"YY(layer{index})")
                    componentList.append(f"ZZ(layer{index})")
                    componentList.append(f"XY(layer{index})")
                    componentList.append(f"YZ(layer{index})")
                    componentList.append(f"ZX(layer{index})")
                    componentList.append(f"vonMises(layer{index})")
        elif outputType == ArrayType.element_shell_internal_energy or \
                outputType == ArrayType.global_timesteps or \
                outputType == ArrayType.global_total_energy or \
                outputType == ArrayType.global_internal_energy or \
                outputType == ArrayType.global_kinetic_energy or \
                outputType == ArrayType.part_mass or \
                outputType == ArrayType.part_kinetic_energy or \
                outputType == ArrayType.part_internal_energy:
            componentList = ["Value"]
        else:
            componentList = []
        return componentList

if __name__ == "__main__":
    lsDyna = ReadLsDynaResultsFile("C:/Users/84180/Desktop/hyperstudy_study/approaches/setup_1-def/run__00001/m_1/d3plot")