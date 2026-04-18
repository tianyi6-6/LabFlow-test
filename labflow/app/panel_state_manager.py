#!/usr/bin/env python3
"""LabFlow 面板状态管理器"""

import json
import os
from PySide6.QtCore import QSettings


class PanelStateManager:
    """面板状态管理器"""
    
    def __init__(self, app_name="LabFlow"):
        self.app_name = app_name
        self.settings = QSettings(app_name, "PanelState")
    
    def save_panel_state(self, panel_name, geometry, floating, area, visible):
        """保存面板状态"""
        self.settings.setValue(f"{panel_name}/geometry", geometry)
        self.settings.setValue(f"{panel_name}/floating", floating)
        self.settings.setValue(f"{panel_name}/area", area)
        self.settings.setValue(f"{panel_name}/visible", visible)
    
    def load_panel_state(self, panel_name):
        """加载面板状态"""
        geometry = self.settings.value(f"{panel_name}/geometry")
        floating = self.settings.value(f"{panel_name}/floating", False, type=bool)
        area = self.settings.value(f"{panel_name}/area", 1, type=int)  # 默认左侧
        visible = self.settings.value(f"{panel_name}/visible", True, type=bool)
        return geometry, floating, area, visible
    
    def save_window_state(self, main_window):
        """保存主窗口状态"""
        self.settings.setValue("window/geometry", main_window.saveGeometry())
        self.settings.setValue("window/state", main_window.saveState())
    
    def load_window_state(self, main_window):
        """加载主窗口状态"""
        geometry = self.settings.value("window/geometry")
        state = self.settings.value("window/state")
        if geometry:
            main_window.restoreGeometry(geometry)
        if state:
            main_window.restoreState(state)
