#!/usr/bin/env python3
"""LabFlow 节点画布"""

from PySide6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem, QMenu, QLineEdit, QComboBox
from PySide6.QtGui import QPen, QBrush, QColor, QFont, QCursor, QMouseEvent, QPainter, QTransform
from PySide6.QtCore import Qt, QPointF, QRectF, QSizeF, QMimeData, Signal, Slot
import math
import json
from experiment_flow_ui.core.base_workflow import Workflow
from experiment_flow_ui.core.base_node import BaseNode


class NodeItem(QGraphicsItem):
    """节点图形项"""
    
    # 定义信号
    property_changed = Signal(str, object)  # 信号：参数变更
    
    def __init__(self, node_id, name, inputs=None, outputs=None, node_type="base", properties=None):
        super().__init__()
        self.node_id = node_id
        self.name = name
        self.inputs = inputs or []
        self.outputs = outputs or []
        self.node_type = node_type
        self.status = "idle"  # idle, running, success, error
        self.properties = properties or {}
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        
        # 节点尺寸
        self.width = 200
        # 计算高度：标题栏30 + 端口区域 + 参数区域
        self.height = 30 + max(len(self.inputs), len(self.outputs)) * 25 + len(self.properties) * 30
        
        # 端口位置
        self.input_ports = []
        self.output_ports = []
        self._update_ports()
        
        # 内嵌控件
        self.parameter_widgets = {}
        self._create_parameter_widgets()
    
    def _update_ports(self):
        """更新端口位置"""
        # 输入端口
        self.input_ports = []
        for i, input_name in enumerate(self.inputs):
            y = 50 + i * 25  # 调整垂直间距
            self.input_ports.append((input_name, QPointF(10, y)))
        
        # 输出端口
        self.output_ports = []
        for i, output_name in enumerate(self.outputs):
            y = 50 + i * 25  # 调整垂直间距
            self.output_ports.append((output_name, QPointF(self.width - 10, y)))
    
    def _create_parameter_widgets(self):
        """创建参数编辑控件"""
        # 清除现有的控件
        for widget in self.parameter_widgets.values():
            widget.deleteLater()
        self.parameter_widgets.clear()
        
        # 为每个属性创建控件
        for i, (key, value) in enumerate(self.properties.items()):
            # 计算控件位置
            y = 30 + max(len(self.inputs), len(self.outputs)) * 25 + i * 30
            
            # 创建标签
            from PySide6.QtWidgets import QLabel
            label = QLabel(key)
            label.setParent(self.scene().parent())
            label.setGeometry(int(self.x() + 10), int(self.y() + y + 5), 100, 20)
            label.show()
            
            # 创建输入控件
            if isinstance(value, str) and " " in value:
                # 如果值包含空格，可能是选项列表
                options = value.split()
                widget = QComboBox()
                widget.addItems(options)
                widget.setCurrentText(options[0])
            else:
                # 否则使用文本输入框
                widget = QLineEdit(str(value))
            
            # 设置控件属性
            widget.setParent(self.scene().parent())
            widget.setGeometry(int(self.x() + 110), int(self.y() + y), 80, 25)
            widget.show()
            
            # 连接信号
            if isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda text, k=key: self._on_property_changed(k, text))
            elif isinstance(widget, QComboBox):
                widget.currentTextChanged.connect(lambda text, k=key: self._on_property_changed(k, text))
            
            # 保存控件
            self.parameter_widgets[key] = (label, widget)
    
    def _on_property_changed(self, key, value):
        """处理参数变更"""
        # 更新属性值
        self.properties[key] = value
        # 发射信号
        self.property_changed.emit(key, value)
    
    def update_parameter_widgets_position(self):
        """更新参数控件的位置"""
        for i, (key, (label, widget)) in enumerate(self.parameter_widgets.items()):
            y = 30 + max(len(self.inputs), len(self.outputs)) * 25 + i * 30
            label.setGeometry(int(self.x() + 10), int(self.y() + y + 5), 100, 20)
            widget.setGeometry(int(self.x() + 110), int(self.y() + y), 80, 25)
    
    def add_parameter(self, name, value):
        """添加参数"""
        self.properties[name] = value
        # 重新计算高度
        self.height = 30 + max(len(self.inputs), len(self.outputs)) * 25 + len(self.properties) * 30
        # 重新创建控件
        self._create_parameter_widgets()
        # 更新
        self.update()
    
    def remove_parameter(self, name):
        """移除参数"""
        if name in self.properties:
            del self.properties[name]
            # 重新计算高度
            self.height = 30 + max(len(self.inputs), len(self.outputs)) * 25 + len(self.properties) * 30
            # 重新创建控件
            self._create_parameter_widgets()
            # 更新
            self.update()
    
    def boundingRect(self):
        """返回节点的边界矩形"""
        return QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter, option, widget):
        """绘制节点"""
        # 节点背景
        if self.node_type == "device_control":
            title_color = QColor("#FFB347")  # 浅橙色
        elif self.node_type == "visualization":
            title_color = QColor("#D2B48C")  # 浅棕色
        elif self.node_type == "data_acquisition":
            title_color = QColor("#87CEEB")  # 天空蓝
        elif self.node_type == "signal_processing":
            title_color = QColor("#98FB98")  # 淡绿色
        elif self.node_type == "control_flow":
            title_color = QColor("#DDA0DD")  #  plum
        else:
            title_color = QColor("#808080")  # 灰色
        
        # 状态颜色
        if self.status == "running":
            border_color = QColor("#FFA500")  # 橙色
        elif self.status == "success":
            border_color = QColor("#00FF00")  # 绿色
        elif self.status == "error":
            border_color = QColor("#FF0000")  # 红色
        else:
            border_color = QColor("#000000")  # 黑色
        
        # 绘制阴影效果
        painter.setPen(QPen(QColor("#808080"), 0))
        painter.setBrush(QBrush(QColor("#808080", 50)))
        painter.drawRoundedRect(5, 5, self.width, self.height, 8, 8)
        
        # 绘制节点背景
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.setPen(QPen(border_color, 2))
        painter.drawRoundedRect(0, 0, self.width, self.height, 8, 8)
        
        # 绘制标题栏
        painter.setBrush(QBrush(title_color))
        painter.setPen(QPen(QColor("#000000"), 1))
        painter.drawRoundedRect(0, 0, self.width, 30, 8, 8)
        
        # 绘制节点名称
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.setPen(QPen(QColor("#000000")))
        painter.drawText(10, 20, self.name)
        
        # 绘制输入端口
        painter.setFont(QFont("Arial", 8))
        for i, (input_name, pos) in enumerate(self.input_ports):
            # 绘制端口圆圈
            painter.setBrush(QBrush(QColor("#4169E1")))
            painter.setPen(QPen(QColor("#000000"), 1))
            painter.drawEllipse(pos.x() - 5, pos.y() - 5, 10, 10)
            # 绘制端口名称
            painter.setPen(QPen(QColor("#000000")))
            painter.drawText(pos.x() + 10, pos.y() + 5, input_name)
        
        # 绘制输出端口
        for i, (output_name, pos) in enumerate(self.output_ports):
            # 绘制端口圆圈
            painter.setBrush(QBrush(QColor("#FFD700")))
            painter.setPen(QPen(QColor("#000000"), 1))
            painter.drawEllipse(pos.x() - 5, pos.y() - 5, 10, 10)
            # 绘制端口名称
            painter.setPen(QPen(QColor("#000000")))
            painter.drawText(pos.x() - 60, pos.y() + 5, output_name)
    
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
            # 更新参数控件位置
            self.update_parameter_widgets_position()
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
        # 对于水平方向的连线，控制点在两侧
        # 对于垂直方向的连线，控制点在中间
        dx = target_pos.x() - source_pos.x()
        dy = target_pos.y() - source_pos.y()
        
        # 计算控制点距离
        control_distance = abs(dx) * 0.3
        if control_distance < 50:
            control_distance = 50
        
        control_point1 = QPointF(source_pos.x() + control_distance, source_pos.y())
        control_point2 = QPointF(target_pos.x() - control_distance, target_pos.y())
        
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
    
    def __init__(self, parent=None, workflow=None):
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
        
        # Workflow 实例引用
        self.workflow = workflow or Workflow()
        
        # 开启拖拽接收
        self.setAcceptDrops(True)
    
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
    
    def add_node(self, node_id, name, inputs=None, outputs=None, node_type="base", position=None, properties=None):
        """添加节点"""
        node_item = NodeItem(node_id, name, inputs, outputs, node_type, properties)
        if position:
            node_item.setPos(position)
        else:
            # 默认位置
            node_item.setPos(100, 100)
        
        self.scene.addItem(node_item)
        self.nodes[node_id] = node_item
        
        # 创建对应的 BaseNode 实例并添加到 Workflow
        base_node = BaseNode(node_id=node_id, name=name)
        base_node.node_type = node_type
        base_node.inputs = inputs or []
        base_node.outputs = outputs or []
        base_node.position = (node_item.x(), node_item.y())
        base_node.properties = properties or {}
        self.workflow.add_node(base_node)
        
        # 连接参数变更信号
        def on_property_changed(key, value):
            # 更新 Workflow 中的节点属性
            node = self.workflow.get_node(node_id)
            if node:
                node.properties[key] = value
        
        node_item.property_changed.connect(on_property_changed)
        
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
            
            # 从 Workflow 中移除节点
            self.workflow.remove_node(node_id)
    
    def add_edge(self, source_node_id, source_port, target_node_id, target_port):
        """添加边"""
        if source_node_id in self.nodes and target_node_id in self.nodes:
            source_node = self.nodes[source_node_id]
            target_node = self.nodes[target_node_id]
            
            edge_item = EdgeItem(source_node, source_port, target_node, target_port)
            self.scene.addItem(edge_item)
            self.edges.append(edge_item)
            
            # 添加边到 Workflow
            self.workflow.add_edge(source_node_id, source_port, target_node_id, target_port)
            
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
                
                # 从 Workflow 中移除边
                self.workflow.remove_edge(source_node_id, source_port, target_node_id, target_port)
                
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
    
    def set_workflow(self, workflow):
        """设置 Workflow 实例"""
        self.workflow = workflow
        # 同步 Workflow 到画布
        self.clear()
        for node_id, node in self.workflow.nodes.items():
            self.add_node(
                node_id=node.node_id,
                name=node.name,
                inputs=node.inputs,
                outputs=node.outputs,
                node_type=node.node_type,
                position=node.position
            )
        for edge in self.workflow.edges:
            source_node_id, source_port, target_node_id, target_port = edge
            self.add_edge(source_node_id, source_port, target_node_id, target_port)
    
    def clear(self):
        """清空画布"""
        self.scene.clear()
        self.draw_grid()
        self.nodes.clear()
        self.edges.clear()
        # 清空 Workflow
        self.workflow.clear()
    
    def dragEnterEvent(self, event):
        """处理拖拽进入事件"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """处理拖拽释放事件"""
        if event.mimeData().hasText():
            # 解析拖拽数据
            try:
                node_info = json.loads(event.mimeData().text())
                
                # 计算节点位置
                pos = self.mapToScene(event.pos())
                # 对齐到网格
                grid_pos = QPointF(
                    round(pos.x() / self.grid_size) * self.grid_size,
                    round(pos.y() / self.grid_size) * self.grid_size
                )
                
                # 生成唯一的节点 ID
                node_id = f"node_{len(self.nodes) + 1}"
                
                # 为不同类型的节点设置默认属性
                properties = self._get_default_properties(node_info["name"])
                
                # 创建节点
                node_item = self.add_node(
                    node_id=node_id,
                    name=node_info["name"],
                    inputs=node_info["inputs"],
                    outputs=node_info["outputs"],
                    node_type=node_info["node_type"],
                    position=grid_pos,
                    properties=properties
                )
                
                # 设置节点位置
                node_item.setPos(grid_pos)
                
                event.acceptProposedAction()
            except Exception as e:
                print(f"处理拖拽事件失败: {e}")
    
    def _get_default_properties(self, node_name):
        """获取节点的默认属性"""
        properties_map = {
            "SetLockInFreq": {"freq_value": "1000"},
            "SetLockInPhase": {"phase_value": "0"},
            "SetLockInTimeCo": {"time_constant": "100ms", "sensitivity": "24dB"},
            "SetDataSampleRate": {"sample_rate": "1000"},
            "get_max_slope": {},
            "lockin_res": {},
            "log_insert_compile": {},
            "循环_重复遍历": {"iterations": "10"},
            "add_row_data": {},
            "set_plot": {},
            "add_data_line": {}
        }
        return properties_map.get(node_name, {})