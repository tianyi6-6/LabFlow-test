#!/usr/bin/env python3
"""LabFlow 基础节点类"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from labflow.utils.data_structures import DataPacket, NodeInfo
from labflow.utils.helpers import generate_id


class BaseNode(ABC):
    """基础节点类"""
    
    def __init__(self, node_id: Optional[str] = None, name: str = "BaseNode"):
        self.node_id = node_id or generate_id("node_")
        self.name = name
        self.inputs: List[str] = []
        self.outputs: List[str] = []
        self.position: Tuple[float, float] = (0, 0)
        self.properties: Dict[str, Any] = {}
        self.status: str = "idle"  # idle, running, success, error
        self.node_type: str = "base"
    
    @abstractmethod
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """获取节点状态"""
        return {
            "node_id": self.node_id,
            "name": self.name,
            "node_type": self.node_type,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "position": self.position,
            "properties": self.properties,
            "status": self.status
        }
    
    def set_state(self, state: Dict[str, Any]) -> None:
        """设置节点状态"""
        self.node_id = state.get("node_id", self.node_id)
        self.name = state.get("name", self.name)
        self.node_type = state.get("node_type", self.node_type)
        self.inputs = state.get("inputs", self.inputs)
        self.outputs = state.get("outputs", self.outputs)
        self.position = state.get("position", self.position)
        self.properties = state.get("properties", self.properties)
        self.status = state.get("status", self.status)
    
    def add_input(self, input_name: str) -> None:
        """添加输入端口"""
        if input_name not in self.inputs:
            self.inputs.append(input_name)
    
    def add_output(self, output_name: str) -> None:
        """添加输出端口"""
        if output_name not in self.outputs:
            self.outputs.append(output_name)
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """获取属性值"""
        return self.properties.get(key, default)
    
    def set_property(self, key: str, value: Any) -> None:
        """设置属性值"""
        self.properties[key] = value
    
    def set_position(self, position: Tuple[float, float]) -> None:
        """设置节点位置"""
        self.position = position
    
    def get_position(self) -> Tuple[float, float]:
        """获取节点位置"""
        return self.position
    
    def set_status(self, status: str) -> None:
        """设置节点状态"""
        self.status = status
    
    def get_status(self) -> str:
        """获取节点状态"""
        return self.status
    
    def to_node_info(self) -> NodeInfo:
        """转换为 NodeInfo 对象"""
        return NodeInfo(
            node_id=self.node_id,
            node_type=self.node_type,
            name=self.name,
            position=self.position,
            properties=self.properties,
            inputs=self.inputs,
            outputs=self.outputs,
            status=self.status
        )
    
    @classmethod
    def from_node_info(cls, node_info: NodeInfo) -> "BaseNode":
        """从 NodeInfo 对象创建节点"""
        node = cls(node_id=node_info.node_id, name=node_info.name)
        node.node_type = node_info.node_type
        node.position = node_info.position
        node.properties = node_info.properties
        node.inputs = node_info.inputs
        node.outputs = node_info.outputs
        node.status = node_info.status
        return node