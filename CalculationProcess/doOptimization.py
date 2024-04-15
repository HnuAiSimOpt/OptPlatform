from PyQt5.QtCore import QObject
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from pymoo.operators.sampling.lhs import LHS
from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.optimize import minimize
import ast
import numpy as np
from AnalyzeProcessTemplates.public import TemplateNameEnum, maskProgress
# from pymoo.factory import get_sampling, get_crossover, get_mutation, get_termination
from pymoo.algorithms.moo.nsga2 import NSGA2
from AnalyzeProcessTemplates.public import translateStringToFloat, isDebug
import logging

class DoOptimization(QObject):
    def __init__(self):
        super(DoOptimization, self).__init__()

    def do(self):
        ReadandWriteTemplateConf().ProgressBar_curCalculateStep = '优化求解中...'
        ReadandWriteTemplateConf().ProgressBar_isAuto = True
        OptimizationAlgorithmData = ReadandWriteTemplateConf().data_OptimizationAlgorithm
        OptAlgorithmName = OptimizationAlgorithmData.Opt_AlgorithmName
        if OptAlgorithmName == "PSO":
            value_popSize = OptimizationAlgorithmData.Opt_AlgorithmParams.get("种群数量")
            if OptimizationAlgorithmData.Opt_AlgorithmParams.get("采样过程") == "LHS":
                value_sampling = LHS()
            value_adaptive = OptimizationAlgorithmData.Opt_AlgorithmParams.get("自适应")
            value_w = OptimizationAlgorithmData.Opt_AlgorithmParams.get("惯性权重")
            value_c1 = OptimizationAlgorithmData.Opt_AlgorithmParams.get("学习因子-1")
            value_c2 = OptimizationAlgorithmData.Opt_AlgorithmParams.get("学习因子-2")
            value_initVec = OptimizationAlgorithmData.Opt_AlgorithmParams.get("初始速度")
            value_maxVec = OptimizationAlgorithmData.Opt_AlgorithmParams.get("最大速率")
            value_pertubeBest = OptimizationAlgorithmData.Opt_AlgorithmParams.get("pertube_best")
            myAlgorithm = PSO(pop_size=int(value_popSize),
                            sampling=value_sampling,
                            w=float(value_w),
                            c1=float(value_c1),
                            c2=float(value_c2),
                            adaptive=ast.literal_eval(value_adaptive),
                            initial_velocity=value_initVec,
                            max_velocity_rate=float(value_maxVec),
                            pertube_best=ast.literal_eval(value_pertubeBest))
            myProblem = Problem_SurrogateModel()
            res = minimize(myProblem, myAlgorithm, seed=1, verbose=False)
            OptimizationAlgorithmData.Opt_AlgorithmResult = res
            print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
        elif OptAlgorithmName == 'NSGA2':
            try:
                myAlgorithm = NSGA2(pop_size=40)
                myProblem = Problem_SurrogateModel()
                OptimizationAlgorithmData.Opt_AlgorithmProblem = myProblem
                res = minimize(myProblem, myAlgorithm, ('n_gen', 200), seed=1, verbose=True)
                OptimizationAlgorithmData.Opt_AlgorithmResult = res
                if isDebug:
                    print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
            except:
                OptimizationAlgorithmData.Opt_AlgorithmResult = None
                logging.getLogger().error('优化算法求解失败！')

class Problem_SurrogateModel(Problem):
    def __init__(self):
        confFile = ReadandWriteTemplateConf()
        self.decimalList = confFile.data_FECalcuFile.getVariableDecimal()
        self.isSciNotation = confFile.data_FECalcuFile.getIsScientificNotation()
        data = confFile.data_OptimizationAlgorithm
        self.targetData = data.Opt_AlgorithmProblem_target
        self.constrData = data.Opt_AlgorithmProblem_constrains
        xUp = data.Opt_AlgorithmProblem_variUpLow.get('up')
        xLow = data.Opt_AlgorithmProblem_variUpLow.get('low')
        varNum = len(xUp)
        objNum = len(self.targetData)
        constrNum = len(self.constrData)
        super().__init__(n_var=varNum, n_obj=objNum, n_constr=constrNum,
                         xl=np.array(xLow), xu=np.array(xUp))

    def _evaluate(self, x, out, *args, **kwargs):
        # 将x中的数据格式化
        # if ReadandWriteTemplateConf().usrChoosnTemplate == TemplateNameEnum.Template_opt_FE:
        #     if len(x.shape) == 2:
        #         for index_i in range(x.shape[0]):
        #             for index_j in range(x.shape[1]):
        #                 tmpValue = translateStringToFloat(strValue=str(x[index_i][index_j]),
        #                                                decimal=self.decimalList[index_j],
        #                                                isSciNotation=self.isSciNotation[index_j])
        #                 x[index_i][index_j] = tmpValue
        #     elif len(x.shape) == 1:
        #         for index_j in range(x.shape[1]):
        #             tmpValue = translateStringToFloat(strValue=str(x[index_j]),
        #                                               decimal=self.decimalList[index_j],
        #                                               isSciNotation=self.isSciNotation[index_j])
        #             x[index_j] = tmpValue

        modelData = ReadandWriteTemplateConf().data_SurrogateModel.SM_Model
        # 响应名称 代理模型
        # for key, value in modelData.items():
        #     exec('{}={}'.format(key, value))
        # 变量名 index
        if ReadandWriteTemplateConf().usrChoosnTemplate == TemplateNameEnum.Template_opt_FE.value:
            varList = ReadandWriteTemplateConf().data_DOE.doe_VariablesValueRange.keys()
        elif ReadandWriteTemplateConf().usrChoosnTemplate == TemplateNameEnum.Template_opt.value:
            varList = ReadandWriteTemplateConf().data_DataInput.DataFile_VariableNameList
        index = 0
        for key in varList:
            exec('{}={}'.format(key, index))
            index += 1
        #定义目标函数
        targetList = []
        for key, value in self.targetData.items():
            expression = self.replaceResponseNameToPredictFunc(modelData, value[0])
            expression = self.replaceVariableNameToVarValue(varList, expression)
            func = value[1]
            if func == 'MAX':
                expression = '-(' + expression + ')'
            F = eval(expression)
            print(f'F: {F}')
            targetList.append(F)
        #定义约束条件
        constrList = []
        if self.constrData:
            for key, value in self.constrData.items():
                expression = self.replaceResponseNameToPredictFunc(modelData, value)
                expression = self.replaceVariableNameToVarValue(varList, expression)
                G = eval(expression)
                print(f'G: {G}')
                constrList.append(G)

        out["F"] = np.column_stack(targetList)
        if constrList:
            out["G"] = np.column_stack(constrList)

    def replaceResponseNameToPredictFunc(self, modelData, expression: str):
        """将响应值名称替换成预测函数"""
        newExpression = expression
        for key in modelData.keys():
            newExpression = newExpression.replace(key, f'modelData["{key}"].predict(x)')
        return newExpression

    def replaceVariableNameToVarValue(self, varlist, expression: str):
        """将变量名替换成对应的值"""
        newExpression = expression
        for key in varlist:
            newExpression = newExpression.replace(key, f'x[:,{key}]')
        return newExpression