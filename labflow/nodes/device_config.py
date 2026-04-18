#!/usr/bin/env python3
"""LabFlow 设备配置节点"""

from .base_node import BaseNode
from utils.data_structures import DataPacket


class DeviceConfigNode(BaseNode):
    """设备配置节点"""
    
    def __init__(self, node_id: str, name: str):
        """初始化设备配置节点"""
        super().__init__(node_id, name, outputs=["device_info"])
        self.properties["device_type"] = "simulated"
        self.properties["device_name"] = "Simulated Device"
        self.properties["connection_info"] = {}
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行设备配置节点逻辑"""
        # 创建设备信息
        device_info = {
            "device_id": self.node_id,
            "device_type": self.properties["device_type"],
            "device_name": self.properties["device_name"],
            "connection_info": self.properties["connection_info"]
        }
        
        # 创建输出数据包
        output_packet = DataPacket()
        output_packet.add_metadata("device_info", device_info)
        output_packet.add_metadata("node_id", self.node_id)
        output_packet.add_metadata("node_name", self.name)
        
        return output_packet