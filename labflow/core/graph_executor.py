#!/usr/bin/env python3
"""LabFlow 图执行器"""

import asyncio
import networkx as nx
from typing import List, Dict, Any, Optional
from labflow.workflow.workflow import Workflow
from labflow.nodes.base_node import BaseNode
from labflow.utils.data_structures import DataPacket


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
            
            return True
        except Exception as e:
            print(f"构建执行图失败: {e}")
            return False
    
    async def execute(self) -> bool:
        """执行工作流"""
        if not self.build_graph():
            return False
        
        self.is_running = True
        self.is_paused = False
        self.execution_stats["start_time"] = asyncio.get_event_loop().time()
        
        data_packet = DataPacket()
        
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
                    print(f"节点 {node_id} 未就绪，跳过执行")
                    continue
                
                # 执行节点
                try:
                    node.set_status("running")
                    print(f"开始执行节点: {node.name} (ID: {node_id})")
                    
                    # 记录开始时间
                    start_time = asyncio.get_event_loop().time()
                    
                    # 执行节点逻辑
                    data_packet = await asyncio.to_thread(node.execute, data_packet)
                    
                    # 记录结束时间
                    end_time = asyncio.get_event_loop().time()
                    execution_time = (end_time - start_time) * 1000  # 转换为毫秒
                    
                    node.set_status("success")
                    print(f"节点 {node.name} (ID: {node_id}) 执行成功，耗时: {execution_time:.2f}ms")
                    
                    self.execution_stats["completed_nodes"] += 1
                except Exception as e:
                    node.set_status("error")
                    print(f"节点 {node.name} (ID: {node_id}) 执行失败: {e}")
                    self.execution_stats["failed_nodes"] += 1
                    
                    # 是否继续执行
                    if self.should_continue_on_error():
                        continue
                    else:
                        break
            
            self.execution_stats["end_time"] = asyncio.get_event_loop().time()
            print(f"工作流执行完成")
            print(f"统计信息: 总节点数: {self.execution_stats['total_nodes']}, ")
            print(f"完成节点数: {self.execution_stats['completed_nodes']}, ")
            print(f"失败节点数: {self.execution_stats['failed_nodes']}")
            
            if self.execution_stats['end_time'] and self.execution_stats['start_time']:
                total_time = (self.execution_stats['end_time'] - self.execution_stats['start_time']) * 1000
                print(f"总执行时间: {total_time:.2f}ms")
            
            return self.execution_stats['failed_nodes'] == 0
        finally:
            self.is_running = False
            self.is_paused = False
    
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
        print("工作流执行已暂停")
    
    def resume(self) -> None:
        """恢复执行"""
        self.is_paused = False
        print("工作流执行已恢复")
    
    def stop(self) -> None:
        """停止执行"""
        self.is_running = False
        self.is_paused = False
        print("工作流执行已停止")
    
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
            print(f"节点 {node_id} 不存在")
            return data_packet
        
        try:
            node.set_status("running")
            print(f"开始执行节点: {node.name} (ID: {node_id})")
            
            # 执行节点逻辑
            result = await asyncio.to_thread(node.execute, data_packet)
            
            node.set_status("success")
            print(f"节点 {node.name} (ID: {node_id}) 执行成功")
            
            return result
        except Exception as e:
            node.set_status("error")
            print(f"节点 {node.name} (ID: {node_id}) 执行失败: {e}")
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