#!/usr/bin/env python3
"""LabFlow 可停靠面板基类"""

from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QIcon, QFont
from .tool_window_manager import ToolWindowManager


class DockPanel(QDockWidget):
    """可停靠面板基类"""
    
    def __init__(self, title, parent=None, name=None):
        super().__init__(title, parent)
        self.name = name
        self.setFeatures(QDockWidget.DockWidgetMovable | 
                        QDockWidget.DockWidgetFloatable | 
                        QDockWidget.DockWidgetClosable)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | 
                           Qt.RightDockWidgetArea | 
                           Qt.TopDockWidgetArea | 
                           Qt.BottomDockWidgetArea)
        
        # 创建面板内容
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.setWidget(self.content_widget)
        
        # 设置面板样式
        self.setStyleSheet("""
            QDockWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
            }
            QDockWidget::title {
                background-color: #f5f5f5;
                padding: 5px;
                text-align: center;
            }
        """)
    
    def closeEvent(self, event):
        """拦截关闭事件，改为隐藏面板"""
        event.ignore()  # 忽略关闭事件
        if self.name:
            tool_window_manager = ToolWindowManager()
            tool_window_manager.hide_tool_window(self.name)
    
    def add_content(self, widget):
        """添加内容到面板"""
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """添加布局到面板"""
        self.content_layout.addLayout(layout)
    
    def set_content_margins(self, left, top, right, bottom):
        """设置内容边距"""
        self.content_layout.setContentsMargins(left, top, right, bottom)
    
    def add_stretch(self, stretch=0):
        """添加伸缩空间"""
        self.content_layout.addStretch(stretch)
