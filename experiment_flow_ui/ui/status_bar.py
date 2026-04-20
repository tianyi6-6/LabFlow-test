#!/usr/bin/env python3
"""LabFlow 状态栏"""

from PySide6.QtWidgets import QStatusBar, QLabel, QProgressBar, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer
import psutil


class StatusBar(QStatusBar):
    """状态栏类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_status)
        self.timer.start(1000)  # 1秒更新一次
    
    def setup_ui(self):
        """设置界面"""
        # 创建状态栏部件
        status_widget = QWidget()
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(10, 0, 10, 0)
        
        # 设备连接状态
        self.device_status_label = QLabel("设备: 0/0 未连接")
        self.device_status_label.setStyleSheet("color: red;")
        status_layout.addWidget(self.device_status_label)
        
        # 分隔符
        status_layout.addSpacing(20)
        
        # CPU 占用
        self.cpu_label = QLabel("CPU: 0%")
        status_layout.addWidget(self.cpu_label)
        
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setMaximumWidth(100)
        self.cpu_bar.setMaximum(100)
        self.cpu_bar.setValue(0)
        status_layout.addWidget(self.cpu_bar)
        
        # 分隔符
        status_layout.addSpacing(20)
        
        # 内存占用
        self.memory_label = QLabel("内存: 0%")
        status_layout.addWidget(self.memory_label)
        
        self.memory_bar = QProgressBar()
        self.memory_bar.setMaximumWidth(100)
        self.memory_bar.setMaximum(100)
        self.memory_bar.setValue(0)
        status_layout.addWidget(self.memory_bar)
        
        # 分隔符
        status_layout.addSpacing(20)
        
        # 运行状态
        self.run_status_label = QLabel("状态: 就绪")
        status_layout.addWidget(self.run_status_label)
        
        status_widget.setLayout(status_layout)
        self.addWidget(status_widget, 1)
    
    def update_system_status(self):
        """更新系统状态"""
        # 获取 CPU 占用
        cpu_percent = psutil.cpu_percent()
        self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
        self.cpu_bar.setValue(int(cpu_percent))
        
        # 获取内存占用
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        self.memory_label.setText(f"内存: {memory_percent:.1f}%")
        self.memory_bar.setValue(int(memory_percent))
    
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
        self.device_status_label.setStyleSheet(f"color: {status_color};")
    
    def set_run_status(self, status):
        """设置运行状态"""
        status_text = f"状态: {status}"
        self.run_status_label.setText(status_text)