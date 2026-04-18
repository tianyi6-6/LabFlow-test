#!/usr/bin/env python3
"""LabFlow 工作流持久化"""

import json
import os
from typing import Optional
from .workflow import Workflow


class WorkflowPersistence:
    """工作流持久化类"""
    
    def __init__(self):
        pass
    
    def save_workflow(self, workflow: Workflow, file_path: str) -> bool:
        """保存工作流到文件"""
        try:
            # 创建目录（如果不存在）
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 获取工作流状态
            state = workflow.get_state()
            
            # 保存到 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            
            print(f"工作流 {workflow.name} 保存成功，路径: {file_path}")
            return True
        except Exception as e:
            print(f"保存工作流失败: {e}")
            return False
    
    def load_workflow(self, file_path: str) -> Optional[Workflow]:
        """从文件加载工作流"""
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                print(f"文件 {file_path} 不存在")
                return None
            
            # 读取 JSON 文件
            with open(file_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            # 创建工作流并恢复状态
            workflow = Workflow()
            workflow.set_state(state)
            
            print(f"工作流 {workflow.name} 加载成功，路径: {file_path}")
            return workflow
        except Exception as e:
            print(f"加载工作流失败: {e}")
            return None
    
    def export_workflow(self, workflow: Workflow, file_path: str, export_format: str = "json") -> bool:
        """导出工作流"""
        try:
            if export_format == "json":
                # 导出为 JSON 文件
                return self.save_workflow(workflow, file_path)
            elif export_format == "python":
                # 导出为 Python 脚本
                return self._export_to_python(workflow, file_path)
            elif export_format == "report":
                # 导出为实验报告
                return self._export_to_report(workflow, file_path)
            else:
                print(f"不支持的导出格式: {export_format}")
                return False
        except Exception as e:
            print(f"导出工作流失败: {e}")
            return False
    
    def _export_to_python(self, workflow: Workflow, file_path: str) -> bool:
        """导出为 Python 脚本"""
        try:
            # 创建目录（如果不存在）
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 生成 Python 脚本
            script = f"#!/usr/bin/env python3
\"\"\"LabFlow 工作流脚本\"\"\"

import asyncio
from labflow.nodes.device_control import SetLockInFreq, SetLockInPhase, SetLockInTimeCo, USB_START, USB_END
from labflow.nodes.data_acquisition import SetDataSampleRate, get_max_slope
from labflow.nodes.signal_processing import lockin_res, log_insert_compile
from labflow.nodes.control_flow import LoopRepeat, add_row_data
from labflow.nodes.visualization import set_plot, add_data_line
from labflow.nodes.custom_nodes import CustomNode
from labflow.utils.data_structures import DataPacket


async def main():
    \"\"\"主函数\"\"\"
    # 创建节点
    nodes = {}


            # 添加节点创建代码
            for node_id, node in workflow.nodes.items():
                node_name = node.name
                node_class = node_name
                script += f"    nodes['{node_id}'] = {node_class}(node_id='{node_id}', name='{node.name}')\n"
                # 设置节点属性
                for key, value in node.properties.items():
                    if isinstance(value, str):
                        script += f"    nodes['{node_id}'].set_property('{key}', '{value}')\n"
                    else:
                        script += f"    nodes['{node_id}'].set_property('{key}', {value})\n"
                # 设置节点位置
                x, y = node.position
                script += f"    nodes['{node_id}'].set_position(({x}, {y}))\n"
            
            # 添加执行逻辑
            script += "\n    # 执行工作流\n"
            script += "    data_packet = DataPacket()\n"
            script += "    for node_id in ["
            # 这里应该按照拓扑顺序执行节点
            # 简化处理，按节点 ID 顺序执行
            node_ids = list(workflow.nodes.keys())
            script += ", ".join([f"'{node_id}'" for node_id in node_ids])
            script += "]:\n"
            script += "        print(f'执行节点: {node_id}')\n"
            script += "        data_packet = nodes[node_id].execute(data_packet)\n"
            script += "\n"
            script += "if __name__ == '__main__':\n"
            script += "    asyncio.run(main())\n"
            
            # 保存脚本文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(script)
            
            print(f"工作流 {workflow.name} 导出为 Python 脚本成功，路径: {file_path}")
            return True
        except Exception as e:
            print(f"导出为 Python 脚本失败: {e}")
            return False
    
    def _export_to_report(self, workflow: Workflow, file_path: str) -> bool:
        """导出为实验报告"""
        try:
            # 创建目录（如果不存在）
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 生成实验报告
            report = f"# LabFlow 实验报告\n\n"
            report += f"## 工作流信息\n\n"
            report += f"- 工作流名称: {workflow.name}\n"
            report += f"- 工作流 ID: {workflow.workflow_id}\n"
            report += f"- 节点数量: {workflow.get_node_count()}\n"
            report += f"- 边数量: {workflow.get_edge_count()}\n"
            report += f"- 变量数量: {workflow.get_variable_count()}\n\n"
            
            report += "## 节点列表\n\n"
            for node_id, node in workflow.nodes.items():
                report += f"### {node.name} (ID: {node_id})\n\n"
                report += f"- 类型: {node.node_type}\n"
                report += f"- 输入端口: {', '.join(node.inputs)}\n"
                report += f"- 输出端口: {', '.join(node.outputs)}\n"
                report += f"- 位置: {node.position}\n"
                report += f"- 属性: {node.properties}\n\n"
            
            report += "## 边列表\n\n"
            for edge in workflow.edges:
                source_node_id, source_port, target_node_id, target_port = edge
                source_node = workflow.nodes.get(source_node_id)
                target_node = workflow.nodes.get(target_node_id)
                if source_node and target_node:
                    report += f"- {source_node.name}({source_port}) -> {target_node.name}({target_port})\n"
            
            report += "\n## 变量列表\n\n"
            for name, value in workflow.variables.items():
                report += f"- {name}: {value}\n"
            
            # 保存报告文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"工作流 {workflow.name} 导出为实验报告成功，路径: {file_path}")
            return True
        except Exception as e:
            print(f"导出为实验报告失败: {e}")
            return False
    
    def list_workflows(self, directory: str) -> list:
        """列出目录中的工作流文件"""
        workflows = []
        try:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    if file.endswith('.json'):
                        file_path = os.path.join(directory, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                state = json.load(f)
                            workflow_name = state.get('name', 'Untitled Workflow')
                            workflows.append({
                                'name': workflow_name,
                                'file_path': file_path,
                                'node_count': len(state.get('nodes', {})),
                                'edge_count': len(state.get('edges', []))
                            })
                        except Exception:
                            pass
        except Exception as e:
            print(f"列出工作流失败: {e}")
        return workflows