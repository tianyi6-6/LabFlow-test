#!/usr/bin/env python3
"""LabFlow 仿真微波设备类"""

import asyncio
import random
from typing import Dict, Any, Optional
from ....labflow.devices.base_device import BaseDevice


class MicrowaveSimulator(BaseDevice):
    """仿真微波设备类"""

    def __init__(self, device_id: Optional[str] = None, name: str = "MicrowaveSimulator"):
        super().__init__(device_id, name)
        self.device_type = "microwave"
        self.connection_info = {
            "type": "simulated",
            "timeout": 5.0
        }
        self.properties = {
            "model": "Simulated Microwave Device",
            "firmware_version": "1.0.0",
            "max_sample_rate": 10000,
            "frequency": 10.0e9,
            "power": -20.0
        }
        self.simulated_data = []
        self.command_history = []

    async def connect(self) -> bool:
        """连接设备"""
        print(f"连接仿真微波设备: {self.name}")
        await asyncio.sleep(0.5)
        self.connected = True
        self.status = "online"
        print(f"仿真微波设备 {self.name} 连接成功")
        return True

    async def disconnect(self) -> bool:
        """断开设备"""
        print(f"断开仿真微波设备: {self.name}")
        await asyncio.sleep(0.2)
        self.connected = False
        self.status = "offline"
        print(f"仿真微波设备 {self.name} 断开成功")
        return True

    async def read(self, **kwargs) -> Any:
        """读取设备数据"""
        if not self.connected:
            raise Exception("设备未连接")

        await asyncio.sleep(0.1)

        sample_count = kwargs.get("sample_count", 100)
        sample_rate = kwargs.get("sample_rate", 1000)

        import numpy as np
        t = np.arange(sample_count) / sample_rate
        frequency = kwargs.get("frequency", self.properties.get("frequency", 10.0e9))
        amplitude = kwargs.get("amplitude", self.properties.get("power", -20.0))
        noise = kwargs.get("noise", 0.1)

        data = amplitude * np.sin(2 * np.pi * frequency * t) + noise * np.random.randn(sample_count)
        self.simulated_data = data.tolist()

        print(f"从仿真微波设备 {self.name} 读取数据，长度: {len(self.simulated_data)}")
        return self.simulated_data

    async def write(self, data: Any, **kwargs) -> bool:
        """写入设备数据"""
        if not self.connected:
            raise Exception("设备未连接")

        await asyncio.sleep(0.1)

        print(f"向仿真微波设备 {self.name} 写入数据: {data}")
        return True

    async def execute_command(self, command: str, **kwargs) -> Any:
        """执行设备命令"""
        if not self.connected:
            raise Exception("设备未连接")

        await asyncio.sleep(0.1)

        self.command_history.append(command)
        print(f"在仿真微波设备 {self.name} 上执行命令: {command}")

        if command.lower().startswith("*idn"):
            return f"{self.properties['model']}, {self.properties['firmware_version']}"
        elif command.lower().startswith("get"):
            param = command.split()[1] if len(command.split()) > 1 else ""
            if param in self.properties:
                return self.properties[param]
            else:
                return f"Unknown parameter: {param}"
        elif command.lower().startswith("set"):
            parts = command.split()
            if len(parts) >= 3:
                param = parts[1]
                value = " ".join(parts[2:])
                self.properties[param] = value
                return f"Set {param} to {value}"
            else:
                return "Invalid set command"
        else:
            return f"Command executed: {command}"

    def get_command_history(self) -> list:
        """获取命令历史"""
        return self.command_history

    def clear_command_history(self) -> None:
        """清空命令历史"""
        self.command_history = []

    def get_simulated_data(self) -> list:
        """获取模拟数据"""
        return self.simulated_data
