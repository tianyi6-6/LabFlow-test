#!/usr/bin/env python3
"""LabFlow 工具栏"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QToolBar
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, QAction


class Toolbar(QWidget):
    """工具栏类"""
    
    execute_workflow_signal = Signal()
    save_workflow_signal = Signal()
    load_workflow_signal = Signal()
    
    def __init__(self, parent=None):
        """初始化工具栏"""
        super().__init__(parent)
        
        # 创建布局
        layout = QHBoxLayout(self)
        
        # 创建执行按钮
        self.execute_button = QPushButton("执行工作流")
        self.execute_button.clicked.connect(self.execute_workflow_signal.emit)
        layout.addWidget(self.execute_button)
        
        # 创建保存按钮
        self.save_button = QPushButton("保存工作流")
        self.save_button.clicked.connect(self.save_workflow_signal.emit)
        layout.addWidget(self.save_button)
        
        # 创建加载按钮
        self.load_button = QPushButton("加载工作流")
        self.load_button.clicked.connect(self.load_workflow_signal.emit)
        layout.addWidget(self.load_button)
        
        # 添加分隔符
        layout.addStretch()
        
        # 创建清除按钮
        self.clear_button = QPushButton("清除画布")
        layout.addWidget(self.clear_button)
        
        # 创建缩放按钮
        self.zoom_in_button = QPushButton("放大")
        layout.addWidget(self.zoom_in_button)
        
        self.zoom_out_button = QPushButton("缩小")
        layout.addWidget(self.zoom_out_button)
        
        # 设置布局
        self.setLayout(layout)