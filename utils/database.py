# 考虑使用类来管理软件中的数据
import numpy as np



class Database(object):
    """所有数据的储藏

    Args:
        object (_type_): _description_
    """
    def __init__(self, file_path, mission, parent=None) -> None:
        """实例化一个数据库

        Args:
            parent ([type], optional): OptPlatform地址. Defaults to None.
        """
        super().__init__()
        self._OptPlatform = parent
        self.file_path = file_path
        self.mission_type = mission
        self.node_data = NodeDataBase()

    # def change_mission(self, mission):
    #     """改变任务类型
    #     #TODO 在某些情况下,中间的信息不必删除

    #     Args:
    #         mission (_type_): _description_
    #     """
    #     self.mission_type = mission
    #     self.nodes.clear_nodes()

class NodeDataBase(object):
    """节点存储数据库"""
    def __init__(self, parent=None) -> None:
        """实例化一个数据库

        Args:
            parent ([type], optional): OptPlatform地址. Defaults to None.
        """
        super().__init__()
        self._OptPlatform = parent
        self.nodes = []



    
# class MxCptDataBase(object):
#     def __init__(self, parent=None) -> None:
#         super().__init__()
#         self._MxDesign = parent
#         self.data = []

#     def append(self, module_database):
#         """添加一个模块的计算数据

#         Args:
#             module_database (class): 模块计算库类
#         """
#         self.data.append(module_database)

#     def remove(self, idx):
#         """删除一个模块的计算数据

#         Args:
#             idx (int): 删除模块的索引
#         """
#         del self.data[idx]

# class MxFitDataBase(object):
#     """拟合模块数据库"""
#     type = "fit"
#     def __init__(self, parent=None) -> None:
#         super().__init__()
#         self._MxDesign = parent
#         self.x_train = None  # 训练集x
#         self.x_test = None  # 测试集x
#         self.y_train = None
#         self.y_test = None  
#         self.y_pred = None  # 预测值y
#         self.model = None  # 模型

#     @property
#     def r2(self):
#         _r2 = r2_score(self.y_test, self.y_pred)
#         return _r2
    
#     @property
#     def mse(self):
#         _mse = mean_squared_error(self.y_test, self.y_pred)
#         return _mse


# class MxDoeDataBase(object):
#     """实验设计模块数据库"""
#     type = "doe"
#     def __init__(self, parent=None) -> None:
#         super().__init__()


# class MxSaDataBase(object):
#     """敏感性分析模块数据库"""
#     type = "sa"
#     def __init__(self, parent=None) -> None:
#         super().__init__()


# class MxOptDataBase(object):
#     """优化模块数据库"""
#     type = "opt"
#     def __init__(self, parent=None) -> None:
#         super().__init__()

# class MxStoDataBase(object):
#     """随机性分析模块数据库"""
#     type = "sto"
#     def __init__(self, parent=None) -> None:
#         super().__init__()