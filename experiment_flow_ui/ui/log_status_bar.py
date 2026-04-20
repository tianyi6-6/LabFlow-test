#!/usr/bin/env python3
"""LabFlow 日志状态栏"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTextEdit, QLineEdit, QPushButton, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer
from labflow.utils.helpers import format_log_time
from .dock_panel import DockPanel
import psutil


class LogStatusBar(DockPanel):
    """日志状态栏"""
    
    def __init__(self, parent=None, name=None):
        super().__init__("日志状态栏", parent, name)
        self.logs = {
            "all": [],
            "info": [],
            "warning": [],
            "error": []
        }
        self.setup_ui()
        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_status)
        self.timer.start(1000)  # 1秒更新一次
    
    def setup_ui(self):
        """设置界面"""
        content_widget = QWidget()
        layout = QVBoxLayout()
        
        # 日志标签页
        self.tab_widget = QTabWidget()
        
        # 全部日志
        self.all_log_edit = QTextEdit()
        self.all_log_edit.setReadOnly(True)
        self.all_log_edit.setStyleSheet("background-color: black; color: white;")
        self.tab_widget.addTab(self.all_log_edit, "全部")
        
        # 信息日志
        self.info_log_edit = QTextEdit()
        self.info_log_edit.setReadOnly(True)
        self.info_log_edit.setStyleSheet("background-color: black; color: white;")
        self.tab_widget.addTab(self.info_log_edit, "信息")
        
        # 警告日志
        self.warning_log_edit = QTextEdit()
        self.warning_log_edit.setReadOnly(True)
        self.warning_log_edit.setStyleSheet("background-color: black; color: white;")
        self.tab_widget.addTab(self.warning_log_edit, "警告")
        
        # 错误日志
        self.error_log_edit = QTextEdit()
        self.error_log_edit.setReadOnly(True)
        self.error_log_edit.setStyleSheet("background-color: black; color: white;")
        self.tab_widget.addTab(self.error_log_edit, "错误")
        
        layout.addWidget(self.tab_widget, 1)
        
        # 日志搜索和操作 - 已删除多余控件
        # control_layout = QHBoxLayout()
        # 
        # 搜索框 - 已删除
        # self.search_edit = QLineEdit()
        # self.search_edit.setPlaceholderText("搜索日志")
        # control_layout.addWidget(self.search_edit)
        # 
        # 导出按钮 - 已删除
        # export_button = QPushButton("导出")
        # export_button.clicked.connect(self.export_logs)
        # control_layout.addWidget(export_button)
        # 
        # 清空按钮 - 已删除
        # clear_button = QPushButton("清空")
        # clear_button.clicked.connect(self.clear_logs)
        # control_layout.addWidget(clear_button)
        # 
        # layout.addLayout(control_layout)
        
        # 系统状态栏 - 缩小高度
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(10, 2, 10, 2)  # 减少垂直边距
        status_layout.setSpacing(5)  # 减少控件间距
        
        # 设备连接状态
        self.device_status_label = QLabel("设备: 0/0 未连接")
        self.device_status_label.setStyleSheet("color: red;")
        status_layout.addWidget(self.device_status_label)
        
        # 分隔符 - 减少间距
        status_layout.addSpacing(10)
        
        # CPU 占用
        self.cpu_label = QLabel("CPU: 0%")
        self.cpu_label.setStyleSheet("font-size: 10px;")  # 缩小字体
        status_layout.addWidget(self.cpu_label)
        
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setMaximumWidth(80)  # 缩小进度条宽度
        self.cpu_bar.setMaximum(100)
        self.cpu_bar.setValue(0)
        status_layout.addWidget(self.cpu_bar)
        
        # 分隔符 - 减少间距
        status_layout.addSpacing(10)
        
        # 内存占用
        self.memory_label = QLabel("内存: 0%")
        self.memory_label.setStyleSheet("font-size: 10px;")  # 缩小字体
        status_layout.addWidget(self.memory_label)
        
        self.memory_bar = QProgressBar()
        self.memory_bar.setMaximumWidth(80)  # 缩小进度条宽度
        self.memory_bar.setMaximum(100)
        self.memory_bar.setValue(0)
        status_layout.addWidget(self.memory_bar)
        
        # 分隔符 - 减少间距
        status_layout.addSpacing(10)
        
        # 运行状态
        self.run_status_label = QLabel("状态: 就绪")
        self.run_status_label.setStyleSheet("font-size: 10px;")  # 缩小字体
        status_layout.addWidget(self.run_status_label)
        
        layout.addLayout(status_layout)
        
        content_widget.setLayout(layout)
        self.add_content(content_widget)
        
        # 初始更新系统状态
        self.update_system_status()
    
    def add_log(self, message, level="info"):
        """添加日志"""
        timestamp = format_log_time()
        log_entry = f"[{timestamp}] {message}"
        
        # 添加到对应级别的日志列表
        self.logs["all"].append(log_entry)
        if level in self.logs:
            self.logs[level].append(log_entry)
        
        # 更新日志显示
        self.update_log_display()
    
    def update_log_display(self):
        """更新日志显示"""
        # 更新全部日志
        self.all_log_edit.setPlainText("\n".join(self.logs["all"]))
        self.all_log_edit.verticalScrollBar().setValue(self.all_log_edit.verticalScrollBar().maximum())
        
        # 更新信息日志
        self.info_log_edit.setPlainText("\n".join(self.logs["info"]))
        self.info_log_edit.verticalScrollBar().setValue(self.info_log_edit.verticalScrollBar().maximum())
        
        # 更新警告日志
        warning_text = "\n".join(self.logs["warning"])
        # 为警告日志添加黄色高亮
        self.warning_log_edit.setPlainText(warning_text)
        self.warning_log_edit.verticalScrollBar().setValue(self.warning_log_edit.verticalScrollBar().maximum())
        
        # 更新错误日志
        error_text = "\n".join(self.logs["error"])
        # 为错误日志添加红色高亮
        self.error_log_edit.setPlainText(error_text)
        self.error_log_edit.verticalScrollBar().setValue(self.error_log_edit.verticalScrollBar().maximum())
    
    def clear_logs(self):
        """清空日志"""
        for level in self.logs:
            self.logs[level].clear()
        self.update_log_display()
    
    def export_logs(self):
        """导出日志"""
        # 这里只是一个示例，实际实现应该打开文件对话框让用户选择保存位置
        import os
        import datetime
        
        # 创建导出目录
        export_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        os.makedirs(export_dir, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(export_dir, f"labflow_log_{timestamp}.txt")
        
        # 写入日志
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.logs["all"]))
        
        print(f"日志已导出到: {file_path}")
    
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
    
    def info(self, message):
        """添加信息日志"""
        self.add_log(message, "info")
    
    def warning(self, message):
        """添加警告日志"""
        self.add_log(message, "warning")
    
    def error(self, message):
        """添加错误日志"""
        self.add_log(message, "error")