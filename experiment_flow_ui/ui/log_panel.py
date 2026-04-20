#!/usr/bin/env python3
"""LabFlow 日志面板"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTextEdit, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt
from experiment_flow_ui.utils.helpers import format_log_time


class LogPanel(QWidget):
    """日志面板类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.logs = {
            "all": [],
            "info": [],
            "warning": [],
            "error": []
        }
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout()
        # 设置布局边距为0，最大化日志显示区域
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 日志面板标题 - 已删除，避免重复
        # title = QLabel("日志")
        # title.setAlignment(Qt.AlignCenter)
        # title.setFont(self.font())
        # layout.addWidget(title)
        
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
        
        # 日志搜索和操作 - 已删除
        # control_layout = QHBoxLayout()
        # 
        # # 搜索框 - 已删除
        # self.search_edit = QLineEdit()
        # self.search_edit.setPlaceholderText("搜索日志")
        # control_layout.addWidget(self.search_edit)
        # 
        # # 导出按钮 - 已删除
        # export_button = QPushButton("导出")
        # export_button.clicked.connect(self.export_logs)
        # control_layout.addWidget(export_button)
        # 
        # # 清空按钮 - 已删除
        # clear_button = QPushButton("清空")
        # clear_button.clicked.connect(self.clear_logs)
        # control_layout.addWidget(clear_button)
        # 
        # layout.addLayout(control_layout)
        
        self.setLayout(layout)
    
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
    
    def info(self, message):
        """添加信息日志"""
        self.add_log(message, "info")
    
    def warning(self, message):
        """添加警告日志"""
        self.add_log(message, "warning")
    
    def error(self, message):
        """添加错误日志"""
        self.add_log(message, "error")