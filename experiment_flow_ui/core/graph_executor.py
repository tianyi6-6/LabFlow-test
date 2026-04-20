#!/usr/bin/env python3
"""LabFlow 图执行器"""

import asyncio
import networkx as nx
from typing import List, Dict, Any, Optional
from experiment_flow_ui.core.base_workflow import Workflow
from experiment_flow_ui.core.base_node import BaseNode
from experiment_flow_ui.utils.data_structures import DataPacket


class GraphExecutor:
    """图执行器类"""
    
    def __init__(self, workflow: Workflow):
        self.workflow = workflow
        self.graph = nx.DiGraph()
        self.execution_order: List[str] = []
        self.is_running = False
        self.is_paused = False
        self.execution_stats = {
            "total_nodes": 0,
            "completed_nodes": 0,
            "failed_nodes": 0,
            "start_time": None,
            "end_time": None
        }
        self.data_cache: Dict[str, Dict[str, Any]] = {}  # 节点输出缓存
        self.node_status_callback = None  # 节点状态变化回调
        self.log_callback = None  # 日志回调
    
    def build_graph(self) -> bool:
        """构建执行图"""
        try:
            # 清空图
            self.graph.clear()
            
            # 添加节点
            for node_id, node in self.workflow.nodes.items():
                self.graph.add_node(node_id, node=node)
            
            # 添加边
            for edge in self.workflow.edges:
                source_node_id, source_port, target_node_id, target_port = edge
                self.graph.add_edge(source_node_id, target_node_id, 
                                   source_port=source_port, 
                                   target_port=target_port)
            
            # 检查是否有环
            if not nx.is_directed_acyclic_graph(self.graph):
                print("工作流中存在循环依赖，无法执行")
                return False
            
            # 拓扑排序
            self.execution_order = list(nx.topological_sort(self.graph))
            print(f"执行顺序: {self.execution_order}")
            
            # 更新执行统计
            self.execution_stats["total_nodes"] = len(self.execution_order)
            self.execution_stats["completed_nodes"] = 0
            self.execution_stats["failed_nodes"] = 0
            
            # 清空数据缓存
            self.data_cache = {}
            
            return True
        except Exception as e:
            print(f"构建执行图失败: {e}")
            return False
    
    def set_node_status_callback(self, callback):
        """设置节点状态变化回调"""
        self.node_status_callback = callback
    
    def set_log_callback(self, callback):
        """设置日志回调"""
        self.log_callback = callback
    
    def log(self, message):
        """记录日志"""
        if self.log_callback:
            self.log_callback(message)
        print(message)
    
    def update_node_status(self, node_id, status):
        """更新节点状态"""
        node = self.workflow.get_node(node_id)
        if node:
            node.set_status(status)
            if self.node_status_callback:
                self.node_status_callback(node_id, status)
    
    async def execute(self) -> bool:
        """执行工作流"""
        if not self.build_graph():
            return False
        
        self.is_running = True
        self.is_paused = False
        self.execution_stats["start_time"] = asyncio.get_event_loop().time()
        
        try:
            for node_id in self.execution_order:
                if not self.is_running:
                    break
                
                while self.is_paused:
                    await asyncio.sleep(0.1)
                
                node = self.workflow.get_node(node_id)
                if not node:
                    continue
                
                # 检查节点是否就绪
                if not self.check_node_ready(node):
                    self.log(f"节点 {node_id} 未就绪，跳过执行")
                    continue
                
                # 执行节点
                try:
                    self.update_node_status(node_id, "running")
                    self.log(f"开始执行节点: {node.name} (ID: {node_id})")
                    
                    # 记录开始时间
                    start_time = asyncio.get_event_loop().time()
                    
                    # 准备节点输入数据
                    input_data = self._prepare_node_input(node_id)
                    
                    # 执行节点逻辑
                    output_data = await asyncio.to_thread(node.execute, DataPacket(data=input_data))
                    
                    # 记录输出数据到缓存
                    self._cache_node_output(node_id, output_data.data if hasattr(output_data, 'data') else output_data)
                    
                    # 记录结束时间
                    end_time = asyncio.get_event_loop().time()
                    execution_time = (end_time - start_time) * 1000  # 转换为毫秒
                    
                    self.update_node_status(node_id, "success")
                    self.log(f"节点 {node.name} (ID: {node_id}) 执行成功，耗时: {execution_time:.2f}ms")
                    
                    self.execution_stats["completed_nodes"] += 1
                except Exception as e:
                    self.update_node_status(node_id, "error")
                    self.log(f"节点 {node.name} (ID: {node_id}) 执行失败: {e}")
                    self.execution_stats["failed_nodes"] += 1
                    
                    # 是否继续执行
                    if not self.should_continue_on_error():
                        break
            
            self.execution_stats["end_time"] = asyncio.get_event_loop().time()
            self.log("工作流执行完成")
            self.log(f"统计信息: 总节点数: {self.execution_stats['total_nodes']}, ")
            self.log(f"完成节点数: {self.execution_stats['completed_nodes']}, ")
            self.log(f"失败节点数: {self.execution_stats['failed_nodes']}")
            
            if self.execution_stats['end_time'] and self.execution_stats['start_time']:
                total_time = (self.execution_stats['end_time'] - self.execution_stats['start_time']) * 1000
                self.log(f"总执行时间: {total_time:.2f}ms")
            
            return self.execution_stats['failed_nodes'] == 0
        finally:
            self.is_running = False
            self.is_paused = False
    
    def _prepare_node_input(self, node_id):
        """准备节点输入数据"""
        input_data = {}
        
        # 获取所有前置节点
        predecessors = list(self.graph.predecessors(node_id))
        for pred_id in predecessors:
            # 获取从该前置节点到当前节点的所有边
            edges = self.graph.get_edge_data(pred_id, node_id)
            if isinstance(edges, dict):
                edges = [edges]
            
            for edge in edges:
                source_port = edge.get('source_port')
                target_port = edge.get('target_port')
                
                # 从缓存中获取前置节点的输出数据
                if pred_id in self.data_cache and source_port in self.data_cache[pred_id]:
                    input_data[target_port] = self.data_cache[pred_id][source_port]
        
        return input_data
    
    def _cache_node_output(self, node_id, output_data):
        """缓存节点输出数据"""
        if isinstance(output_data, dict):
            self.data_cache[node_id] = output_data
        else:
            # 如果输出不是字典，尝试将其作为默认输出端口的数据
            self.data_cache[node_id] = {"output": output_data}
    
    def check_node_ready(self, node: BaseNode) -> bool:
        """检查节点是否就绪"""
        # 检查所有前置节点是否执行成功
        predecessors = list(self.graph.predecessors(node.node_id))
        for pred_id in predecessors:
            pred_node = self.workflow.get_node(pred_id)
            if pred_node and pred_node.get_status() != "success":
                return False
        return True
    
    def pause(self) -> None:
        """暂停执行"""
        self.is_paused = True
        self.log("工作流执行已暂停")
    
    def resume(self) -> None:
        """恢复执行"""
        self.is_paused = False
        self.log("工作流执行已恢复")
    
    def stop(self) -> None:
        """停止执行"""
        self.is_running = False
        self.is_paused = False
        self.log("工作流执行已停止")
    
    def should_continue_on_error(self) -> bool:
        """是否在错误时继续执行"""
        # 可以从配置中读取，这里默认继续执行
        return True
    
    def get_execution_order(self) -> List[str]:
        """获取执行顺序"""
        return self.execution_order
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """获取执行统计信息"""
        return self.execution_stats
    
    def get_running_status(self) -> bool:
        """获取运行状态"""
        return self.is_running
    
    def get_paused_status(self) -> bool:
        """获取暂停状态"""
        return self.is_paused
    
    async def execute_node(self, node_id: str, data_packet: DataPacket) -> DataPacket:
        """执行单个节点"""
        node = self.workflow.get_node(node_id)
        if not node:
            self.log(f"节点 {node_id} 不存在")
            return data_packet
        
        try:
            self.update_node_status(node_id, "running")
            self.log(f"开始执行节点: {node.name} (ID: {node_id})")
            
            # 执行节点逻辑
            result = await asyncio.to_thread(node.execute, data_packet)
            
            self.update_node_status(node_id, "success")
            self.log(f"节点 {node.name} (ID: {node_id}) 执行成功")
            
            return result
        except Exception as e:
            self.update_node_status(node_id, "error")
            self.log(f"节点 {node.name} (ID: {node_id}) 执行失败: {e}")
            return data_packet
    
    def get_node_dependencies(self, node_id: str) -> List[str]:
        """获取节点的依赖节点"""
        return list(self.graph.predecessors(node_id))
    
    def get_node_successors(self, node_id: str) -> List[str]:
        """获取节点的后继节点"""
        return list(self.graph.successors(node_id))
    
    def get_graph(self) -> nx.DiGraph:
        """获取执行图"""
        return self.graph
    
    def get_execution_progress(self) -> float:
        """获取执行进度"""
        if self.execution_stats["total_nodes"] == 0:
            return 0.0
        return (self.execution_stats["completed_nodes"] + self.execution_stats["failed_nodes"]) / self.execution_stats["total_nodes"] * 100