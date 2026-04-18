#!/usr/bin/env python3
"""LabFlow 工具窗口管理器"""

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import QDockWidget, QMainWindow
import json
import os


class ToolWindowManager:
    """工具窗口管理器单例类"""
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, main_window=None):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.main_window = main_window
            self.tool_windows = {}
            self.settings = QSettings("LabFlow", "ToolWindowState")
            self.default_layouts = {
                "LeftDock": {
                    "area": Qt.LeftDockWidgetArea,
                    "visible": True,
                    "geometry": None
                },
                "PlotDock": {
                    "area": Qt.RightDockWidgetArea,
                    "visible": True,
                    "geometry": None
                },
                "PropertyDock": {
                    "area": Qt.RightDockWidgetArea,
                    "visible": True,
                    "geometry": None
                },
                "LogDock": {
                    "area": Qt.BottomDockWidgetArea,
                    "visible": True,
                    "geometry": None
                }
                # BottomDock 已删除，不再需要默认布局配置
            }
    
    def set_main_window(self, main_window):
        """设置主窗口"""
        self.main_window = main_window
    
    def register_tool_window(self, name, dock_widget):
        """注册工具窗口"""
        self.tool_windows[name] = dock_widget
        # 加载工具窗口状态
        self.load_tool_window_state(name)
    
    def get_tool_window(self, name):
        """获取工具窗口"""
        return self.tool_windows.get(name)
    
    def show_tool_window(self, name):
        """显示工具窗口"""
        if name in self.tool_windows:
            dock_widget = self.tool_windows[name]
            if not dock_widget.isVisible():
                dock_widget.show()
                # 保存工具窗口状态
                self.save_tool_window_state(name)
    
    def hide_tool_window(self, name):
        """隐藏工具窗口"""
        if name in self.tool_windows:
            dock_widget = self.tool_windows[name]
            if dock_widget.isVisible():
                dock_widget.hide()
                # 保存工具窗口状态
                self.save_tool_window_state(name)
    
    def toggle_tool_window(self, name):
        """切换工具窗口显示/隐藏状态"""
        if name in self.tool_windows:
            dock_widget = self.tool_windows[name]
            if dock_widget.isVisible():
                self.hide_tool_window(name)
            else:
                self.show_tool_window(name)
    
    def save_tool_window_state(self, name):
        """保存工具窗口状态"""
        if name in self.tool_windows:
            dock_widget = self.tool_windows[name]
            visible = dock_widget.isVisible()
            area = self.main_window.dockWidgetArea(dock_widget)
            geometry = dock_widget.saveGeometry()
            size = dock_widget.size()
            
            self.settings.setValue(f"{name}/visible", visible)
            self.settings.setValue(f"{name}/area", area)
            self.settings.setValue(f"{name}/geometry", geometry)
            self.settings.setValue(f"{name}/size_width", size.width())
            self.settings.setValue(f"{name}/size_height", size.height())
    
    def load_tool_window_state(self, name):
        """加载工具窗口状态"""
        if name in self.tool_windows:
            dock_widget = self.tool_windows[name]
            
            # 加载状态
            visible = self.settings.value(f"{name}/visible", self.default_layouts[name]["visible"], type=bool)
            area = self.settings.value(f"{name}/area", self.default_layouts[name]["area"], type=int)
            geometry = self.settings.value(f"{name}/geometry")
            size_width = self.settings.value(f"{name}/size_width", 0, type=int)
            size_height = self.settings.value(f"{name}/size_height", 0, type=int)
            
            # 应用状态
            if geometry:
                dock_widget.restoreGeometry(geometry)
            
            # 恢复大小
            if size_width > 0 and size_height > 0:
                dock_widget.resize(size_width, size_height)
            
            # 显示或隐藏面板
            if visible:
                dock_widget.show()
            else:
                dock_widget.hide()
    
    def save_all_tool_window_states(self):
        """保存所有工具窗口状态"""
        for name in self.tool_windows:
            self.save_tool_window_state(name)
        # 保存主窗口状态
        if self.main_window:
            self.settings.setValue("main_window/geometry", self.main_window.saveGeometry())
            self.settings.setValue("main_window/state", self.main_window.saveState())
    
    def load_all_tool_window_states(self):
        """加载所有工具窗口状态"""
        for name in self.tool_windows:
            self.load_tool_window_state(name)
        # 加载主窗口状态
        if self.main_window:
            geometry = self.settings.value("main_window/geometry")
            state = self.settings.value("main_window/state")
            if geometry:
                self.main_window.restoreGeometry(geometry)
            if state:
                self.main_window.restoreState(state)
    
    def reset_layout(self):
        """重置窗口布局"""
        # 重置所有工具窗口到默认位置
        for name, dock_widget in self.tool_windows.items():
            area = self.default_layouts[name]["area"]
            self.main_window.addDockWidget(area, dock_widget)
            dock_widget.show()
        # 保存重置后的状态
        self.save_all_tool_window_states()
