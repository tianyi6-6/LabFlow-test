#!/usr/bin/env python3
"""LabFlow 流程控制节点"""

import numpy as np
from .base_node import BaseNode
from labflow.utils.data_structures import DataPacket


class LoopRepeat(BaseNode):
    """循环重复遍历节点"""
    
    def __init__(self, node_id=None, name="LoopRepeat"):
        super().__init__(node_id, name)
        self.node_type = "control_flow"
        self.add_input("data_in")
        self.add_output("data_out")
        # 默认参数
        self.properties = {
            "repeat_count": 10,  # 重复次数
            "step_size": 1.0  # 步长
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取数据
        data = data_packet.get_data()
        
        # 执行循环重复
        repeat_count = self.properties['repeat_count']
        step_size = self.properties['step_size']
        
        print(f"开始循环，重复次数: {repeat_count}, 步长: {step_size}")
        
        # 这里是模拟实现，实际应该执行循环逻辑
        # 生成循环数据
        loop_data = []
        for i in range(repeat_count):
            value = i * step_size
            loop_data.append(value)
            print(f"循环第 {i+1} 次: {value}")
        
        # 更新数据
        data_packet.set_data(np.array(loop_data))
        data_packet.add_metadata("loop_count", repeat_count)
        data_packet.add_metadata("loop_step", step_size)
        
        self.set_status("success")
        return data_packet


class add_row_data(BaseNode):
    """添加行数据节点"""
    
    def __init__(self, node_id=None, name="add_row_data"):
        super().__init__(node_id, name)
        self.node_type = "control_flow"
        self.add_input("data_in")
        self.add_output("data_out")
        # 默认参数
        self.properties = {
            "row_data": [0.0, 0.0, 0.0],  # 要添加的行数据
            "append_mode": True  # 是否追加模式
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取数据
        data = data_packet.get_data()
        
        # 执行添加行数据
        row_data = np.array(self.properties['row_data'])
        
        if self.properties['append_mode']:
            # 追加模式
            if len(data) == 0:
                # 如果数据为空，直接设置为行数据
                data_packet.set_data(row_data)
            else:
                # 否则，追加行数据
                if data.ndim == 1:
                    # 如果是一维数组，转换为二维数组
                    data = data.reshape(-1, 1)
                # 确保行数据维度匹配
                if row_data.ndim == 1:
                    row_data = row_data.reshape(1, -1)
                # 追加数据
                new_data = np.vstack([data, row_data])
                data_packet.set_data(new_data)
        else:
            # 替换模式
            data_packet.set_data(row_data)
        
        print(f"添加行数据: {row_data}")
        print(f"新数据形状: {data_packet.get_data().shape}")
        
        self.set_status("success")
        return data_packet