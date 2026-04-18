#!/usr/bin/env python3
"""LabFlow 节点画布"""

from PySide6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem, QMenu
from PySide6.QtGui import QPen, QBrush, QColor, QFont, QCursor, QMouseEvent, QPainter
from PySide6.QtCore import Qt, QPointF, QRectF, QSizeF
import math


class NodeItem(QGraphicsItem):
    """节点图形项"""
    
    def __init__(self, node_id, name, inputs=None, outputs=None, node_type="base"):
        super().__init__()
        self.node_id = node_id
        self.name = name
        self.inputs = inputs or []
        self.outputs = outputs or []
        self.node_type = node_type
        self.status = "idle"  # idle, running, success, error
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        
        # 节点尺寸
        self.width = 200
        self.height = 100 + max(len(self.inputs), len(self.outputs)) * 20
        
        # 端口位置
        self.input_ports = []
        self.output_ports = []
        self._update_ports()
    
    def _update_ports(self):
        """更新端口位置"""
        # 输入端口
        self.input_ports = []
        for i, input_name in enumerate(self.inputs):
            y = 40 + i * 20
            self.input_ports.append((input_name, QPointF(0, y)))
        
        # 输出端口
        self.output_ports = []
        for i, output_name in enumerate(self.outputs):
            y = 40 + i * 20
            self.output_ports.append((output_name, QPointF(self.width, y)))
    
    def boundingRect(self):
        """返回节点的边界矩形"""
        return QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter, option, widget):
        """绘制节点"""
        # 节点背景
        if self.node_type == "device_control":
            color = QColor("#FFB347")  # 浅橙色
        elif self.node_type == "visualization":
            color = QColor("#D2B48C")  # 浅棕色
        else:
            color = QColor("#808080")  # 灰色
        
        # 状态颜色
        if self.status == "running":
            border_color = QColor("#FFA500")  # 橙色
        elif self.status == "success":
            border_color = QColor("#00FF00")  # 绿色
        elif self.status == "error":
            border_color = QColor("#FF0000")  # 红色
        else:
            border_color = QColor("#000000")  # 黑色
        
        # 绘制节点背景
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(border_color, 2))
        painter.drawRect(0, 0, self.width, self.height)
        
        # 绘制节点名称
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(10, 20, self.name)
        
        # 绘制输入端口
        painter.setFont(QFont("Arial", 8))
        for input_name, pos in self.input_ports:
            # 绘制端口圆圈
            painter.setBrush(QBrush(QColor("#4169E1")))  # 蓝色
            painter.setPen(QPen(QColor("#000000"), 1))
            painter.drawEllipse(pos.x() - 5, pos.y() - 5, 10, 10)
            # 绘制端口名称
            painter.setPen(QPen(QColor("#000000")))
            painter.drawText(pos.x() + 5, pos.y() + 5, input_name)
        
        # 绘制输出端口
        for output_name, pos in self.output_ports:
            # 绘制端口圆圈
            painter.setBrush(QBrush(QColor("#FFD700")))  # 黄色
            painter.setPen(QPen(QColor("#000000"), 1))
            painter.drawEllipse(pos.x() - 5, pos.y() - 5, 10, 10)
            # 绘制端口名称
            painter.setPen(QPen(QColor("#000000")))
            painter.drawText(pos.x() - 50, pos.y() + 5, output_name)
    
    def get_port_position(self, port_name, is_input):
        """获取端口位置"""
        ports = self.input_ports if is_input else self.output_ports
        for name, pos in ports:
            if name == port_name:
                return self.mapToScene(pos)
        return None
    
    def set_status(self, status):
        """设置节点状态"""
        self.status = status
        self.update()
    
    def itemChange(self, change, value):
        """处理项目变化"""
        if change == QGraphicsItem.ItemPositionChange:
            # 节点位置变化时，需要更新连线
            pass
        return super().itemChange(change, value)


class EdgeItem(QGraphicsItem):
    """边图形项"""
    
    def __init__(self, source_node, source_port, target_node, target_port):
        super().__init__()
        self.source_node = source_node
        self.source_port = source_port
        self.target_node = target_node
        self.target_port = target_port
        self.setZValue(-1)  # 边在节点下方
    
    def boundingRect(self):
        """返回边的边界矩形"""
        source_pos = self.source_node.get_port_position(self.source_port, is_input=False)
        target_pos = self.target_node.get_port_position(self.target_port, is_input=True)
        if not source_pos or not target_pos:
            return QRectF()
        
        x_min = min(source_pos.x(), target_pos.x())
        y_min = min(source_pos.y(), target_pos.y())
        x_max = max(source_pos.x(), target_pos.x())
        y_max = max(source_pos.y(), target_pos.y())
        
        return QRectF(x_min - 10, y_min - 10, x_max - x_min + 20, y_max - y_min + 20)
    
    def paint(self, painter, option, widget):
        """绘制边"""
        source_pos = self.source_node.get_port_position(self.source_port, is_input=False)
        target_pos = self.target_node.get_port_position(self.target_port, is_input=True)
        if not source_pos or not target_pos:
            return
        
        # 绘制贝塞尔曲线
        painter.setPen(QPen(QColor("#4169E1"), 2, Qt.DashLine))
        
        # 计算控制点
        mid_x = (source_pos.x() + target_pos.x()) / 2
        control_point1 = QPointF(source_pos.x() + 50, source_pos.y())
        control_point2 = QPointF(target_pos.x() - 50, target_pos.y())
        
        painter.drawBezierCurve(
            source_pos,
            control_point1,
            control_point2,
            target_pos
        )
    
    def update_position(self):
        """更新边的位置"""
        self.prepareGeometryChange()
        self.update()


class NodeCanvas(QGraphicsView):
    """节点画布"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # 设置画布属性
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        
        # 缩放功能
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
        # 网格设置
        self.grid_size = 20
        self.draw_grid()
        
        # 连线相关
        self.is_dragging = False
        self.start_node = None
        self.start_port = None
        self.temp_edge = None
        
        # 节点和边的映射
        self.nodes = {}
        self.edges = []
    
    def draw_grid(self):
        """绘制网格"""
        self.scene.clear()
        
        # 绘制网格线
        pen = QPen(QColor("#E0E0E0"), 0.5)
        
        # 计算网格范围
        width = 2000
        height = 2000
        
        for x in range(0, width, self.grid_size):
            self.scene.addLine(x, 0, x, height, pen)
        for y in range(0, height, self.grid_size):
            self.scene.addLine(0, y, width, y, pen)
        
        # 设置场景范围
        self.scene.setSceneRect(0, 0, width, height)
    
    def add_node(self, node_id, name, inputs=None, outputs=None, node_type="base", position=None):
        """添加节点"""
        node_item = NodeItem(node_id, name, inputs, outputs, node_type)
        if position:
            node_item.setPos(position)
        else:
            # 默认位置
            node_item.setPos(100, 100)
        
        self.scene.addItem(node_item)
        self.nodes[node_id] = node_item
        return node_item
    
    def remove_node(self, node_id):
        """移除节点"""
        if node_id in self.nodes:
            node_item = self.nodes[node_id]
            # 移除与该节点相关的所有边
            edges_to_remove = []
            for edge in self.edges:
                if edge.source_node == node_item or edge.target_node == node_item:
                    edges_to_remove.append(edge)
            
            for edge in edges_to_remove:
                self.scene.removeItem(edge)
                self.edges.remove(edge)
            
            # 移除节点
            self.scene.removeItem(node_item)
            del self.nodes[node_id]
    
    def add_edge(self, source_node_id, source_port, target_node_id, target_port):
        """添加边"""
        if source_node_id in self.nodes and target_node_id in self.nodes:
            source_node = self.nodes[source_node_id]
            target_node = self.nodes[target_node_id]
            
            edge_item = EdgeItem(source_node, source_port, target_node, target_port)
            self.scene.addItem(edge_item)
            self.edges.append(edge_item)
            return edge_item
        return None
    
    def remove_edge(self, source_node_id, source_port, target_node_id, target_port):
        """移除边"""
        for edge in self.edges:
            if (edge.source_node.node_id == source_node_id and 
                edge.source_port == source_port and 
                edge.target_node.node_id == target_node_id and 
                edge.target_port == target_port):
                self.scene.removeItem(edge)
                self.edges.remove(edge)
                return True
        return False
    
    def wheelEvent(self, event):
        """处理鼠标滚轮事件，实现缩放"""
        zoom_factor = 1.1
        if event.angleDelta().y() > 0:
            # 放大
            self.scale(zoom_factor, zoom_factor)
        else:
            # 缩小
            self.scale(1/zoom_factor, 1/zoom_factor)
    
    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        # 检查是否点击了端口
        pos = self.mapToScene(event.pos())
        items = self.scene.items(pos)
        
        # 检查是否点击了节点的端口
        for item in items:
            if isinstance(item, NodeItem):
                # 检查输入端口
                for input_name, port_pos in item.input_ports:
                    port_scene_pos = item.mapToScene(port_pos)
                    if (pos.x() - port_scene_pos.x()) ** 2 + (pos.y() - port_scene_pos.y()) ** 2 < 25:
                        # 点击了输入端口，开始连线
                        self.is_dragging = True
                        self.start_node = item
                        self.start_port = input_name
                        return
                
                # 检查输出端口
                for output_name, port_pos in item.output_ports:
                    port_scene_pos = item.mapToScene(port_pos)
                    if (pos.x() - port_scene_pos.x()) ** 2 + (pos.y() - port_scene_pos.y()) ** 2 < 25:
                        # 点击了输出端口，开始连线
                        self.is_dragging = True
                        self.start_node = item
                        self.start_port = output_name
                        return
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """处理鼠标移动事件"""
        if self.is_dragging:
            # 绘制临时连线
            pos = self.mapToScene(event.pos())
            if self.temp_edge:
                self.scene.removeItem(self.temp_edge)
            
            # 创建临时连线
            from PySide6.QtWidgets import QGraphicsLineItem
            start_pos = self.start_node.get_port_position(self.start_port, 
                                                       is_input=self.start_port in [p[0] for p in self.start_node.input_ports])
            if start_pos:
                self.temp_edge = QGraphicsLineItem(start_pos.x(), start_pos.y(), pos.x(), pos.y())
                self.temp_edge.setPen(QPen(QColor("#4169E1"), 2, Qt.DashLine))
                self.scene.addItem(self.temp_edge)
        else:
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """处理鼠标释放事件"""
        if self.is_dragging:
            # 完成连线
            pos = self.mapToScene(event.pos())
            items = self.scene.items(pos)
            
            # 检查是否释放到了另一个节点的端口
            for item in items:
                if isinstance(item, NodeItem) and item != self.start_node:
                    # 检查输入端口
                    for input_name, port_pos in item.input_ports:
                        port_scene_pos = item.mapToScene(port_pos)
                        if (pos.x() - port_scene_pos.x()) ** 2 + (pos.y() - port_scene_pos.y()) ** 2 < 25:
                            # 连接到输入端口
                            if self.start_port in [p[0] for p in self.start_node.output_ports]:
                                # 从输出端口到输入端口
                                self.add_edge(self.start_node.node_id, self.start_port, item.node_id, input_name)
                            break
                    
                    # 检查输出端口
                    for output_name, port_pos in item.output_ports:
                        port_scene_pos = item.mapToScene(port_pos)
                        if (pos.x() - port_scene_pos.x()) ** 2 + (pos.y() - port_scene_pos.y()) ** 2 < 25:
                            # 连接到输出端口
                            if self.start_port in [p[0] for p in self.start_node.input_ports]:
                                # 从输入端口到输出端口
                                self.add_edge(item.node_id, output_name, self.start_node.node_id, self.start_port)
                            break
            
            # 清理临时连线
            if self.temp_edge:
                self.scene.removeItem(self.temp_edge)
                self.temp_edge = None
            
            self.is_dragging = False
            self.start_node = None
            self.start_port = None
        else:
            super().mouseReleaseEvent(event)
    
    def contextMenuEvent(self, event):
        """处理上下文菜单事件"""
        menu = QMenu()
        
        # 添加菜单项
        add_node_action = menu.addAction("添加节点")
        delete_action = menu.addAction("删除")
        copy_action = menu.addAction("复制")
        paste_action = menu.addAction("粘贴")
        
        # 执行菜单项
        action = menu.exec_(event.globalPos())
        if action == delete_action:
            # 删除选中的节点和边
            for item in self.scene.selectedItems():
                if isinstance(item, NodeItem):
                    self.remove_node(item.node_id)
                elif isinstance(item, EdgeItem):
                    self.scene.removeItem(item)
                    self.edges.remove(item)
    
    def update_node_status(self, node_id, status):
        """更新节点状态"""
        if node_id in self.nodes:
            self.nodes[node_id].set_status(status)
    
    def clear(self):
        """清空画布"""
        self.scene.clear()
        self.draw_grid()
        self.nodes.clear()
        self.edges.clear()