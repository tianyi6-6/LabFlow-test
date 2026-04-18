#!/usr/bin/env python3
"""LabFlow 设备控制节点"""

from .base_node import BaseNode
from labflow.utils.data_structures import DataPacket


class SetLockInFreq(BaseNode):
    """锁相放大器频率设置节点"""
    
    def __init__(self, node_id=None, name="SetLockInFreq"):
        super().__init__(node_id, name)
        self.node_type = "device_control"
        self.add_input("device_in")
        self.add_output("device_out")
        # 默认参数
        self.properties = {
            "time_constant": "100ms",
            "sensitivity": "24dB",
            "reference_frequency": "1000Hz",
            "filter_enabled": True
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取设备
        device = data_packet.get_metadata_value("device")
        
        # 执行频率设置
        if device:
            # 这里是模拟实现，实际应该调用设备的方法
            print(f"设置锁相放大器频率: {self.properties['reference_frequency']}")
            print(f"时间常数: {self.properties['time_constant']}")
            print(f"灵敏度: {self.properties['sensitivity']}")
            print(f"滤波开关: {self.properties['filter_enabled']}")
        
        self.set_status("success")
        return data_packet


class SetLockInPhase(BaseNode):
    """锁相放大器相位设置节点"""
    
    def __init__(self, node_id=None, name="SetLockInPhase"):
        super().__init__(node_id, name)
        self.node_type = "device_control"
        self.add_input("device_in")
        self.add_output("device_out")
        # 默认参数
        self.properties = {
            "phase": 0.0  # 相位角，单位度
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取设备
        device = data_packet.get_metadata_value("device")
        
        # 执行相位设置
        if device:
            # 这里是模拟实现，实际应该调用设备的方法
            print(f"设置锁相放大器相位: {self.properties['phase']}度")
        
        self.set_status("success")
        return data_packet


class SetLockInTimeCo(BaseNode):
    """锁相放大器时间常数设置节点"""
    
    def __init__(self, node_id=None, name="SetLockInTimeCo"):
        super().__init__(node_id, name)
        self.node_type = "device_control"
        self.add_input("device_in")
        self.add_output("device_out")
        # 默认参数
        self.properties = {
            "time_constant": "100ms"  # 时间常数
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取设备
        device = data_packet.get_metadata_value("device")
        
        # 执行时间常数设置
        if device:
            # 这里是模拟实现，实际应该调用设备的方法
            print(f"设置锁相放大器时间常数: {self.properties['time_constant']}")
        
        self.set_status("success")
        return data_packet


class USB_START(BaseNode):
    """USB 设备启动节点"""
    
    def __init__(self, node_id=None, name="USB_START"):
        super().__init__(node_id, name)
        self.node_type = "device_control"
        self.add_input("device_in")
        self.add_output("device_out")
        # 默认参数
        self.properties = {
            "device_id": "usb_device_001"
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取设备
        device = data_packet.get_metadata_value("device")
        
        # 执行设备启动
        if device:
            # 这里是模拟实现，实际应该调用设备的方法
            print(f"启动 USB 设备: {self.properties['device_id']}")
        
        self.set_status("success")
        return data_packet


class USB_END(BaseNode):
    """USB 设备结束节点"""
    
    def __init__(self, node_id=None, name="USB_END"):
        super().__init__(node_id, name)
        self.node_type = "device_control"
        self.add_input("device_in")
        self.add_output("device_out")
        # 默认参数
        self.properties = {
            "device_id": "usb_device_001"
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取设备
        device = data_packet.get_metadata_value("device")
        
        # 执行设备结束
        if device:
            # 这里是模拟实现，实际应该调用设备的方法
            print(f"结束 USB 设备: {self.properties['device_id']}")
        
        self.set_status("success")
        return data_packet