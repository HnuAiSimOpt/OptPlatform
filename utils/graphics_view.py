import math
from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem, QGraphicsScene, QGraphicsView,QGraphicsPixmapItem, QGraphicsEllipseItem
from PyQt5.QtGui import QColor, QPen, QBrush, QPainterPath, QColor, QPen, QPainter, QPixmap
from PyQt5.QtCore import Qt, QPointF, QLine


from PyQt5 import QtGui, QtCore


class MyGraphicView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._canvas = parent
        self.gr_scene = MyGraphicScene
        self.drag_edge = None
        self._correct_ui()

    def _correct_ui(self):
        self.gr_scene = MyGraphicScene()
        self.setScene(self.gr_scene)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform |
                            QPainter.LosslessImageRendering)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setDragMode(self.RubberBandDrag)

    # # # events
    # def keyPressEvent(self, event):
    #     print(1111)
    #     if event.key() == Qt.Key_Q:
    #         item = NodeStart()
    #         item.setPos(0, 0)
    #         self.gr_scene.add_node(item)
    #         print(111)

                
    def mousePressEvent(self, event):
        # print(event.pos(),111)
        # print(self.mapToScene(event.pos()),333)
        item = self.get_item_at_click(event)
        if event.button() == Qt.LeftButton:
            if isinstance(item, ControlPoint):
                self.edge_drag_start(item)
            else:
                pos = self.mapToScene(event.pos())
                # print('1',pos.x(),pos.y())
                super().mousePressEvent(event)     
        elif event.button() == Qt.RightButton:
            if isinstance(item, GraphicItem):
                if item.removable:
                    self.gr_scene.remove_node(item)
                    self.update()
                else:
                    pass
            elif isinstance(item, GraphicEdge):
                if item.removable:
                    self.gr_scene.remove_edge(item)
                    self.gr_scene.update_nodes_info()
                    self.update()
                else:
                    pass
        else:
            pass
    
    def get_item_at_click(self, event):
        """ 
        Return the object that clicked on. 
        """
        pos = event.pos()
        item = self.itemAt(pos)
        return item

    def get_items_at_rubber(self):
        """ 
        Get group select items. 
        """
        area = self.rubberBandRect()
        return self.items(area)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if self.drag_edge is not None:
            sc_pos = self.mapToScene(pos)
            self.drag_edge.gr_edge.set_dst(sc_pos.x(), sc_pos.y())
            self.drag_edge.gr_edge.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.drag_edge:
            item = self.get_item_at_click(event)
            # check the end_node can be connected
            if isinstance(item, ControlPoint):
                if item.check_connection(self.drag_start_item):
                    seq = item.check_connection(self.drag_start_item)
                    self.edge_drag_end(item, seq)
                else:
                    self.drag_edge.remove()
                    self.drag_edge = None
            else:
                self.drag_edge.remove()
                self.drag_edge = None
        else:
            super().mouseReleaseEvent(event)

    def edge_drag_start(self, item):
        """
        drag start

        Args:
            item (_type_): _description_
        """
        self.drag_start_item = item
        self.drag_edge = Edge(self.gr_scene, self.drag_start_item, None)

    def edge_drag_end(self, item, seq):
        """
        drag end

        Args:
            item (_type_): _description_
        """
        name = len(self.gr_scene.edges)
        if seq==1:
            new_edge = Edge(self.gr_scene, self.drag_start_item, item, name=name)
        else:
            new_edge = Edge(self.gr_scene, item, self.drag_start_item, name=name)
        self.drag_edge.remove()
        self.drag_edge = None
        self.gr_scene.edges.pop()
        new_edge.store()
        self.gr_scene.update_nodes_info()

    def connect(self, start, end):
        name = len(self.gr_scene.edges)
        new_edge = Edge(self.gr_scene, start, end, name=name)
        self.gr_scene.edges.pop()
        new_edge.store()
        # self.gr_scene.update_nodes_info()

class MyGraphicScene(QGraphicsScene):
    """
    QGraphicsScene, similar to model.

    Args:
        QGraphicsScene (_type_): _description_
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.nodes = []
        self.edges = []
        self._correct_ui()

    def _correct_ui(self):
        self.grid_size = 20
        self.grid_squares = 5

        self._color_background = QColor('#393939')
        self._color_light = QColor('#2f2f2f')
        self._color_dark = QColor('#292929')

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)
        self.setSceneRect(0, 0, 100, 100)
        
    def add_node(self, node):
        self.nodes.append(node)
        self.addItem(node)
        # self.update_nodes_info()

    def remove_node(self, node):
        # remove edges
        remove_list = []
        for edge in self.edges:
            if edge.edge_wrap.start_item.gr_item is node or edge.edge_wrap.end_item.gr_item is node:
                remove_list.append(edge)
        self.remove_edge(remove_list)
        # remove node
        node.setVisible(False)
        self.nodes.remove(node)
        self.removeItem(node)
        self.update_nodes_info()

    def add_edge(self, edge):
        self.edges.append(edge)
        self.addItem(edge)

    def remove_edge(self, edges):
        if isinstance(edges, list):
            for edge in edges:
                self.edges.remove(edge)
                edge.setVisible(False)
                self.removeItem(edge)
        else:
            self.edges.remove(edges)
            self.removeItem(edges)
        
    def update_nodes_info(self, debug=True):
        """
        update when connection changed(add connections, remove connections, remove nodes)
        """

        for node in self.nodes:
            node.pnodes.clear()
            node.nnodes.clear()
        
        for edge in self.edges:
            start = edge.edge_wrap.start_item.gr_item
            end = edge.edge_wrap.end_item.gr_item
            start.nnodes.append(end)
            end.pnodes.append(start)

        # debug
        if debug:
            for idx, node in enumerate(self.nodes):     
                print(node.node_name, node.pnodes, node.nnodes) 

    def drawBackground(self, painter, rect):
        """draw the background

        Args:
            painter (_type_): _description_
            rect (_type_): _description_
        """
        super().drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # draw the lines
        painter.setPen(self._pen_light)
        if lines_light:
            painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        if lines_dark:
            painter.drawLines(*lines_dark)

class Edge(object):
    def __init__(self, scene, start_item, end_item, name=None):
        super().__init__()
        self.name = name
        self.scene = scene
        self.start_item = start_item
        self.end_item = end_item

        self.gr_edge = GraphicEdge(self)
        self.scene.add_edge(self.gr_edge)
        if self.start_item is not None:
            self.update_positions()

    def store(self):
        self.scene.add_edge(self.gr_edge)

    def update_positions(self):
        src_pos = self.start_item.get_pos()
        self.gr_edge.set_src(src_pos.x(), src_pos.y())
        if self.end_item is not None:
            end_pos = self.end_item.get_pos()
            self.gr_edge.set_dst(end_pos.x(), end_pos.y())
        else:
            self.gr_edge.set_dst(src_pos.x(), src_pos.y())
        self.gr_edge.update()

    def remove_from_current_items(self):
        self.end_item = None
        self.start_item = None

    def remove(self):
        self.remove_from_current_items()
        self.scene.remove_edge(self.gr_edge)
        self.gr_edge = None

class GraphicEdge(QGraphicsPathItem):

    def __init__(self, edge_wrap, parent=None):
        super().__init__(parent)
        self.edge_wrap = edge_wrap
        self.width = 3.0
        self.pos_src = [0, 0]
        self.pos_dst = [0, 0]
        self.removable = True

        self._pen = QPen(QColor("#000"))
        self._pen.setWidthF(self.width)

        self._pen_dragging = QPen(QColor("#000"))
        self._pen_dragging.setStyle(Qt.DashDotLine)
        self._pen_dragging.setWidthF(self.width)

        self._mark_pen = QPen(Qt.green)
        self._mark_pen.setWidthF(self.width)
        self._mark_brush = QBrush()
        self._mark_brush.setColor(Qt.green)
        self._mark_brush.setStyle(Qt.SolidPattern)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

    def set_src(self, x, y):
        self.pos_src = [x, y]

    def set_dst(self, x, y):
        self.pos_dst = [x, y]

    def calc_path(self):
        path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))
        path.lineTo(self.pos_dst[0], self.pos_dst[1])
        return path

    def boundingRect(self):
        return self.shape().boundingRect()

    def shape(self):
        return self.calc_path()

    def arrowCalc(self, x1, y1, x2, y2):
        dx, dy = x1-x2, y1-y2

        leng = math.sqrt(dx ** 2 + dy ** 2)
        normX, normY = dx / leng, dy / leng  # normalize

        # perpendicular vector
        perpX = -normY
        perpY = normX

        leftX = x2 + 10 * normX + 4 * perpX
        leftY = y2 + 10 * normY + 4 * perpY

        rightX = x2 + 10 * normX - 4 * perpX
        rightY = y2 + 10 * normY - 4 * perpY

        point2 = QtCore.QPointF(leftX, leftY)
        point3 = QtCore.QPointF(rightX, rightY)
        endPoint = QtCore.QPointF(x2, y2)

        return QtGui.QPolygonF([point2, endPoint, point3])

    def paint(self, painter, graphics_item, widget=None):
        # update the path 
        self.setPath(self.calc_path())
        path = self.path()
        if self.edge_wrap.end_item is None:
            painter.setPen(self._pen_dragging)
            painter.drawPath(path)
        else:
            x1, y1 = self.pos_src
            x2, y2 = self.pos_dst
            # radius = 5    # marker radius
            # length = 70   # marker length
            # k = math.atan2(y2 - y1, x2 - x1)
            # new_x = x2 - length * math.cos(k) - self.width
            # new_y = y2 - length * math.sin(k) - self.width
            # pp = self.arrowCalc(x1, y1, x2, y2)
            painter.setPen(self._pen)
            painter.drawPath(path)
            # painter.drawPolyline(pp)
            # painter.setPen(self._mark_pen)
            # painter.setBrush(self._mark_brush)
            
class GraphicItem(QGraphicsPixmapItem):
    node_name = None
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pnodes = [] # name of previous nodes.
        self.avl_pnodes = [] # nodes that available to be pnodes.
        self.num_pnodes = int # maxixum pnodes, 0 means no pnode, 1 means 1 pnode, 2 means 1 pnode or more.
        
        # properties for current node
        self.function = str # usage
        self.removable = bool # if node can be removable
        self.maxnum_node = int # maximun number of current node in a single project
        
        # properties for next nodes
        self.nnodes = [] # name of next nodes.
        self.avl_nnodes = [] # nodes that available to be nnodes.
        self.num_nnodes = int # maxixum nnodes, 0 means no nnode, 1 means 1 nnode, 2 means 1 nnode or more.

        self.input_point = None
        self.output_point = None

        self.input_data = None
        self.finished_state = False 
        self.output_data = None
        
    def _correct_ui(self, icon):
        self.pix = QPixmap(icon)
        self.width = 85
        self.height = 85
        # set the node item
        self.setPixmap(self.pix.scaled(self.width, self.height))
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)

        if self.avl_pnodes:
            self.input_point = ControlPoint('input', self, 'horizontal')
        if self.avl_nnodes:
            self.output_point = ControlPoint('output', self, 'horizontal')
        
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # update selected node and its edge
        if self.isSelected():
            for gr_edge in self.scene().edges:
                gr_edge.edge_wrap.update_positions()
    
    def add_pnode(self, node):
        self.pnodes.append(node)
    
    def add_nnode(self, node):
        self.nnodes.append(node)

class ControlPoint(QGraphicsEllipseItem):
    def __init__(self, point_type, parent, point_pos):
        super().__init__(-5, -5, 10, 10, parent)
        self.gr_item = parent
        self.point_type = point_type
        self.point_pos = point_pos        
        self._correct_ui()
        self.setFlags(self.ItemSendsScenePositionChanges)

    def _correct_ui(self):
        if self.point_type == 'input':
            pen = QtGui.QPen(QtCore.Qt.red, 2)
            controlBrush = QtGui.QBrush(QtGui.QColor(214, 13, 36))
            self.setPen(pen)
            self.setBrush(controlBrush)
            if self.point_pos == 'horizontal':
                self.setX(0)
                self.setY(int(self.gr_item.height/2))
            else:
                self.setX(int(self.gr_item.width/2))
                self.setY(0)
        else: # output
            pen = QtGui.QPen(QtCore.Qt.blue, 2)
            controlBrush = QtGui.QBrush(QtGui.QColor(4, 13, 36))
            self.setPen(pen)
            self.setBrush(controlBrush)   
            if self.point_pos == 'horizontal':
                self.setX(int(self.gr_item.width))
                self.setY(int(self.gr_item.height/2))
            else:
                self.setX(int(self.gr_item.width)/2)
                self.setY(int(self.gr_item.height))

    def get_pos(self):
        return self.mapToScene(self.pos()) - self.pos()

    def check_connection(self, start_node):
        """
        check if the start_node node can be connected to current node
        Args:
            start_node (ControlPoint): _description_
        """
        if self.point_type != start_node.point_type:
            s_gr_node = start_node.gr_item
            if self.point_type == 'input':
                if self.gr_item.node_name in s_gr_node.avl_nnodes and s_gr_node.node_name in self.gr_item.avl_pnodes:
                    if len(s_gr_node.nnodes)<s_gr_node.num_nnodes and len(self.gr_item.pnodes)<self.gr_item.num_pnodes:
                        if s_gr_node not in self.gr_item.pnodes and self.gr_item not in s_gr_node.nnodes:
                            return 1
            else:
                if self.gr_item.node_name in s_gr_node.avl_pnodes and s_gr_node.node_name in self.gr_item.avl_nnodes:
                    if len(s_gr_node.pnodes)<s_gr_node.num_pnodes and len(self.gr_item.nnodes)<self.gr_item.num_nnodes:
                        if s_gr_node not in self.gr_item.nnodes and self.gr_item not in s_gr_node.pnodes:
                            return 2
        return 0


# class StatePoint(QGraphicsEllipseItem):
#     def __init__(self, point_type, parent, point_pos):
#         super().__init__(-5, -5, 10, 10, parent)
#         self.gr_item = parent
#         self.point_type = point_type
#         self.point_pos = point_pos        
#         self._correct_ui()
#         self.setFlags(self.ItemSendsScenePositionChanges)

#     def _correct_ui(self):
#         if self.point_type == 'input':
#             pen = QtGui.QPen(QtCore.Qt.red, 2)
#             controlBrush = QtGui.QBrush(QtGui.QColor(214, 13, 36))
#             self.setPen(pen)
#             self.setBrush(controlBrush)
#             if self.point_pos == 'horizontal':
#                 self.setX(0)
#                 self.setY(int(self.gr_item.height/2))
#             else:
#                 self.setX(int(self.gr_item.width/2))
#                 self.setY(0)
#         else: # output
#             pen = QtGui.QPen(QtCore.Qt.blue, 2)
#             controlBrush = QtGui.QBrush(QtGui.QColor(4, 13, 36))
#             self.setPen(pen)
#             self.setBrush(controlBrush)   
#             if self.point_pos == 'horizontal':
#                 self.setX(int(self.gr_item.width))
#                 self.setY(int(self.gr_item.height/2))
#             else:
#                 self.setX(int(self.gr_item.width)/2)
#                 self.setY(int(self.gr_item.height))

#     def get_pos(self):
#         return self.mapToScene(self.pos()) - self.pos()

class ExternalBox():
    def __init__(self) -> None:
        pass

