#!/usr/bin/env python3
"""LabFlow 串口设备类"""

import asyncio
from typing import Dict, Any, Optional
from ....labflow.devices.base_device import BaseDevice


class SerialDevice(BaseDevice):
    """串口设备类"""

    def __init__(self, device_id: Optional[str] = None, name: str = "SerialDevice"):
        super().__init__(device_id, name)
        self.device_type = "serial"
        self.connection_info = {
            "type": "serial",
            "port": "COM1",
            "baudrate": 9600,
            "bytesize": 8,
            "parity": "N",
            "stopbits": 1,
            "timeout": 5.0
        }
        self.properties = {
            "model": "Serial Device",
            "firmware_version": "1.0.0"
        }
        self._serial_port = None

    async def connect(self) -> bool:
        """连接设备"""
        print(f"连接串口设备: {self.name}")
        print(f"端口: {self.connection_info['port']}")
        print(f"波特率: {self.connection_info['baudrate']}")
        await asyncio.sleep(0.5)
        self.connected = True
        self.status = "online"
        print(f"串口设备 {self.name} 连接成功")
        return True

    async def disconnect(self) -> bool:
        """断开设备"""
        print(f"断开串口设备: {self.name}")
        await asyncio.sleep(0.2)
        self.connected = False
        self.status = "offline"
        print(f"串口设备 {self.name} 断开成功")
        return True

    async def read(self, **kwargs) -> Any:
        """读取设备数据"""
        if not self.connected:
            raise Exception("设备未连接")
        await asyncio.sleep(0.1)
        data = b"Hello from serial device"
        print(f"从串口设备 {self.name} 读取数据: {data}")
        return data

    async def write(self, data: Any, **kwargs) -> bool:
        """写入设备数据"""
        if not self.connected:
            raise Exception("设备未连接")
        await asyncio.sleep(0.1)
        print(f"向串口设备 {self.name} 写入数据: {data}")
        return True

    async def execute_command(self, command: str, **kwargs) -> Any:
        """执行设备命令"""
        if not self.connected:
            raise Exception("设备未连接")
        await asyncio.sleep(0.1)
        print(f"在串口设备 {self.name} 上执行命令: {command}")
        if command.lower().startswith("*idn"):
            return f"{self.properties['model']}, {self.properties['firmware_version']}"
        else:
            return f"Command executed: {command}"

    def set_port(self, port: str) -> None:
        """设置端口名称"""
        self.connection_info['port'] = port

    def set_baudrate(self, baudrate: int) -> None:
        """设置波特率"""
        self.connection_info['baudrate'] = baudrate
