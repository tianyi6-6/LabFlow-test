#!/usr/bin/env python3
"""LabFlow 数据采集节点"""

import numpy as np
from .base_node import BaseNode
from labflow.utils.data_structures import DataPacket


class SetDataSampleRate(BaseNode):
    """设置数据采样率节点"""
    
    def __init__(self, node_id=None, name="SetDataSampleRate"):
        super().__init__(node_id, name)
        self.node_type = "data_acquisition"
        self.add_input("device_in")
        self.add_output("data_out")
        # 默认参数
        self.properties = {
            "sample_rate": 1000  # 采样率，单位 Hz
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取设备
        device = data_packet.get_metadata_value("device")
        
        # 执行采样率设置
        if device:
            # 这里是模拟实现，实际应该调用设备的方法
            print(f"设置数据采样率: {self.properties['sample_rate']} Hz")
        
        # 将采样率添加到元数据
        data_packet.add_metadata("sample_rate", self.properties['sample_rate'])
        
        self.set_status("success")
        return data_packet


class get_max_slope(BaseNode):
    """获取最大斜率节点"""
    
    def __init__(self, node_id=None, name="get_max_slope"):
        super().__init__(node_id, name)
        self.node_type = "data_acquisition"
        self.add_input("data_in")
        self.add_output("data_out")
        # 默认参数
        self.properties = {
            "window_size": 10  # 计算斜率的窗口大小
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取数据
        data = data_packet.get_data()
        
        # 计算最大斜率
        if len(data) > 1:
            # 计算相邻点之间的斜率
            slopes = np.diff(data)
            # 计算窗口平均斜率
            window_size = min(self.properties['window_size'], len(slopes))
            if window_size > 0:
                windowed_slopes = np.convolve(slopes, np.ones(window_size)/window_size, mode='valid')
                max_slope = np.max(np.abs(windowed_slopes))
                print(f"最大斜率: {max_slope}")
                # 将最大斜率添加到元数据
                data_packet.add_metadata("max_slope", max_slope)
        
        self.set_status("success")
        return data_packet