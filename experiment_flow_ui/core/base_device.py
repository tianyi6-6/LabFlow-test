#!/usr/bin/env python3
"""LabFlow 基础设备类"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
from experiment_flow_ui.utils.data_structures import DeviceInfo
from experiment_flow_ui.utils.helpers import generate_id


class BaseDevice(ABC):
    """基础设备类"""
    
    def __init__(self, device_id: Optional[str] = None, name: str = "BaseDevice"):
        self.device_id = device_id or generate_id("device_")
        self.name = name
        self.connected = False
        self.status = "offline"  # offline, online, warning, error
        self.lock = asyncio.Lock()
        self.device_type = "base"
        self.connection_info: Dict[str, Any] = {}
        self.properties: Dict[str, Any] = {}
    
    @abstractmethod
    async def connect(self) -> bool:
        """连接设备"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """断开设备"""
        pass
    
    @abstractmethod
    async def read(self, **kwargs) -> Any:
        """读取设备数据"""
        pass
    
    @abstractmethod
    async def write(self, data: Any, **kwargs) -> bool:
        """写入设备数据"""
        pass
    
    async def execute_command(self, command: str, **kwargs) -> Any:
        """执行设备命令"""
        raise NotImplementedError("Subclasses must implement execute_command")
    
    def get_state(self) -> Dict[str, Any]:
        """获取设备状态"""
        return {
            "device_id": self.device_id,
            "name": self.name,
            "device_type": self.device_type,
            "connected": self.connected,
            "status": self.status,
            "connection_info": self.connection_info,
            "properties": self.properties
        }
    
    def set_state(self, state: Dict[str, Any]) -> None:
        """设置设备状态"""
        self.device_id = state.get("device_id", self.device_id)
        self.name = state.get("name", self.name)
        self.device_type = state.get("device_type", self.device_type)
        self.connected = state.get("connected", self.connected)
        self.status = state.get("status", self.status)
        self.connection_info = state.get("connection_info", self.connection_info)
        self.properties = state.get("properties", self.properties)
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """获取属性值"""
        return self.properties.get(key, default)
    
    def set_property(self, key: str, value: Any) -> None:
        """设置属性值"""
        self.properties[key] = value
    
    def get_connection_info(self, key: str, default: Any = None) -> Any:
        """获取连接信息"""
        return self.connection_info.get(key, default)
    
    def set_connection_info(self, key: str, value: Any) -> None:
        """设置连接信息"""
        self.connection_info[key] = value
    
    def is_connected(self) -> bool:
        """检查设备是否连接"""
        return self.connected
    
    def get_status(self) -> str:
        """获取设备状态"""
        return self.status
    
    def set_status(self, status: str) -> None:
        """设置设备状态"""
        self.status = status
    
    def to_device_info(self) -> DeviceInfo:
        """转换为 DeviceInfo 对象"""
        return DeviceInfo(
            device_id=self.device_id,
            device_type=self.device_type,
            name=self.name,
            connection_info=self.connection_info,
            properties=self.properties,
            connected=self.connected,
            status=self.status
        )
    
    @classmethod
    def from_device_info(cls, device_info: DeviceInfo) -> "BaseDevice":
        """从 DeviceInfo 对象创建设备"""
        device = cls(device_id=device_info.device_id, name=device_info.name)
        device.device_type = device_info.device_type
        device.connection_info = device_info.connection_info
        device.properties = device_info.properties
        device.connected = device_info.connected
        device.status = device_info.status
        return device