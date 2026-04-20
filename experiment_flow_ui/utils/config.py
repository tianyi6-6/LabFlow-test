#!/usr/bin/env python3
"""LabFlow 配置管理"""

import yaml
from typing import Dict, Any, Optional
import os


class Config:
    """配置管理类"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or os.path.join(os.path.dirname(__file__), "..", "config.yaml")
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f) or {}
        else:
            # 初始化默认配置
            self.config = {
                "ui": {
                    "default_window_size": [1600, 900],
                    "canvas_background": "#f0f0f0",
                    "node_colors": {
                        "device_control": "#FFB347",  # 浅橙色
                        "data_acquisition": "#808080",  # 灰色
                        "signal_processing": "#808080",  # 灰色
                        "control_flow": "#808080",  # 灰色
                        "visualization": "#D2B48C",  # 浅棕色
                        "custom": "#808080"  # 灰色
                    },
                    "port_colors": {
                        "device": "#4169E1",  # 蓝色
                        "data": "#FFD700"  # 黄色
                    }
                },
                "execution": {
                    "max_concurrent_nodes": 10,
                    "node_timeout": 30,  # 秒
                    "default_polling_interval": 0.1  # 秒
                },
                "devices": {
                    "default_timeout": 5,  # 秒
                    "max_retry_count": 3
                },
                "logging": {
                    "level": "INFO",
                    "log_file": "labflow.log",
                    "max_log_size": 10485760  # 10MB
                }
            }
            self.save_config()
    
    def save_config(self) -> None:
        """保存配置文件"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
    
    def get_node_color(self, node_type: str) -> str:
        """获取节点颜色"""
        return self.get(f"ui.node_colors.{node_type}", "#808080")
    
    def get_port_color(self, port_type: str) -> str:
        """获取端口颜色"""
        return self.get(f"ui.port_colors.{port_type}", "#808080")