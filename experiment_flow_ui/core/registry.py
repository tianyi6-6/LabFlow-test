"""Registry for nodes and devices"""

import os
import importlib
import inspect
from typing import Dict, List, Type
from experiment_flow_ui.nodes.base_node import BaseNode
from experiment_flow_ui.core.base_device import BaseDevice


class Registry:
    """节点和设备注册表"""
    
    def __init__(self):
        self.node_registry: Dict[str, Type[BaseNode]] = {}
        self.device_registry: Dict[str, Type[BaseDevice]] = {}
        self.node_categories: Dict[str, List[str]] = {}
    
    def register_node(self, node_class: Type[BaseNode]):
        """注册节点类"""
        if issubclass(node_class, BaseNode):
            node_name = node_class.__name__
            self.node_registry[node_name] = node_class
            
            # 确定节点类别
            module_name = node_class.__module__
            category = module_name.split('.')[-1] if '.' in module_name else 'general'
            if category not in self.node_categories:
                self.node_categories[category] = []
            if node_name not in self.node_categories[category]:
                self.node_categories[category].append(node_name)
            
            print(f"节点 {node_name} 注册成功，类别: {category}")
    
    def register_device(self, device_class: Type[BaseDevice]):
        """注册设备类"""
        if issubclass(device_class, BaseDevice):
            device_name = device_class.__name__
            self.device_registry[device_name] = device_class
            print(f"设备 {device_name} 注册成功")
    
    def get_node(self, node_name: str) -> Type[BaseNode]:
        """获取节点类"""
        return self.node_registry.get(node_name)
    
    def get_device(self, device_name: str) -> Type[BaseDevice]:
        """获取设备类"""
        return self.device_registry.get(device_name)
    
    def get_all_nodes(self) -> Dict[str, Type[BaseNode]]:
        """获取所有节点类"""
        return self.node_registry
    
    def get_all_devices(self) -> Dict[str, Type[BaseDevice]]:
        """获取所有设备类"""
        return self.device_registry
    
    def get_node_categories(self) -> Dict[str, List[str]]:
        """获取节点类别"""
        return self.node_categories
    
    def scan_nodes_directory(self, nodes_dir: str):
        """扫描 nodes 目录，自动注册节点"""
        if not os.path.exists(nodes_dir):
            print(f"节点目录 {nodes_dir} 不存在")
            return
        
        # 遍历 nodes 目录
        for root, dirs, files in os.walk(nodes_dir):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    # 计算模块路径
                    relative_path = os.path.relpath(root, os.path.dirname(nodes_dir))
                    module_path = f"experiment_flow_ui.nodes.{relative_path.replace(os.path.sep, '.')}.{file[:-3]}"
                    
                    try:
                        # 导入模块
                        module = importlib.import_module(module_path)
                        
                        # 扫描模块中的类
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if issubclass(obj, BaseNode) and obj != BaseNode:
                                self.register_node(obj)
                    except Exception as e:
                        print(f"导入模块 {module_path} 失败: {e}")
    
    def scan_devices_directory(self, devices_dir: str):
        """扫描 devices 目录，自动注册设备"""
        if not os.path.exists(devices_dir):
            print(f"设备目录 {devices_dir} 不存在")
            return
        
        # 遍历 devices 目录
        for root, dirs, files in os.walk(devices_dir):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    # 计算模块路径
                    relative_path = os.path.relpath(root, os.path.dirname(devices_dir))
                    module_path = f"experiment_flow_ui.devices.{relative_path.replace(os.path.sep, '.')}.{file[:-3]}"
                    
                    try:
                        # 导入模块
                        module = importlib.import_module(module_path)
                        
                        # 扫描模块中的类
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if issubclass(obj, BaseDevice) and obj != BaseDevice:
                                self.register_device(obj)
                    except Exception as e:
                        print(f"导入模块 {module_path} 失败: {e}")


# 全局注册表实例
registry = Registry()