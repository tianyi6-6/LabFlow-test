#!/usr/bin/env python3
"""LabFlow 自定义节点"""

from .base_node import BaseNode
from labflow.utils.data_structures import DataPacket


class CustomNode(BaseNode):
    """自定义节点类"""
    
    def __init__(self, node_id=None, name="CustomNode"):
        super().__init__(node_id, name)
        self.node_type = "custom"
        self.add_input("data_in")
        self.add_output("data_out")
        # 默认参数
        self.properties = {
            "script_path": "",  # 自定义脚本路径
            "function_name": "execute",  # 执行函数名称
            "parameters": {}
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取数据
        data = data_packet.get_data()
        
        # 执行自定义逻辑
        script_path = self.properties['script_path']
        function_name = self.properties['function_name']
        parameters = self.properties['parameters']
        
        print(f"执行自定义节点: {self.name}")
        print(f"脚本路径: {script_path}")
        print(f"函数名称: {function_name}")
        print(f"参数: {parameters}")
        
        # 这里是模拟实现，实际应该加载并执行自定义脚本
        # 例如：
        # import importlib.util
        # spec = importlib.util.spec_from_file_location("custom_module", script_path)
        # custom_module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(custom_module)
        # execute_func = getattr(custom_module, function_name)
        # result = execute_func(data, **parameters)
        # data_packet.set_data(result)
        
        # 模拟执行结果
        print("执行自定义逻辑...")
        print(f"输入数据长度: {len(data) if data.size > 0 else 0}")
        
        self.set_status("success")
        return data_packet
    
    def set_script_path(self, script_path: str) -> None:
        """设置脚本路径"""
        self.properties['script_path'] = script_path
    
    def set_function_name(self, function_name: str) -> None:
        """设置函数名称"""
        self.properties['function_name'] = function_name
    
    def set_parameters(self, parameters: dict) -> None:
        """设置参数"""
        self.properties['parameters'] = parameters
    
    def add_parameter(self, key: str, value: any) -> None:
        """添加参数"""
        self.properties['parameters'][key] = value