#!/usr/bin/env python3
"""LabFlow 数据读取节点"""

from .base_node import BaseNode
from utils.data_structures import DataPacket
import numpy as np


class DataReadNode(BaseNode):
    """数据读取节点"""
    
    def __init__(self, node_id: str, name: str):
        """初始化数据读取节点"""
        super().__init__(node_id, name, inputs=["device_info"], outputs=["data"])
        self.properties["sample_count"] = 100
        self.properties["sample_rate"] = 1000
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行数据读取节点逻辑"""
        # 获取设备信息
        device_info = data_packet.get_metadata_value("device_info")
        
        # 模拟数据读取
        sample_count = self.properties["sample_count"]
        sample_rate = self.properties["sample_rate"]
        
        # 生成模拟数据
        time_array = np.linspace(0, sample_count / sample_rate, sample_count)
        data = np.sin(2 * np.pi * 5 * time_array) + np.random.normal(0, 0.1, sample_count)
        
        # 创建输出数据包
        output_packet = DataPacket(data=data)
        output_packet.add_metadata("node_id", self.node_id)
        output_packet.add_metadata("node_name", self.name)
        output_packet.add_metadata("sample_count", sample_count)
        output_packet.add_metadata("sample_rate", sample_rate)
        
        return output_packet