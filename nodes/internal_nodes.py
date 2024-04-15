from utils.graphics_view import GraphicItem

class NodeStart(GraphicItem):
    node_name = 'Start'
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pnodes = [] # name of previous nodes.
        self.avl_pnodes = [] # nodes that available to be pnodes.
        self.num_pnodes = 0 # maxixum pnodes, 0 means no pnode, 1 means 1 pnode, 2 means 1 pnode or more.
        
        # properties for current node
        self.function = '' # usage
        self.removable = False # if node can be removable
        # self.maxnum_node = int # maximun number of current node in a single project
        self.state = False # finished or not
        
        # properties for next nodes
        self.nnodes = [] # name of next nodes.
        self.avl_nnodes = ['SetPara'] # nodes that available to be nnodes.
        self.num_nnodes = 2 # maxixum nnodes, 0 means no nnode, 1 means 1 nnode, 2 means 1 nnode or more.
        self._correct_ui('icons\开始.png')

class NodeSetPara(GraphicItem):
    node_name = 'SetPara'
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pnodes = [] # name of previous nodes.
        self.avl_pnodes = ['Start'] # nodes that available to be pnodes.
        self.num_pnodes = 2 # maxixum pnodes, 0 means no pnode, 1 means 1 pnode, 2 means 1 pnode or more.
        
        # properties for current node
        self.function = 'settings' # usage
        self.removable = False # if node can be removable
        # self.maxnum_node = int # maximun number of current node in a single project
        self.state = False # finished or not
        
        # properties for next nodes
        self.nnodes = [] # name of next nodes.
        self.avl_nnodes = ['ExternalBox'] # nodes that available to be nnodes.
        self.num_nnodes = 1 # maxixum nnodes, 0 means no nnode, 1 means 1 nnode, 2 means 1 nnode or more.
        self._correct_ui('icons\变量.png')

# class NodeTest(GraphicItem):
#     node_name = 'Test'
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.pnodes = [] # name of previous nodes.
#         self.avl_pnodes = ['SetPara'] # nodes that available to be pnodes.
#         self.num_pnodes = 2 # maxixum pnodes, 0 means no pnode, 1 means 1 pnode, 2 means 1 pnode or more.
        
#         # properties for current node
#         self.function = 'settings' # usage
#         self.removable = False # if node can be removable
#         # self.maxnum_node = int # maximun number of current node in a single project
#         self.state = False # finished or not
        
#         # properties for next nodes
#         self.nnodes = [] # name of next nodes.
#         self.avl_nnodes = ['ExternalBox'] # nodes that available to be nnodes.
#         self.num_nnodes = 1 # maxixum nnodes, 0 means no nnode, 1 means 1 nnode, 2 means 1 nnode or more.
#         self._correct_ui('icons\最近访问.png')   
        
# class temp_node_2(GraphicItem):
#     def __init__(self, name=None, parent=None):
#         super().__init__(name, parent)
#         self.pnodes = [] # name of previous nodes.
#         self.avl_pnodes = ['start'] # nodes that available to be pnodes.
#         self.num_pnodes = 1 # maxixum pnodes, 0 means no pnode, 1 means 1 pnode, 2 means 1 pnode or more.
        
#         # properties for current node
#         self.node_name = 'doe' # node name
#         self.function = str # usage
#         self.removable = True # if node can be removable
#         # self.maxnum_node = int # maximun number of current node in a single project
#         self.state = bool # finished or not
        
#         # properties for next nodes
#         self.nnodes = [] # name of next nodes.
#         self.avl_nnodes = ['model'] # nodes that available to be nnodes.
#         self.num_nnodes = 2 # maxixum nnodes, 0 means no nnode, 1 means 1 nnode, 2 means 1 nnode or more.
#         self._correct_ui()

# class temp_node_3(GraphicItem):
#     def __init__(self, name=None, parent=None):
#         super().__init__(name, parent)
#         self.pnodes = [] # name of previous nodes.
#         self.avl_pnodes = ['doe'] # nodes that available to be pnodes.
#         self.num_pnodes = 10 # maxixum pnodes, 0 means no pnode, 1 means 1 pnode, 2 means 1 pnode or more.
        
#         # properties for current node
#         self.node_name = 'model' # node name
#         self.function = str # usage
#         self.removable = True # if node can be removable
#         # self.maxnum_node = int # maximun number of current node in a single project
#         self.state = bool # finished or not
        
#         # properties for next nodes
#         self.nnodes = [] # name of next nodes.
#         self.avl_nnodes = ['end'] # nodes that available to be nnodes.
#         self.num_nnodes = 1 # maxixum nnodes, 0 means no nnode, 1 means 1 nnode, 2 means 1 nnode or more.
#         self._correct_ui()

# class temp_node_4(GraphicItem):
#     def __init__(self, name=None, parent=None):
#         super().__init__(name, parent)
#         self.pnodes = [] # name of previous nodes.
#         self.avl_pnodes = ['model'] # nodes that available to be pnodes.
#         self.num_pnodes = 1 # maxixum pnodes, 0 means no pnode, 1 means 1 pnode, 2 means 1 pnode or more.
        
#         # properties for current node
#         self.node_name = 'end' # node name
#         self.function = str # usage
#         self.removable = False # if node can be removable
#         # self.maxnum_node = int # maximun number of current node in a single project
#         self.state = bool # finished or not
        
#         # properties for next nodes
#         self.nnodes = [] # name of next nodes.
#         self.avl_nnodes = [] # nodes that available to be nnodes.
#         self.num_nnodes = 0 # maxixum nnodes, 0 means no nnode, 1 means 1 nnode, 2 means 1 nnode or more.
#         self._correct_ui()

