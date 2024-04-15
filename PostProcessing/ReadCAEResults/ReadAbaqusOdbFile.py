# encoding: utf-8
from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import sys
import json
import numpy as np

class abaqusODBProcess(object):
    def __init__(self,odbPath):
        self._odb = openOdb(path=odbPath)

    # 读取step_list
    @property
    def step_list(self):
        step_list=self._odb.steps.keys()
        return step_list

    # 读取instance_list
    @property
    def instance_list(self):
        instance_list = self._odb.rootAssembly.instances.keys()
        return instance_list
    
    # 读取node_sets_list
    @property
    def nodeSets_list(self):
        nodeSets_list = self._odb.rootAssembly.nodeSets.keys()
        return nodeSets_list

    # 读取element_sets_list
    @property
    def elementSets_list(self):
        elementSet_list = self._odb.rootAssembly.elementSets.keys()
        return elementSet_list

    # 读取某个step的frame_list
    def get_frame_list(self, step):
        frame_num = len(self._odb.steps[step].frames)
        frame_list = list(range(frame_num))
        return frame_list

    # 读某frame的components_list
    def get_components_list(self, step, frame):
        components_list = self._odb.steps[step].frames[frame].fieldOutputs.keys()
        return components_list

    # 通过instance的名称获取node_list
    def get_node_list(self, instance):
        nodes = self._odb.rootAssembly.instances[instance].nodes
        nodeList=[[each.label]+list(each.coordinates) for each in nodes]
        return nodeList
    
    # 读取某个step的historyregion
    def get_historyregion_list(self, step):
        historyregion_list = self._odb.steps[step].historyRegions.keys()
        return historyregion_list
    
    # 读取historyoutputs中的响应类型histype
    def get_histype_list(self, step, region):
        historyregion_list = self._odb.steps[step].historyRegions[region].historyOutputs.keys()
        return historyregion_list

    # step-instance-nodelist-components-field outputs
    def read_response_from_nodelist(self, step=str, frame=int, instance=str, component=str):
        frame = self._odb.steps[step].frames[frame]
        response = frame.fieldOutputs[component]
        instance = self._odb.rootAssembly.instances[instance]
        response_instance = response.getSubset(region=instance)
        returnDict = {}

        for each in response_instance.values:
            if each.nodeLabel:
                returnDict[each.nodeLabel] = each.data
            else:
                returnDict[each.elementLabel] = each.data
        return returnDict

    # step-instance-elementlist-components-field outputs
    def read_response_from_elementlist(self, step=str, frame=int, element=str, component=str):
        curframe = self._odb.steps[step].frames[frame]
        response = curframe.fieldOutputs[component]
        instance = self._odb.rootAssembly.elementSets[element]
        response_instance = response.getSubset(region=instance)
        returnDict = {}

        for each in response_instance.values:
            returnDict[each.elementLabel] = each.data
            print(each.elementLabel)
        return returnDict

    # step-instance-nodelist-components-field outputs
    def read_response_from_nodeset(self, step=str, frame=int, nodeSet=str, component=str):
        frame = self._odb.steps[step].frames[frame]
        response = frame.fieldOutputs[component]
        nodeSet = self._odb.rootAssembly.nodeSets[nodeSet]
        response_instance = response.getSubset(region=nodeSet)
        returnDict = {}

        for each in response_instance.values:
            returnDict[each.nodeLabel] = each.data
        return returnDict  
    
    def read_responese_from_history(self, step=str, region=str, histype=str):
        return self._odb.steps[step].historyRegions[region].historyOutputs[histype].data

"""
使用:
1. 用户选择odb文件
2. 读取odb完毕后, 读取odb文件中step的列表, 供用户选择
##### A 读取场输出#####
A3. 选择step完毕后, 读取step中的frame数目, 供用户选择
A4. 选择frame完毕后, 读取frame中响应的类型(component), 供用户选择
A5. 读取instance_list/nodeSet, 供用户选择
A6. 根据step, frame, component, instance/nodeset, 输出响应值
A7. 记录该索引(step, frame, component, instance/nodeset),用于后续优化
##### B 读取历程输出#####
B3. 选择step完毕后, 读取step中历程输出historyRegion, 供用户选择
B4. 选择historyRegion完毕后, 读取historyOutputs的类型histype, 供用户选择
B6. 根据step, historyRegion, histype, 输出响应值
B7. 记录该索引(step, historyRegion, histype),用于后续优化
"""
def case1():
    # CASE_1 
    # 1 读取某个部件的位移场输出
    filepath = r"D:\project_optPlatform\opt_platform\temp\V3_modified.odb"
    CASE1 = abaqusODBProcess(filepath)
    # 2 
    step_list = CASE1.step_list
    print(step_list)
    mystep = step_list[-1]
    # 3
    frame_list = CASE1.get_frame_list(mystep)
    print(frame_list)
    myframe = frame_list[-1]
    # 4
    components_list = CASE1.get_components_list(mystep, myframe)
    print(components_list)
    mycomponent = 'U' # U是components_list中的一个component
    # 5
    instance_list = CASE1.instance_list
    my_instance = instance_list[-1]
    # 6
    returnDict = CASE1.read_response_from_nodelist(mystep, myframe, my_instance, mycomponent)
    newfilepath = filepath[0: filepath.rfind('\\') + 1] + 'curResults_.npy'
    # with open(newfilepath, 'w') as f:
    #     f.write(json.dumps(returnDict, ensure_ascii=False))
    #     f.close()

    # with open(newfilepath, 'w') as f_obj:  # 打开模式为可写
    #     json.dump(returnDict, f_obj)  # 存储文件

    np.save(newfilepath, returnDict)  # 注意带上后缀名

def case2():
    # CASE_2
    # 1 读取某个nodeset的位移场输出
    CASE1 = abaqusODBProcess(r"D:\project_optPlatform\opt_platform\temp\V3_modified.odb")
    # 2 
    step_list = CASE1.step_list
    print(step_list)
    mystep = step_list[-1]
    # 3
    frame_list = CASE1.get_frame_list(mystep)
    print(frame_list)
    myframe = frame_list[-1]
    # 4
    components_list = CASE1.get_components_list(mystep, myframe)
    print(components_list)
    mycomponent = 'U' # U是components_list中的一个component
    # 5
    nodeset_list = CASE1.nodeSets_list
    my_nodeset = nodeset_list[-1]
    # 6
    returnDict = CASE1.read_response_from_nodeset(mystep, myframe, my_nodeset, mycomponent)
    for item in returnDict:
        print(returnDict[item])

def case3():
    # CASE_2
    # 1 读取某个部件的位移场输出
    CASE1 = abaqusODBProcess(r"D:\project_optPlatform\opt_platform\temp\V3_modified.odb")
    # 2 
    step_list = CASE1.step_list
    print(step_list)
    mystep = step_list[-1]
    # 3
    historyregion_list = CASE1.get_historyregion_list(mystep) 
    print(historyregion_list)
    myregion = historyregion_list[-1]
    # 4 
    histype_list = CASE1.get_histype_list(mystep, myregion)
    print(histype_list)
    myhistype = histype_list[-1]
    # 5
    returnList = CASE1.read_responese_from_history(mystep, myregion, myhistype)
    print(returnList)

def case4():
    # CASE_4
    # 1 读取某个部件的位移场输出
    filepath = r"D:\project_optPlatform\opt_platform\temp\V3_modified.odb"
    CASE1 = abaqusODBProcess(filepath)
    # 2
    step_list = CASE1.step_list
    print(step_list)
    mystep = step_list[-1]
    # 3
    frame_list = CASE1.get_frame_list(mystep)
    print(frame_list)
    myframe = frame_list[-1]
    # 4
    components_list = CASE1.get_components_list(mystep, myframe)
    print(components_list)
    mycomponent = 'S' # U是components_list中的一个component
    # 5
    elementsSet_list = CASE1.elementSets_list
    my_instance = elementsSet_list[-1]
    # 6
    returnDict = CASE1.read_response_from_elementlist(mystep, myframe, my_instance, mycomponent)
    newfilepath = filepath[0: filepath.rfind('\\') + 1] + 'curResults_.npy'
    # with open(newfilepath, 'w') as f:
    #     f.write(json.dumps(returnDict, ensure_ascii=False))
    #     f.close()

    # with open(newfilepath, 'w') as f_obj:  # 打开模式为可写
    #     json.dump(returnDict, f_obj)  # 存储文件

    np.save(newfilepath, returnDict)  # 注意带上后缀名

def get_List_Value(filepath):
    structDict = {}
    odbProcess = abaqusODBProcess(filepath)
    step_list = odbProcess.step_list
    structDict['_step_list'] = step_list
    # outStr = '__STEP__:' + ','.join(step_list) + '\n'
    for step in step_list:
        frame_list = odbProcess.get_frame_list(step)
        strName = '_frame_' + str(step)
        structDict[strName] = frame_list
        # tmpStr = '__FRAME_' + str(step) + '__:' + ','.join(frame_list) + '\n'
        # outStr = ''.join([outStr, tmpStr])
        for frame in frame_list:
            components_list = odbProcess.get_components_list(step, frame)
            strName = '_component_' + str(step) + '_' + str(frame)
            structDict[strName] = components_list
            # tmpStr = '__COMPONENTS_' + str(step) + '_' + str(frame) + '__:' + ','.join(components_list) + '\n'
            # outStr = ''.join([outStr, tmpStr])
        historyregion_list = odbProcess.get_historyregion_list(step)
        strName = '_historyregion_' + str(step)
        structDict[strName] = historyregion_list
        # tmpStr = '__HISTORYOUTPUT_' + str(step) + '__:' + ','.join(historyregion_list) + '\n'
        # outStr = ''.join([outStr, tmpStr])
        for region in historyregion_list:
            histype_list = odbProcess.get_histype_list(step, region)
            strName = '_histype_' + str(step) + '_' + str(region)
            structDict[strName] = histype_list
            # tmpStr = '__HISTYPE_' + str(step) + '_' + str(region) + '__:' + ','.join(histype_list) + '\n'
            # outStr = ''.join([outStr, tmpStr])
    nodeset_list = odbProcess.nodeSets_list
    if nodeset_list:
        structDict['_nodeset_list'] = nodeset_list
    # tmpStr = '__NODESET__:' + ','.join(nodeset_list) + '\n'
    # outStr = ''.join([outStr, tmpStr])
    instance_list = odbProcess.instance_list
    if instance_list:
        structDict['_instance_list'] = instance_list
    # tmpStr = '__INSTANCE__:' + ','.join(instance_list) + '\n'
    # outStr = ''.join([outStr, tmpStr])
    element_list = odbProcess.elementSets_list
    if element_list:
        structDict['_elementset_list'] = element_list
        print('_elementset_list' + str(len(element_list)))

    newfilepath = filepath[0: filepath.rfind('\\') + 1] + 'curStruct.npy'
    np.save(newfilepath, structDict)

    # sys.stdout.write(outStr)
    # sys.stdout.flush()

# case1()

# get_List_Value(r"D:\project_optPlatform\opt_platform\temp\V3_modified.odb")

if __name__ == "__main__":
    try:
        strFilePath = str(sys.argv[1])
        strParams = str(sys.argv[2])
        setType = int(sys.argv[3])
        sys.stdout.write("数据传入成功\n")
        sys.stdout.flush()
    except ValueError:
        sys.stdout.write('there is no input!\n')
        sys.stdout.flush()
        exit(1)
    else:
        if strFilePath and strParams == 'None':
            sys.stdout.write("正在解析odb文件: " + strFilePath)
            sys.stdout.flush()
            get_List_Value(strFilePath)
        elif strFilePath and strParams != 'None':
            params_list = strParams.split(',')
            if len(params_list) == 3:
                odbProcess = abaqusODBProcess(strFilePath)
                returnList = odbProcess.read_responese_from_history(
                    params_list[0], params_list[1], params_list[2])
                newfilepath = strFilePath[0: strFilePath.rfind('\\') + 1] +\
                              'curResults_' + '_'.join(params_list) + '.npy'
                np.save(newfilepath, returnList)
                sys.stdout.flush()
            elif len(params_list) == 4:
                odbProcess = abaqusODBProcess(strFilePath)
                if (setType & 1):
                    returnDict = odbProcess.read_response_from_nodelist(
                        params_list[0], int(params_list[1]), params_list[2], params_list[3])
                elif (setType & 2):
                    returnDict = odbProcess.read_response_from_nodeset(
                        params_list[0], int(params_list[1]), params_list[2], params_list[3])
                elif (setType & 4):
                    returnDict = odbProcess.read_response_from_elementlist(
                        params_list[0], int(params_list[1]), params_list[2], params_list[3])
                newfilepath = strFilePath[0: strFilePath.rfind('\\') + 1] + \
                              'curResults_' + '_'.join(params_list) + '.npy'
                np.save(newfilepath, returnDict)
            sys.stdout.write('_'.join(params_list) + "\n")
            exit(0)