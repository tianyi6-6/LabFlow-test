#!/usr/bin/env python3
"""LabFlow 属性面板"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QGroupBox, QLabel
from PySide6.QtCore import Qt


class PropertyPanel(QWidget):
    """属性面板类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.current_node = None
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout()
        
        # 精简状态条
        status_bar = QWidget()
        status_bar.setFixedHeight(24)
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(5, 2, 5, 2)
        status_layout.setSpacing(10)
        
        # 设备连接状态
        self.device_status_label = QLabel("设备: 0/0 未连接")
        self.device_status_label.setStyleSheet("font-size: 11px; color: red;")
        status_layout.addWidget(self.device_status_label)
        
        # 分隔符
        status_layout.addStretch()
        
        # 运行状态
        self.run_status_label = QLabel("状态: 就绪")
        self.run_status_label.setStyleSheet("font-size: 11px;")
        status_layout.addWidget(self.run_status_label)
        
        status_bar.setLayout(status_layout)
        layout.addWidget(status_bar)
        
        # 属性面板标题
        title = QLabel("参数配置")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(self.font())
        layout.addWidget(title)
        
        # 属性组
        self.property_group = QGroupBox()
        self.property_layout = QFormLayout()
        self.property_group.setLayout(self.property_layout)
        layout.addWidget(self.property_group)
        
        # 空状态
        self.empty_label = QLabel("请选择一个节点")
        self.empty_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.empty_label)
        
        self.setLayout(layout)
    
    def set_device_status(self, connected_count, total_count):
        """设置设备状态"""
        if total_count == 0:
            status_text = "设备: 0/0 未连接"
            status_color = "red"
        elif connected_count == total_count:
            status_text = f"设备: {connected_count}/{total_count} 正常工作"
            status_color = "green"
        else:
            status_text = f"设备: {connected_count}/{total_count} 部分连接"
            status_color = "yellow"
        
        self.device_status_label.setText(status_text)
        self.device_status_label.setStyleSheet(f"font-size: 11px; color: {status_color};")
    
    def set_run_status(self, status):
        """设置运行状态"""
        status_text = f"状态: {status}"
        self.run_status_label.setText(status_text)
        self.run_status_label.setStyleSheet("font-size: 11px;")
    
    def set_node(self, node):
        """设置当前节点"""
        self.current_node = node
        self.update_properties()
    
    def update_properties(self):
        """更新属性"""
        # 清空布局
        while self.property_layout.count() > 0:
            item = self.property_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        if self.current_node:
            # 显示属性组
            self.property_group.setVisible(True)
            self.empty_label.setVisible(False)
            
            # 设置属性组标题
            self.property_group.setTitle(f"{self.current_node.name} 属性")
            
            # 添加属性
            for key, value in self.current_node.properties.items():
                if isinstance(value, str):
                    # 字符串类型
                    editor = QLineEdit(str(value))
                    editor.textChanged.connect(lambda text, k=key: self.on_property_changed(k, text))
                elif isinstance(value, bool):
                    # 布尔类型
                    editor = QCheckBox()
                    editor.setChecked(value)
                    editor.stateChanged.connect(lambda state, k=key: self.on_property_changed(k, bool(state)))
                elif isinstance(value, int):
                    # 整数类型
                    editor = QSpinBox()
                    editor.setValue(value)
                    editor.valueChanged.connect(lambda value, k=key: self.on_property_changed(k, value))
                elif isinstance(value, float):
                    # 浮点数类型
                    editor = QDoubleSpinBox()
                    editor.setValue(value)
                    editor.valueChanged.connect(lambda value, k=key: self.on_property_changed(k, value))
                else:
                    # 其他类型，使用字符串编辑器
                    editor = QLineEdit(str(value))
                    editor.textChanged.connect(lambda text, k=key: self.on_property_changed(k, text))
                
                # 添加到布局
                self.property_layout.addRow(key, editor)
        else:
            # 显示空状态
            self.property_group.setVisible(False)
            self.empty_label.setVisible(True)
    
    def on_property_changed(self, key, value):
        """属性变化回调"""
        if self.current_node:
            self.current_node.set_property(key, value)
            print(f"节点 {self.current_node.name} 的属性 {key} 已更新为: {value}")
    
    def clear(self):
        """清空属性面板"""
        self.set_node(None)