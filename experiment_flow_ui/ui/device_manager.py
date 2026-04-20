#!/usr/bin/env python3
"""LabFlow 设备管理器"""

import asyncio
from typing import Dict, List, Optional
from labflow.devices.base_device import BaseDevice
from labflow.devices.simulated.simulated_device import SimulatedDevice
from labflow.devices.usb.usb_device import USBDevice
from labflow.devices.serial.serial_device import SerialDevice
from labflow.devices.network.network_device import NetworkDevice
from labflow.utils.data_structures import DeviceInfo


class DeviceManager:
    """设备管理器类"""
    
    def __init__(self):
        self.devices: Dict[str, BaseDevice] = {}
        self._lock = asyncio.Lock()
    
    async def add_device(self, device: BaseDevice) -> bool:
        """添加设备"""
        async with self._lock:
            if device.device_id in self.devices:
                print(f"设备 {device.device_id} 已存在")
                return False
            self.devices[device.device_id] = device
            print(f"设备 {device.name} (ID: {device.device_id}) 添加成功")
            return True
    
    async def remove_device(self, device_id: str) -> bool:
        """移除设备"""
        async with self._lock:
            if device_id not in self.devices:
                print(f"设备 {device_id} 不存在")
                return False
            device = self.devices[device_id]
            if device.is_connected():
                await device.disconnect()
            del self.devices[device_id]
            print(f"设备 {device.name} (ID: {device_id}) 移除成功")
            return True
    
    async def connect_device(self, device_id: str) -> bool:
        """连接设备"""
        async with self._lock:
            if device_id not in self.devices:
                print(f"设备 {device_id} 不存在")
                return False
            device = self.devices[device_id]
            if device.is_connected():
                print(f"设备 {device.name} 已经连接")
                return True
            try:
                result = await device.connect()
                if result:
                    print(f"设备 {device.name} 连接成功")
                else:
                    print(f"设备 {device.name} 连接失败")
                return result
            except Exception as e:
                print(f"设备 {device.name} 连接失败: {e}")
                device.set_status("error")
                return False
    
    async def disconnect_device(self, device_id: str) -> bool:
        """断开设备"""
        async with self._lock:
            if device_id not in self.devices:
                print(f"设备 {device_id} 不存在")
                return False
            device = self.devices[device_id]
            if not device.is_connected():
                print(f"设备 {device.name} 已经断开")
                return True
            try:
                result = await device.disconnect()
                if result:
                    print(f"设备 {device.name} 断开成功")
                else:
                    print(f"设备 {device.name} 断开失败")
                return result
            except Exception as e:
                print(f"设备 {device.name} 断开失败: {e}")
                return False
    
    async def connect_all_devices(self) -> Dict[str, bool]:
        """连接所有设备"""
        results = {}
        for device_id in self.devices:
            results[device_id] = await self.connect_device(device_id)
        return results
    
    async def disconnect_all_devices(self) -> Dict[str, bool]:
        """断开所有设备"""
        results = {}
        for device_id in self.devices:
            results[device_id] = await self.disconnect_device(device_id)
        return results
    
    def get_device(self, device_id: str) -> Optional[BaseDevice]:
        """获取设备"""
        return self.devices.get(device_id)
    
    def get_all_devices(self) -> List[BaseDevice]:
        """获取所有设备"""
        return list(self.devices.values())
    
    def get_device_info(self, device_id: str) -> Optional[DeviceInfo]:
        """获取设备信息"""
        device = self.get_device(device_id)
        if device:
            return device.to_device_info()
        return None
    
    def get_all_device_info(self) -> List[DeviceInfo]:
        """获取所有设备信息"""
        return [device.to_device_info() for device in self.devices.values()]
    
    def get_connected_devices(self) -> List[BaseDevice]:
        """获取已连接的设备"""
        return [device for device in self.devices.values() if device.is_connected()]
    
    def get_device_status(self, device_id: str) -> Optional[str]:
        """获取设备状态"""
        device = self.get_device(device_id)
        if device:
            return device.get_status()
        return None
    
    async def execute_command(self, device_id: str, command: str, **kwargs) -> Any:
        """执行设备命令"""
        device = self.get_device(device_id)
        if not device:
            print(f"设备 {device_id} 不存在")
            return None
        if not device.is_connected():
            print(f"设备 {device.name} 未连接")
            return None
        try:
            result = await device.execute_command(command, **kwargs)
            return result
        except Exception as e:
            print(f"执行命令失败: {e}")
            device.set_status("error")
            return None
    
    async def create_device(self, device_type: str, device_id: Optional[str] = None, name: str = "", **kwargs) -> Optional[BaseDevice]:
        """创建设备"""
        device = None
        if device_type == "simulated":
            device = SimulatedDevice(device_id, name or "SimulatedDevice")
        elif device_type == "usb":
            device = USBDevice(device_id, name or "USBDevice")
            # 设置 USB 设备参数
            if "vendor_id" in kwargs:
                device.set_vendor_id(kwargs["vendor_id"])
            if "product_id" in kwargs:
                device.set_product_id(kwargs["product_id"])
            if "serial_number" in kwargs:
                device.set_serial_number(kwargs["serial_number"])
        elif device_type == "serial":
            device = SerialDevice(device_id, name or "SerialDevice")
            # 设置串口设备参数
            if "port" in kwargs:
                device.set_port(kwargs["port"])
            if "baudrate" in kwargs:
                device.set_baudrate(kwargs["baudrate"])
            if "bytesize" in kwargs:
                device.set_bytesize(kwargs["bytesize"])
            if "parity" in kwargs:
                device.set_parity(kwargs["parity"])
            if "stopbits" in kwargs:
                device.set_stopbits(kwargs["stopbits"])
        elif device_type == "network":
            device = NetworkDevice(device_id, name or "NetworkDevice")
            # 设置网络设备参数
            if "host" in kwargs:
                device.set_host(kwargs["host"])
            if "port" in kwargs:
                device.set_port(kwargs["port"])
            if "protocol" in kwargs:
                device.set_protocol(kwargs["protocol"])
        else:
            print(f"不支持的设备类型: {device_type}")
            return None
        
        # 添加设备
        await self.add_device(device)
        return device
    
    def get_device_count(self) -> int:
        """获取设备数量"""
        return len(self.devices)
    
    def get_connected_device_count(self) -> int:
        """获取已连接设备数量"""
        return len(self.get_connected_devices())