import numpy as np
import threading
import fortranformat as ff
from AnalyzeProcessTemplates.public import OutputFunc

class ReadRwforcFile(object):
    _instance = None
    _lock = threading.Lock()
    _initFlag = False
    currentFilePath = ''

    def __new__(cls, *args, **kw):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self, rwforc_pat='') -> None:
        with ReadRwforcFile._lock:
            if not ReadRwforcFile._initFlag:
                ReadRwforcFile._initFlag = True
                self.praserFile(rwforc_pat)

    def praserFile(self, rwforcPath):
        if rwforcPath:
            if self.currentFilePath == rwforcPath:
                if self.rwforc:
                    return True
                else:
                    return False
            else:
                self.rwforc = {}
                self.currentFilePath = rwforcPath
        rwforc_file = open(rwforcPath)
        rwforc_lines = rwforc_file.readlines()
        rwforc_file.close()
        for i, line in enumerate(rwforc_lines):
            line = line.strip()
            if line == "{BEGIN LEGEND}":
                rigid_num_beg = i
                continue
            elif line == "{END LEGEND}":
                rigid_num_end = i
                continue
            elif ff.FortranRecordReader('(A4, A12, A15, A11, A15, A15)').read(line)[0] == "time":
                time_step_beg = i
            else:
                time_step_end = i

        self.n_rigid_wall = rigid_num_end - rigid_num_beg - 2
        self.n_time_step = int((time_step_end - time_step_beg) / self.n_rigid_wall)

        self.rwforc["rigid_ids"] = []

        for i in range(self.n_rigid_wall):
            rigid_id = ff.FortranRecordReader('(A9)').read(rwforc_lines[rigid_num_beg + 2 + i])[0]
            rigid_id = rigid_id.strip()
            self.rwforc["rigid_ids"].append(rigid_id)
            self.rwforc[rigid_id] = []

        time_step_ = []
        for i, line in enumerate(rwforc_lines):
            if i <= time_step_beg:
                continue
            else:
                temp = []
                data_str = ff.FortranRecordReader('(A12, A8, 4A15)').read(line)
                time = float(data_str[0].strip())
                rigid_id = data_str[1].strip()
                norm_force = float(data_str[2].strip())
                x_force = float(data_str[3].strip())
                y_force = float(data_str[4].strip())
                z_force = float(data_str[5].strip())
                temp.append(norm_force)
                temp.append(x_force)
                temp.append(y_force)
                temp.append(z_force)
                self.rwforc[rigid_id].append(temp)

                if len(time_step_) == 0:
                    time_step_.append(time)
                else:
                    if time_step_[-1] != time:
                        time_step_.append(time)

        for i in range(self.n_rigid_wall):
            rigid_id = self.rwforc["rigid_ids"][i]
            self.rwforc[rigid_id] = np.array(self.rwforc[rigid_id])

        self.rwforc["time_step"] = np.array(time_step_)

        return True

    def get_rw_force(self, rigid_id_, direction_) -> np.array:
        if not self.rwforc:
            return None
        if direction_ == "norm":
            rw_forc_spec = self.rwforc[rigid_id_][:, 0]
        elif direction_ == "x":
            rw_forc_spec = self.rwforc[rigid_id_][:, 1]
        elif direction_ == "y":
            rw_forc_spec = self.rwforc[rigid_id_][:, 2]
        elif direction_ == "z":
            rw_forc_spec = self.rwforc[rigid_id_][:, 3]
        elif direction_ == "resultant":
            rw_forc_spec = np.sqrt(self.rwforc[rigid_id_][:, 1]**2 +
                                   self.rwforc[rigid_id_][:, 2]**2 +
                                   self.rwforc[rigid_id_][:, 3]**2)
        else:
            rw_forc_spec = self.rwforc[rigid_id_]

        return rw_forc_spec

    def get_rigid_ids(self):
        return self.rwforc["rigid_ids"]

    def get_directions(self):
        return ['norm', 'x', 'y', 'z', 'resultant']

    def get_time_step(self):
        return self.rwforc['time_step']

    def n_rigid_walls(self):
        return len(self.rwforc["rigid_ids"])

    def plot(self):
        pass

    def getTargetValueByOutputFunc(self, currentData, strFunc):
        """
        根据函数求取最终目标值
        :param currentData: 当前选择的数据集
        :param strFunc: 目标函数
        :return: 目标值位置/None，目标值
        """
        if strFunc == OutputFunc.Max.value:
            index = np.argmax(currentData)
            value = currentData[index]
            index = list(self.rwforc['time_step'])[index]
            return index, value
        elif strFunc == OutputFunc.Min.value:
            index = np.argmin(currentData)
            value = currentData[index]
            index = list(self.rwforc['time_step'])[index]
            return index, value
        elif strFunc == OutputFunc.Mean.value:
            mean = currentData.mean()
            return None, mean
        elif strFunc == OutputFunc.Sum.value:
            sum = currentData.sum()
            return None, sum
        elif strFunc == OutputFunc.Last.value:
            lastValue = currentData[-1]
            index = list(self.rwforc['time_step'])[-1]
            return index, lastValue
        elif strFunc == OutputFunc.First.value:
            firstValue = currentData[0]
            index = list(self.rwforc['time_step'])[0]
            return index, firstValue
        else:
            return None

    def getOutputValueByParameters(self, params:dict):
        func = params.get('outputFunc')
        direction = params.get('direction')
        rigidID = params.get('rigidID')
        currentData = self.get_rw_force(rigidID, direction)
        if func is not None:
            result = self.getTargetValueByOutputFunc(currentData, func)
            if len(result) > 1:
                return result[-1]
            return result[0]
        else:
            return currentData

    def getAllOutputType(self) -> dict:
        """
        获取所有输出类型
        :return:
        """
        outputTypeDict = {}
        outputTypeDict['force'] = 'rwforc_force'
        return outputTypeDict

    def getAllPositionByOutputType(self, outputType) -> list:
        """
        获取rigid部件
        :param outputType:
        :return:
        """
        if outputType == 'rwforc_force':
            return self.get_rigid_ids()

    def getAllComponentByOutputType(self, outputType, layerNum = 0) -> list:
        if outputType == 'rwforc_force':
            return self.get_directions()

    def getOutputDataByTypeandPosition(self, outputType, position):
        if outputType == 'rwforc_force':
            if not self.rwforc:
                return None
            curOutputData = self.rwforc[position]
            resultantData = np.sqrt(curOutputData[:, 1]**2 +
                                    curOutputData[:, 2]**2 +
                                    curOutputData[:, 3]**2)
            resultantData = resultantData[:, np.newaxis]
            finalData = np.concatenate((curOutputData, resultantData), axis=1)
            return finalData

    def getCurrentDataByOutputForm(self, outputData, index):
        if index < outputData.shape[1]:
            return outputData[:, index]
        else:
            return None



if __name__ == '__main__':
    rwforc_parser = ReadRwforcFile(
        rwforc_path=r"D:\BeiJingLiGongShenZhenQiCheYanJiuYuan\RMPOD\opt_platform\temp\fuhecailiao\7-5\rwforc")
    rwforc_x = rwforc_parser.get_rw_force('18', "z")
    time_step = rwforc_parser.get_time_step()
    n_rigid_walls = rwforc_parser.n_rigid_walls()
    print(time_step, n_rigid_walls)