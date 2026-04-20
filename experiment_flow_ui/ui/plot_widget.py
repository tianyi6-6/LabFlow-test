#!/usr/bin/env python3
"""LabFlow 数据可视化绘图组件"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg
import numpy as np


class PlotWidget(QWidget):
    """数据可视化绘图组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.curves = []
        self.setup_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)  # 100ms 更新一次
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout()
        
        # 绘图控制栏
        control_layout = QHBoxLayout()
        
        # 绘图类型选择
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems(["折线图", "散点图"])
        self.plot_type_combo.currentTextChanged.connect(self.on_plot_type_changed)
        control_layout.addWidget(QLabel("绘图类型:"))
        control_layout.addWidget(self.plot_type_combo)
        
        # 清除按钮
        clear_button = QPushButton("清除")
        clear_button.clicked.connect(self.clear_plot)
        control_layout.addWidget(clear_button)
        
        # 暂停/继续按钮
        self.pause_button = QPushButton("暂停")
        self.pause_button.clicked.connect(self.toggle_pause)
        control_layout.addWidget(self.pause_button)
        
        layout.addLayout(control_layout)
        
        # 绘图区域
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("w")
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setLabel('bottom', 'X', units='s')
        self.plot_widget.setLabel('left', 'Y', units='V')
        self.plot = self.plot_widget.plot(pen="b")
        
        # 添加坐标拾取功能
        self.plot_widget.scene().sigMouseMoved.connect(self.on_mouse_moved)
        
        layout.addWidget(self.plot_widget, 1)
        
        # 数据信息
        self.data_info = QLabel("数据点: 0")
        self.coord_info = QLabel("坐标: (0, 0)")
        info_layout = QHBoxLayout()
        info_layout.addWidget(self.data_info)
        info_layout.addWidget(self.coord_info)
        layout.addLayout(info_layout)
        
        self.setLayout(layout)
        
        # 暂停状态
        self.is_paused = False
        
        # 初始化曲线
        self.add_curve()
    
    def add_curve(self, color="b", name=""):
        """添加曲线"""
        curve = self.plot_widget.plot(pen=color, name=name)
        self.curves.append(curve)
        return curve
    
    def add_data(self, data, curve_index=0):
        """添加数据"""
        if isinstance(data, list):
            self.data.extend(data)
        else:
            self.data.append(data)
        
        # 限制数据长度
        if len(self.data) > 1000:
            self.data = self.data[-1000:]
        
        # 更新数据信息
        self.data_info.setText(f"数据点: {len(self.data)}")
    
    def update_plot(self):
        """更新绘图"""
        if self.is_paused or len(self.data) == 0:
            return
        
        # 获取绘图类型
        plot_type = self.plot_type_combo.currentText()
        
        if plot_type == "折线图":
            # 折线图
            x = np.arange(len(self.data))
            y = np.array(self.data)
            self.plot.setData(x, y, pen="b")
        elif plot_type == "散点图":
            # 散点图
            x = np.arange(len(self.data))
            y = np.array(self.data)
            self.plot.setData(x, y, pen=None, symbol="o", symbolSize=5, symbolBrush="b")
    
    def clear_plot(self):
        """清除绘图"""
        self.data = []
        self.plot.setData([], [])
        self.data_info.setText("数据点: 0")
    
    def toggle_pause(self):
        """切换暂停状态"""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.setText("继续")
        else:
            self.pause_button.setText("暂停")
    
    def on_plot_type_changed(self, plot_type):
        """绘图类型变更回调"""
        self.update_plot()
    
    def on_mouse_moved(self, pos):
        """鼠标移动回调，实现坐标拾取"""
        # 将屏幕坐标转换为绘图坐标
        view_pos = self.plot_widget.plotItem.vb.mapSceneToView(pos)
        x, y = view_pos.x(), view_pos.y()
        self.coord_info.setText(f"坐标: ({x:.2f}, {y:.2f})")
    
    def set_plot_title(self, title):
        """设置绘图标题"""
        self.plot_widget.setTitle(title)
    
    def set_x_label(self, label):
        """设置X轴标签"""
        self.plot_widget.setLabel('bottom', label)
    
    def set_y_label(self, label):
        """设置Y轴标签"""
        self.plot_widget.setLabel('left', label)
    
    def set_x_range(self, min_val, max_val):
        """设置X轴范围"""
        self.plot_widget.setXRange(min_val, max_val)
    
    def set_y_range(self, min_val, max_val):
        """设置Y轴范围"""
        self.plot_widget.setYRange(min_val, max_val)
    
    def add_data_line(self, data, color="r", name=""):
        """添加数据线条"""
        curve = self.add_curve(color, name)
        x = np.arange(len(data))
        y = np.array(data)
        curve.setData(x, y)
        return curve