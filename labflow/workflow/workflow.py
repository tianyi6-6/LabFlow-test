#!/usr/bin/env python3
"""LabFlow 工作流类"""

from typing import Dict, List, Optional, Tuple
from labflow.nodes.base_node import BaseNode
from labflow.utils.helpers import generate_id


class Workflow:
    """工作流类"""
    
    def __init__(self, workflow_id: Optional[str] = None, name: str = "Untitled Workflow"):
        self.workflow_id = workflow_id or generate_id("workflow_")
        self.name = name
        self.nodes: Dict[str, BaseNode] = {}
        self.edges: List[Tuple[str, str, str, str]] = []  # (source_node_id, source_port, target_node_id, target_port)
        self.variables: Dict[str, any] = {}
        self.pages: List[str] = []
        self.current_page = "main"
    
    def add_node(self, node: BaseNode) -> bool:
        """添加节点"""
        if node.node_id in self.nodes:
            print(f"节点 {node.node_id} 已存在")
            return False
        self.nodes[node.node_id] = node
        print(f"节点 {node.name} (ID: {node.node_id}) 添加成功")
        return True
    
    def remove_node(self, node_id: str) -> bool:
        """移除节点"""
        if node_id not in self.nodes:
            print(f"节点 {node_id} 不存在")
            return False
        # 移除与该节点相关的所有边
        self.edges = [edge for edge in self.edges if edge[0] != node_id and edge[2] != node_id]
        # 移除节点
        del self.nodes[node_id]
        print(f"节点 {node_id} 移除成功")
        return True
    
    def add_edge(self, source_node_id: str, source_port: str, target_node_id: str, target_port: str) -> bool:
        """添加边"""
        # 检查源节点和目标节点是否存在
        if source_node_id not in self.nodes:
            print(f"源节点 {source_node_id} 不存在")
            return False
        if target_node_id not in self.nodes:
            print(f"目标节点 {target_node_id} 不存在")
            return False
        
        # 检查源端口和目标端口是否存在
        source_node = self.nodes[source_node_id]
        target_node = self.nodes[target_node_id]
        if source_port not in source_node.outputs:
            print(f"源节点 {source_node_id} 没有输出端口 {source_port}")
            return False
        if target_port not in target_node.inputs:
            print(f"目标节点 {target_node_id} 没有输入端口 {target_port}")
            return False
        
        # 检查边是否已经存在
        edge = (source_node_id, source_port, target_node_id, target_port)
        if edge in self.edges:
            print(f"边 {edge} 已存在")
            return False
        
        # 添加边
        self.edges.append(edge)
        print(f"边 {edge} 添加成功")
        return True
    
    def remove_edge(self, source_node_id: str, source_port: str, target_node_id: str, target_port: str) -> bool:
        """移除边"""
        edge = (source_node_id, source_port, target_node_id, target_port)
        if edge not in self.edges:
            print(f"边 {edge} 不存在")
            return False
        self.edges.remove(edge)
        print(f"边 {edge} 移除成功")
        return True
    
    def get_node(self, node_id: str) -> Optional[BaseNode]:
        """获取节点"""
        return self.nodes.get(node_id)
    
    def get_nodes(self) -> List[BaseNode]:
        """获取所有节点"""
        return list(self.nodes.values())
    
    def get_edges(self) -> List[Tuple[str, str, str, str]]:
        """获取所有边"""
        return self.edges
    
    def get_node_edges(self, node_id: str) -> List[Tuple[str, str, str, str]]:
        """获取与节点相关的所有边"""
        return [edge for edge in self.edges if edge[0] == node_id or edge[2] == node_id]
    
    def add_variable(self, name: str, value: any) -> bool:
        """添加变量"""
        self.variables[name] = value
        print(f"变量 {name} 添加成功，值: {value}")
        return True
    
    def remove_variable(self, name: str) -> bool:
        """移除变量"""
        if name not in self.variables:
            print(f"变量 {name} 不存在")
            return False
        del self.variables[name]
        print(f"变量 {name} 移除成功")
        return True
    
    def get_variable(self, name: str, default: any = None) -> any:
        """获取变量值"""
        return self.variables.get(name, default)
    
    def set_variable(self, name: str, value: any) -> bool:
        """设置变量值"""
        self.variables[name] = value
        print(f"变量 {name} 设置成功，值: {value}")
        return True
    
    def add_page(self, page_name: str) -> bool:
        """添加页面"""
        if page_name in self.pages:
            print(f"页面 {page_name} 已存在")
            return False
        self.pages.append(page_name)
        print(f"页面 {page_name} 添加成功")
        return True
    
    def remove_page(self, page_name: str) -> bool:
        """移除页面"""
        if page_name not in self.pages:
            print(f"页面 {page_name} 不存在")
            return False
        if page_name == self.current_page:
            print(f"不能移除当前页面 {page_name}")
            return False
        self.pages.remove(page_name)
        print(f"页面 {page_name} 移除成功")
        return True
    
    def set_current_page(self, page_name: str) -> bool:
        """设置当前页面"""
        if page_name not in self.pages:
            print(f"页面 {page_name} 不存在")
            return False
        self.current_page = page_name
        print(f"当前页面设置为 {page_name}")
        return True
    
    def get_current_page(self) -> str:
        """获取当前页面"""
        return self.current_page
    
    def get_pages(self) -> List[str]:
        """获取所有页面"""
        return self.pages
    
    def get_state(self) -> Dict[str, any]:
        """获取工作流状态"""
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "nodes": {node_id: node.get_state() for node_id, node in self.nodes.items()},
            "edges": self.edges,
            "variables": self.variables,
            "pages": self.pages,
            "current_page": self.current_page
        }
    
    def set_state(self, state: Dict[str, any]) -> None:
        """设置工作流状态"""
        self.workflow_id = state.get("workflow_id", self.workflow_id)
        self.name = state.get("name", self.name)
        self.edges = state.get("edges", self.edges)
        self.variables = state.get("variables", self.variables)
        self.pages = state.get("pages", self.pages)
        self.current_page = state.get("current_page", self.current_page)
        
        # 恢复节点
        from labflow.nodes.base_node import BaseNode
        from labflow.nodes.device_control import SetLockInFreq, SetLockInPhase, SetLockInTimeCo, USB_START, USB_END
        from labflow.nodes.data_acquisition import SetDataSampleRate, get_max_slope
        from labflow.nodes.signal_processing import lockin_res, log_insert_compile
        from labflow.nodes.control_flow import LoopRepeat, add_row_data
        from labflow.nodes.visualization import set_plot, add_data_line
        from labflow.nodes.custom_nodes import CustomNode
        
        node_classes = {
            "SetLockInFreq": SetLockInFreq,
            "SetLockInPhase": SetLockInPhase,
            "SetLockInTimeCo": SetLockInTimeCo,
            "USB_START": USB_START,
            "USB_END": USB_END,
            "SetDataSampleRate": SetDataSampleRate,
            "get_max_slope": get_max_slope,
            "lockin_res": lockin_res,
            "log_insert_compile": log_insert_compile,
            "LoopRepeat": LoopRepeat,
            "add_row_data": add_row_data,
            "set_plot": set_plot,
            "add_data_line": add_data_line,
            "CustomNode": CustomNode
        }
        
        self.nodes = {}
        for node_id, node_state in state.get("nodes", {}).items():
            node_type = node_state.get("node_type", "base")
            node_class = node_classes.get(node_state.get("name"), BaseNode)
            node = node_class(node_id=node_id)
            node.set_state(node_state)
            self.nodes[node_id] = node
    
    def clear(self) -> None:
        """清空工作流"""
        self.nodes.clear()
        self.edges.clear()
        self.variables.clear()
        self.pages = ["main"]
        self.current_page = "main"
        print("工作流清空成功")
    
    def get_node_count(self) -> int:
        """获取节点数量"""
        return len(self.nodes)
    
    def get_edge_count(self) -> int:
        """获取边数量"""
        return len(self.edges)
    
    def get_variable_count(self) -> int:
        """获取变量数量"""
        return len(self.variables)