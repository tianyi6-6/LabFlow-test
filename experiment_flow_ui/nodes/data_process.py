#!/usr/bin/env python3
"""LabFlow 数据处理节点"""

from .base_node import BaseNode
from utils.data_structures import DataPacket
import numpy as np


class DataProcessNode(BaseNode):
    """数据处理节点"""
    
    def __init__(self, node_id: str, name: str):
        """初始化数据处理节点"""
        super().__init__(node_id, name, inputs=["input"], outputs=["output"])
        self.properties["process_type"] = "filter"
        self.properties["filter_type"] = "lowpass"
        self.properties["cutoff_frequency"] = 10
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行数据处理节点逻辑"""
        # 获取输入数据
        input_data = data_packet.get_data()
        
        # 执行数据处理
        process_type = self.properties["process_type"]
        output_data = input_data.copy()
        
        if process_type == "filter":
            # 简单的低通滤波
            cutoff = self.properties["cutoff_frequency"]
            # 这里使用简单的移动平均作为低通滤波
            window_size = 10
            output_data = np.convolve(input_data, np.ones(window_size)/window_size, mode='same')
        elif process_type == "normalize":
            # 归一化处理
            output_data = (input_data - np.min(input_data)) / (np.max(input_data) - np.min(input_data))
        elif process_type == "amplify":
            # 放大处理
            output_data = input_data * 2
        
        # 创建输出数据包
        output_packet = DataPacket(data=output_data)
        output_packet.add_metadata("node_id", self.node_id)
        output_packet.add_metadata("node_name", self.name)
        output_packet.add_metadata("process_type", process_type)
        
        return output_packet