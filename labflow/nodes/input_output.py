#!/usr/bin/env python3
"""LabFlow 输入输出节点"""

from .base_node import BaseNode
from utils.data_structures import DataPacket
import numpy as np


class InputNode(BaseNode):
    """输入节点"""
    
    def __init__(self, node_id: str, name: str):
        """初始化输入节点"""
        super().__init__(node_id, name, outputs=["output"])
        self.properties["value"] = 0.0
        self.properties["data_type"] = "float"
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行输入节点逻辑"""
        # 获取输入值
        value = self.properties["value"]
        data_type = self.properties["data_type"]
        
        # 转换数据类型
        if data_type == "float":
            value = float(value)
        elif data_type == "int":
            value = int(value)
        elif data_type == "bool":
            value = bool(value)
        
        # 创建输出数据
        output_data = np.array([value])
        output_packet = DataPacket(data=output_data)
        output_packet.add_metadata("node_id", self.node_id)
        output_packet.add_metadata("node_name", self.name)
        
        return output_packet


class OutputNode(BaseNode):
    """输出节点"""
    
    def __init__(self, node_id: str, name: str):
        """初始化输出节点"""
        super().__init__(node_id, name, inputs=["input"])
        self.properties["output_file"] = "output.txt"
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行输出节点逻辑"""
        # 获取输入数据
        input_data = data_packet.get_data()
        
        # 保存到文件
        output_file = self.properties["output_file"]
        try:
            np.savetxt(output_file, input_data)
            print(f"数据已保存到: {output_file}")
        except Exception as e:
            print(f"保存数据失败: {e}")
        
        # 返回原始数据包
        return data_packet