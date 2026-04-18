#!/usr/bin/env python3
"""LabFlow 信号处理节点"""

import numpy as np
from .base_node import BaseNode
from labflow.utils.data_structures import DataPacket


class lockin_res(BaseNode):
    """锁相放大器信号处理节点"""
    
    def __init__(self, node_id=None, name="lockin_res"):
        super().__init__(node_id, name)
        self.node_type = "signal_processing"
        self.add_input("data_in")
        self.add_output("data_out")
        # 默认参数
        self.properties = {
            "reference_frequency": 1000,  # 参考频率，单位 Hz
            "phase": 0.0  # 相位角，单位度
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取数据
        data = data_packet.get_data()
        
        # 执行锁相放大处理
        if len(data) > 0:
            # 这里是模拟实现，实际应该使用锁相放大算法
            # 生成参考信号
            t = np.arange(len(data)) / data_packet.get_metadata_value("sample_rate", 1000)
            reference = np.sin(2 * np.pi * self.properties['reference_frequency'] * t + np.deg2rad(self.properties['phase']))
            # 计算互相关
            result = np.correlate(data, reference, mode='same')
            # 更新数据
            data_packet.set_data(result)
            print(f"锁相放大处理完成，结果长度: {len(result)}")
        
        self.set_status("success")
        return data_packet


class log_insert_compile(BaseNode):
    """日志插入编译节点"""
    
    def __init__(self, node_id=None, name="log_insert_compile"):
        super().__init__(node_id, name)
        self.node_type = "signal_processing"
        self.add_input("data_in")
        self.add_output("data_out")
        # 默认参数
        self.properties = {
            "log_message": "Processing data",
            "compile_enabled": True
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取数据
        data = data_packet.get_data()
        
        # 插入日志
        print(f"[LOG] {self.properties['log_message']}")
        
        # 执行编译处理（模拟）
        if self.properties['compile_enabled']:
            print("[COMPILE] Compiling data...")
            # 这里是模拟实现，实际应该执行编译逻辑
            if len(data) > 0:
                # 简单的编译处理：计算数据的统计信息
                stats = {
                    "mean": np.mean(data),
                    "std": np.std(data),
                    "min": np.min(data),
                    "max": np.max(data)
                }
                data_packet.add_metadata("data_stats", stats)
                print(f"[COMPILE] Data stats: {stats}")
        
        self.set_status("success")
        return data_packet