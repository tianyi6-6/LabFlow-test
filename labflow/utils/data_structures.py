#!/usr/bin/env python3
"""LabFlow 数据结构"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple


@dataclass
class DataPacket:
    """数据包类"""
    data: np.ndarray = field(default_factory=lambda: np.array([]))
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_data(self) -> np.ndarray:
        """获取数据"""
        return self.data
    
    def get_metadata(self) -> Dict[str, Any]:
        """获取元数据"""
        return self.metadata
    
    def set_data(self, data: np.ndarray) -> None:
        """设置数据"""
        self.data = data
    
    def set_metadata(self, metadata: Dict[str, Any]) -> None:
        """设置元数据"""
        self.metadata = metadata
    
    def add_metadata(self, key: str, value: Any) -> None:
        """添加元数据"""
        self.metadata[key] = value
    
    def get_metadata_value(self, key: str, default: Any = None) -> Any:
        """获取元数据值"""
        return self.metadata.get(key, default)


@dataclass
class NodeInfo:
    """节点信息类"""
    node_id: str
    node_type: str
    name: str
    position: Tuple[float, float]
    properties: Dict[str, Any] = field(default_factory=dict)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    status: str = "idle"  # idle, running, success, error
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """获取属性值"""
        return self.properties.get(key, default)
    
    def set_property(self, key: str, value: Any) -> None:
        """设置属性值"""
        self.properties[key] = value
    
    def add_input(self, input_name: str) -> None:
        """添加输入端口"""
        if input_name not in self.inputs:
            self.inputs.append(input_name)
    
    def add_output(self, output_name: str) -> None:
        """添加输出端口"""
        if output_name not in self.outputs:
            self.outputs.append(output_name)


@dataclass
class DeviceInfo:
    """设备信息类"""
    device_id: str
    device_type: str
    name: str
    connection_info: Dict[str, Any]
    properties: Dict[str, Any] = field(default_factory=dict)
    connected: bool = False
    status: str = "offline"  # offline, online, warning, error
    
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