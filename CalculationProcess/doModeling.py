from PyQt5.QtCore import QObject
from configFile.ReadTemplateConf import ReadandWriteTemplateConf
from lssvr import LSSVR
from sklearn import svm
from AnalyzeProcessTemplates.public import TemplateNameEnum
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from AnalyzeProcessTemplates.public import SurrogateModelParamSettingWayEnum, getTrainyData
from AnalyzeProcessTemplates.public import maskProgress
import numpy as np
from sklearn.datasets import load_iris
from joblib import parallel_backend, Parallel
import time

class DoModeling(QObject):
    def __init__(self):
        super(DoModeling, self).__init__()
        self.SurrogateModelData = ReadandWriteTemplateConf().data_SurrogateModel
        self.exeModeling()

    def exeModeling(self):
        ReadandWriteTemplateConf().ProgressBar_curCalculateStep = '构建代理模型中...'
        ReadandWriteTemplateConf().ProgressBar_isAuto = True
        ModelName = self.SurrogateModelData.SM_ModelName
        if self.SurrogateModelData.SM_ModelParamSettingWays == \
                SurrogateModelParamSettingWayEnum.GridSearch.value:
            trainyData = getTrainyData()
            self.SurrogateModelData.SM_TrainyData = trainyData
            trainy_x = trainyData[0]
            trainy_y = trainyData[1]
            variableNameList = trainyData[2]
            outputNameList = trainyData[3]
            yNum = trainy_y.shape[1]
            scoreList = np.zeros(yNum)
            # test_x = ReadandWriteTemplateConf().data_DataInput.DataFile_TestSet_x
            # test_y = ReadandWriteTemplateConf().data_DataInput.DataFile_TestSet_y
            for index in range(yNum):
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                y = trainy_y[:, index]
                if ModelName == 'Hybrid Model':
                    search_SVR = self.setGridSearchCV('SVR')
                    search_SVR.fit(trainy_x, y)
                    search = search_SVR
                    search_LSSVR = self.setGridSearchCV('LSSVR')
                    search_LSSVR.fit(trainy_x, y)
                    if search.best_score_ < search_LSSVR.best_score_:
                        search = search_LSSVR
                else:
                    search = self.setGridSearchCV(ModelName)
                    search.fit(trainy_x, y)
                scoreList[index] = search.best_score_
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                print(f"{outputNameList[index]}建模结果r2：{search.best_score_}")
                if search.best_score_ <= 0:
                    print('此模型精度过低，不适合用于后续优化')
                # ypre = search.predict([0.2,1.0,0.2,0.971199, 0.2,1.0,0.2,1.0,0.2,1.0])
                # print(ypre)
                self.SurrogateModelData.SM_Model[outputNameList[index]] = search
        elif self.SurrogateModelData.SM_ModelParamSettingWays == \
                SurrogateModelParamSettingWayEnum.Customization.value:
            self.doSVR()

    def doSVR(self):
        value_kernel = self.SurrogateModelData.SM_Params.get("核函数")
        value_dedgree = self.SurrogateModelData.SM_Params.get("多项式核函数次数")
        value_gamma = self.SurrogateModelData.SM_Params.get("核函数系数")
        value_coef0 = self.SurrogateModelData.SM_Params.get("核函数常数项")
        value_tol = self.SurrogateModelData.SM_Params.get("残差收敛条件")
        value_C = self.SurrogateModelData.SM_Params.get("正则化参数")
        value_epsilon = self.SurrogateModelData.SM_Params.get("epsilon")
        regr = svm.SVR(kernel=value_kernel,
                       degree=int(value_dedgree),
                       gamma=value_gamma,
                       coef0=float(value_coef0),
                       tol=float(value_tol),
                       C=float(value_C),
                       epsilon=float(value_epsilon))
        trainyData = self.getTrainyData()
        trainy_x = trainyData[0]
        trainy_y = trainyData[1]
        variableNameList = trainyData[2]
        outputNameList = trainyData[3]
        for index in range(trainy_y.shape[1]):
            # regr.fit(trainy_x, trainy_y[:, index].ravel())
            # test_x = ReadandWriteTemplateConf().data_DataInput.DataFile_TestSet_x
            # test_y = ReadandWriteTemplateConf().data_DataInput.DataFile_TestSet_y
            # coef = regr.score(test_x, test_y)
            # pred_y = regr.predict(test_x)
            # self.SurrogateModelData.SM_Model[index] = regr

            # 交叉验证
            score = cross_val_score(regr, trainy_x, trainy_y[:, index], cv=5, scoring="r2") #获取交叉验证的评价指标
            ypre = cross_val_predict(regr, trainy_x, trainy_y[:, index].ravel(), cv=5) #获取交叉验证的预测值
            r2 = r2_score(trainy_y[:, index], ypre, multioutput='variance_weighted')
            print("建模结果score", score)
            print("建模结果r2：", r2)
            self.SurrogateModelData.SM_Model[outputNameList[index]] = regr

    def setGridSearchCV(self, modelType):
        """
        网格搜索
        :param modelType: 代理模型类型
        :return: 估计器
        """
        kfold = self.SurrogateModelData.SM_ValidationParams.get('k-fold')
        # 回归指标
        myscoring = {'MAE': 'neg_mean_absolute_error',  # 平均绝对误差
                     'RMSE': 'neg_root_mean_squared_error',  # 均方误差
                     'R2': 'r2'}  # 可决系数
        if kfold is None:
            kfold = 10
        if modelType == 'SVR':
            pipe = Pipeline([('scaler', StandardScaler()), ('model',  svm.SVR())])
            paramGrid = self.getParamGrid(modelType)
            search = GridSearchCV(pipe, paramGrid, scoring=myscoring, refit='R2', cv=int(kfold), n_jobs=6)
            return search
        elif modelType == 'LSSVR':
            pipe = Pipeline([('scaler', StandardScaler()), ('model', LSSVR())])
            paramGrid = self.  getParamGrid(modelType)
            search = GridSearchCV(pipe, paramGrid, scoring=myscoring, refit='R2', cv=int(kfold), n_jobs=6)
            return search
        return None

    def getParamGrid(self, modelType):
        """SVR模型的网格参数"""
        if modelType == 'SVR':
            paramGrid = [{
                    'model__kernel': ['rbf'],
                    'model__tol':    [1e-5, 1e-4, 1e-3, 0.01, 0.1],
                    'model__gamma':  ['scale', 'auto', 0.001, 0.0001],
                    'model__C':      [1.0, 10.0, 1e+2, 1e+3, 1e+4, 1e+5, 1e+6]},
                # {
                #     'model__kernel': ['linear'],
                #     'model__tol':    [1e-5, 1e-4, 1e-3],
                #     'model__C':      [1.0, 10.0, 1e+2, 1e+3, 1e+4, 1e+5, 1e+6]},
                # {
                #     'model__kernel': ['poly'],
                #     'model__degree': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                #     'model__gamma':  ['scale', 'auto'],
                #     'model__tol':    [1e-5, 1e-4, 1e-3],
                #     'model__coef0':  [0, 1.0, 10.0, 1e+2, 1e+3, 1e+4, 1e+5, 1e+6],
                #     'model__C':      [1.0, 10.0, 1e+2, 1e+3, 1e+4, 1e+5, 1e+6]},
            ]

                #     'model__kernel': ['poly'],
                #     'model__degree': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                #     'model__gamma':  ['scale', 'auto'],
                #     'model__tol':    [1e-5, 1e-4, 1e-3],
                #     'model__coef0':  [0, 1.0, 10.0, 1e+2, 1e+3, 1e+4, 1e+5, 1e+6],
                #     'model__C':      [1.0, 10.0, 1e+2, 1e+3, 1e+4, 1e+5, 1e+6]},
                # {
                #     'model__kernel': ['sigmoid'],
                #     'model__gamma':  ['scale', 'auto'],
                #     'model__tol':    [1e-5, 1e-4, 1e-3],
                #     'model__coef0':  [0, 1.0, 10.0, 1e+2, 1e+3, 1e+4, 1e+5, 1e+6],
                #     'model__C':      [1.0, 10.0, 1e+2, 1e+3, 1e+4, 1e+5, 1e+6]},
            return paramGrid
        elif modelType == 'LSSVR':
            paramGrid = {
                'model__kernel': ['rbf', 'linear'],
                'model__gamma': [0.0001, 0.001, 0.01, 0.001, 0.0001, 0.00001, 0.000001],
                'model__C': [0.01, 0.1, 1, 2, 10, 100, 1000, 10000, 100000]}
            return paramGrid