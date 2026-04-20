#!/usr/bin/env python3
"""LabFlow 可视化节点"""

import numpy as np
from .base_node import BaseNode
from labflow.utils.data_structures import DataPacket


class set_plot(BaseNode):
    """设置绘图节点"""
    
    def __init__(self, node_id=None, name="set_plot"):
        super().__init__(node_id, name)
        self.node_type = "visualization"
        self.add_input("data_in")
        self.add_output("data_out")
        # 默认参数
        self.properties = {
            "plot_title": "数据可视化",
            "x_label": "X轴",
            "y_label": "Y轴",
            "x_range": [0, 100],
            "y_range": [0, 100],
            "grid_enabled": True
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取数据
        data = data_packet.get_data()
        
        # 执行绘图设置
        print(f"设置绘图: {self.properties['plot_title']}")
        print(f"X轴标签: {self.properties['x_label']}")
        print(f"Y轴标签: {self.properties['y_label']}")
        print(f"X轴范围: {self.properties['x_range']}")
        print(f"Y轴范围: {self.properties['y_range']}")
        print(f"网格: {self.properties['grid_enabled']}")
        
        # 将绘图设置添加到元数据
        data_packet.add_metadata("plot_settings", self.properties)
        
        self.set_status("success")
        return data_packet


class add_data_line(BaseNode):
    """添加数据线条节点"""
    
    def __init__(self, node_id=None, name="add_data_line"):
        super().__init__(node_id, name)
        self.node_type = "visualization"
        self.add_input("data_in")
        self.add_output("data_out")
        # 默认参数
        self.properties = {
            "line_name": "数据线条",
            "line_color": "blue",
            "line_width": 2,
            "line_style": "solid",
            "marker_enabled": False,
            "marker_style": "o"
        }
    
    def execute(self, data_packet: DataPacket) -> DataPacket:
        """执行节点逻辑"""
        self.set_status("running")
        
        # 获取数据
        data = data_packet.get_data()
        
        # 执行添加数据线条
        print(f"添加数据线条: {self.properties['line_name']}")
        print(f"线条颜色: {self.properties['line_color']}")
        print(f"线条宽度: {self.properties['line_width']}")
        print(f"线条样式: {self.properties['line_style']}")
        print(f"标记: {self.properties['marker_enabled']}")
        if self.properties['marker_enabled']:
            print(f"标记样式: {self.properties['marker_style']}")
        
        # 将线条设置添加到元数据
        line_settings = {
            "name": self.properties['line_name'],
            "color": self.properties['line_color'],
            "width": self.properties['line_width'],
            "style": self.properties['line_style'],
            "marker": self.properties['marker_style'] if self.properties['marker_enabled'] else None
        }
        
        # 获取现有线条列表
        lines = data_packet.get_metadata_value("plot_lines", [])
        lines.append(line_settings)
        data_packet.add_metadata("plot_lines", lines)
        
        # 打印数据信息
        if len(data) > 0:
            print(f"数据长度: {len(data)}")
            print(f"数据范围: [{np.min(data)}, {np.max(data)}]")
        
        self.set_status("success")
        return data_packet