#!/usr/bin/env python3
"""LabFlow USB 设备类"""

import asyncio
from typing import Dict, Any, Optional
from ....labflow.devices.base_device import BaseDevice


class USBDevice(BaseDevice):
    """USB 设备类"""

    def __init__(self, device_id: Optional[str] = None, name: str = "USBDevice"):
        super().__init__(device_id, name)
        self.device_type = "usb"
        self.connection_info = {
            "type": "usb",
            "vendor_id": 0,
            "product_id": 0,
            "serial_number": "",
            "timeout": 5.0
        }
        self.properties = {
            "model": "USB Device",
            "firmware_version": "1.0.0",
            "max_transfer_size": 4096
        }
        self._usb_handle = None

    async def connect(self) -> bool:
        """连接设备"""
        print(f"连接 USB 设备: {self.name}")
        print(f"厂商 ID: {self.connection_info['vendor_id']}")
        print(f"产品 ID: {self.connection_info['product_id']}")
        await asyncio.sleep(0.5)
        self.connected = True
        self.status = "online"
        print(f"USB 设备 {self.name} 连接成功")
        return True

    async def disconnect(self) -> bool:
        """断开设备"""
        print(f"断开 USB 设备: {self.name}")
        await asyncio.sleep(0.2)
        self.connected = False
        self.status = "offline"
        print(f"USB 设备 {self.name} 断开成功")
        return True

    async def read(self, **kwargs) -> Any:
        """读取设备数据"""
        if not self.connected:
            raise Exception("设备未连接")
        await asyncio.sleep(0.1)
        data = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05]
        print(f"从 USB 设备 {self.name} 读取数据: {data}")
        return data

    async def write(self, data: Any, **kwargs) -> bool:
        """写入设备数据"""
        if not self.connected:
            raise Exception("设备未连接")
        await asyncio.sleep(0.1)
        print(f"向 USB 设备 {self.name} 写入数据: {data}")
        return True

    async def execute_command(self, command: str, **kwargs) -> Any:
        """执行设备命令"""
        if not self.connected:
            raise Exception("设备未连接")
        await asyncio.sleep(0.1)
        print(f"在 USB 设备 {self.name} 上执行命令: {command}")
        if command.lower().startswith("*idn"):
            return f"{self.properties['model']}, {self.properties['firmware_version']}"
        else:
            return f"Command executed: {command}"

    def set_vendor_id(self, vendor_id: int) -> None:
        """设置厂商 ID"""
        self.connection_info['vendor_id'] = vendor_id

    def set_product_id(self, product_id: int) -> None:
        """设置产品 ID"""
        self.connection_info['product_id'] = product_id

    def set_serial_number(self, serial_number: str) -> None:
        """设置序列号"""
        self.connection_info['serial_number'] = serial_number
