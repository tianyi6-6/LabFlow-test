#!/usr/bin/env python3
"""LabFlow 主窗口"""

from PySide6.QtWidgets import (
    QMainWindow, QMenuBar, QToolBar, QWidget, QSplitter,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget,
    QFormLayout, QGroupBox, QProgressBar, QLineEdit, QTreeWidget, QTreeWidgetItem, QToolButton
)
from PySide6.QtGui import QAction, QColor, QFont
from PySide6.QtCore import Qt, QSize
from .node_canvas import NodeCanvas
from .property_panel import PropertyPanel
from .plot_widget import PlotWidget
from .dock_panel import DockPanel
from .panel_state_manager import PanelStateManager
from .tool_window_manager import ToolWindowManager
from .styled_splitter import StyledSplitter


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.state_manager = PanelStateManager()
        self.tool_window_manager = ToolWindowManager(self)
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        # 设置窗口标题和大小
        self.setWindowTitle("LabFlow")
        self.resize(1600, 900)
        
        # 加载样式文件
        self.load_styles()
        
        # 创建中央部件（使用QSplitter实现多层嵌套布局）
        self.create_central_widget()
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
    
    def load_styles(self):
        """加载样式文件"""
        stylesheet_path = "labflow/app/styles.qss"
        try:
            with open(stylesheet_path, "r", encoding="utf-8") as f:
                stylesheet = f.read()
                self.setStyleSheet(stylesheet)
        except Exception as e:
            print(f"加载样式文件失败: {e}")
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        new_action = QAction("新建", self)
        open_action = QAction("打开", self)
        save_action = QAction("保存", self)
        save_as_action = QAction("另存为", self)
        exit_action = QAction("退出", self)
        file_menu.addActions([new_action, open_action, save_action, save_as_action])
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        undo_action = QAction("撤销", self)
        redo_action = QAction("重做", self)
        cut_action = QAction("剪切", self)
        copy_action = QAction("复制", self)
        paste_action = QAction("粘贴", self)
        edit_menu.addActions([undo_action, redo_action])
        edit_menu.addSeparator()
        edit_menu.addActions([cut_action, copy_action, paste_action])
        
        # 设备菜单
        device_menu = menu_bar.addMenu("设备")
        connect_action = QAction("连接设备", self)
        disconnect_action = QAction("断开设备", self)
        device_menu.addActions([connect_action, disconnect_action])
        
        # 流程菜单
        flow_menu = menu_bar.addMenu("流程")
        run_action = QAction("运行", self)
        pause_action = QAction("暂停", self)
        stop_action = QAction("停止", self)
        flow_menu.addActions([run_action, pause_action, stop_action])
        
        # 视图菜单
        view_menu = menu_bar.addMenu("视图")
        zoom_in_action = QAction("放大", self)
        zoom_out_action = QAction("缩小", self)
        zoom_reset_action = QAction("重置缩放", self)
        view_menu.addActions([zoom_in_action, zoom_out_action, zoom_reset_action])
        
        # 工具窗口子菜单
        tool_windows_menu = view_menu.addMenu("工具窗口")
        
        # 资源栏菜单项
        left_dock_action = QAction("资源栏", self)
        left_dock_action.setCheckable(True)
        left_dock_action.setChecked(self.tool_window_manager.get_tool_window("LeftDock").isVisible())
        left_dock_action.triggered.connect(lambda: self.tool_window_manager.toggle_tool_window("LeftDock"))
        # 添加快捷键
        left_dock_action.setShortcut("Ctrl+1")
        tool_windows_menu.addAction(left_dock_action)
        
        # 数据可视化面板菜单项
        plot_dock_action = QAction("数据可视化", self)
        plot_dock_action.setCheckable(True)
        plot_dock_action.setChecked(self.tool_window_manager.get_tool_window("PlotDock").isVisible())
        plot_dock_action.triggered.connect(lambda: self.tool_window_manager.toggle_tool_window("PlotDock"))
        # 添加快捷键
        plot_dock_action.setShortcut("Ctrl+2")
        tool_windows_menu.addAction(plot_dock_action)
        
        # 参数与执行监控面板菜单项
        property_dock_action = QAction("参数与执行监控", self)
        property_dock_action.setCheckable(True)
        property_dock_action.setChecked(self.tool_window_manager.get_tool_window("PropertyDock").isVisible())
        property_dock_action.triggered.connect(lambda: self.tool_window_manager.toggle_tool_window("PropertyDock"))
        # 添加快捷键
        property_dock_action.setShortcut("Ctrl+3")
        tool_windows_menu.addAction(property_dock_action)
        
        # 日志面板菜单项
        log_dock_action = QAction("日志", self)
        log_dock_action.setCheckable(True)
        log_dock_action.setChecked(self.tool_window_manager.get_tool_window("LogDock").isVisible())
        log_dock_action.triggered.connect(lambda: self.tool_window_manager.toggle_tool_window("LogDock"))
        # 添加快捷键
        log_dock_action.setShortcut("Ctrl+4")
        tool_windows_menu.addAction(log_dock_action)
        
        # 状态栏菜单项 - 已删除
        # bottom_dock_action = QAction("状态栏", self)
        # bottom_dock_action.setCheckable(True)
        # bottom_dock_action.setChecked(self.tool_window_manager.get_tool_window("BottomDock").isVisible())
        # bottom_dock_action.triggered.connect(lambda: self.tool_window_manager.toggle_tool_window("BottomDock"))
        # # 添加快捷键
        # bottom_dock_action.setShortcut("Ctrl+4")
        # tool_windows_menu.addAction(bottom_dock_action)
        

        
        # 重置窗口布局菜单项
        reset_layout_action = QAction("重置窗口布局", self)
        reset_layout_action.triggered.connect(self.tool_window_manager.reset_layout)
        view_menu.addAction(reset_layout_action)
        
        # 工具菜单
        tool_menu = menu_bar.addMenu("工具")
        options_action = QAction("选项", self)
        tool_menu.addAction(options_action)
        
        # 设置菜单
        settings_menu = menu_bar.addMenu("设置")
        preferences_action = QAction("首选项", self)
        settings_menu.addAction(preferences_action)
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)
    
    def create_tool_bar(self):
        """创建工具栏"""
        tool_bar = QToolBar("操作栏")
        tool_bar.setIconSize(QSize(24, 24))
        
        # 程序按钮
        program_button = QPushButton("程序")
        tool_bar.addWidget(program_button)
        
        # 运行按钮（绿色）
        run_button = QPushButton("运行")
        run_button.setStyleSheet("background-color: green; color: white;")
        tool_bar.addWidget(run_button)
        
        # 暂停按钮（黄色）
        pause_button = QPushButton("暂停")
        pause_button.setStyleSheet("background-color: yellow; color: black;")
        tool_bar.addWidget(pause_button)
        
        # 停止按钮（红色）
        stop_button = QPushButton("停止")
        stop_button.setStyleSheet("background-color: red; color: white;")
        tool_bar.addWidget(stop_button)
        
        # 导出按钮
        export_button = QPushButton("导出")
        tool_bar.addWidget(export_button)
        
        # 节点库按钮
        nodes_button = QPushButton("节点库")
        tool_bar.addWidget(nodes_button)
        
        self.addToolBar(tool_bar)
    
    def create_central_widget(self):
        """创建中央部件（使用QSplitter实现多层嵌套布局）"""
        # 创建中央画布区域
        canvas_widget = QWidget()
        canvas_layout = QVBoxLayout(canvas_widget)
        canvas_title = QLabel("工作流画布")
        canvas_title.setAlignment(Qt.AlignCenter)
        canvas_title.setFont(QFont("Arial", 12, QFont.Bold))
        canvas_layout.addWidget(canvas_title)
        
        self.canvas = NodeCanvas()
        canvas_layout.addWidget(self.canvas, 1)
        
        # 设置中央部件为画布区域
        self.setCentralWidget(canvas_widget)
        
        # 创建日志面板，直接位于窗口底部
        from .log_panel import LogPanel
        self.log_dock = DockPanel("日志", self, "LogDock")
        self.log_dock.setObjectName("LogDock")
        self.log_dock.setAllowedAreas(Qt.AllDockWidgetAreas)  # 支持所有停靠区域
        log_panel = LogPanel()
        self.log_dock.add_content(log_panel)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.log_dock)
        
        # 创建左侧可停靠面板
        left_dock = DockPanel("资源栏", self, "LeftDock")
        left_dock.setObjectName("LeftDock")
        left_dock.add_content(self.create_control_library())
        self.addDockWidget(Qt.LeftDockWidgetArea, left_dock)
        
        # 创建数据可视化面板
        from .plot_widget import PlotWidget
        plot_dock = DockPanel("数据可视化", self, "PlotDock")
        plot_dock.setObjectName("PlotDock")
        plot_dock.setAllowedAreas(Qt.AllDockWidgetAreas)  # 支持所有停靠区域
        plot_widget = PlotWidget()
        plot_dock.add_content(plot_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, plot_dock)
        
        # 创建参数与执行监控面板
        property_dock = DockPanel("参数与执行监控", self, "PropertyDock")
        property_dock.setObjectName("PropertyDock")
        property_dock.setAllowedAreas(Qt.AllDockWidgetAreas)  # 支持所有停靠区域
        property_widget = QWidget()
        property_layout = QVBoxLayout()
        
        # 参数配置面板
        self.property_panel = PropertyPanel()
        property_layout.addWidget(self.property_panel)
        
        # 执行监控面板
        monitor_group = QGroupBox("执行监控")
        monitor_layout = QFormLayout()
        monitor_layout.addRow("流程名称:", QLabel("未命名"))
        monitor_layout.addRow("整体进度:", QProgressBar())
        monitor_layout.addRow("已执行节点数/总节点数:", QLabel("0/0"))
        monitor_layout.addRow("运行时间:", QLabel("00:00:00"))
        monitor_group.setLayout(monitor_layout)
        property_layout.addWidget(monitor_group)
        
        property_widget.setLayout(property_layout)
        property_dock.add_content(property_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, property_dock)
        
        # 注册工具窗口
        self.tool_window_manager.register_tool_window("LeftDock", left_dock)
        self.tool_window_manager.register_tool_window("PlotDock", plot_dock)
        self.tool_window_manager.register_tool_window("PropertyDock", property_dock)
        self.tool_window_manager.register_tool_window("LogDock", self.log_dock)
        # 底部状态栏已删除，不再注册
        # self.tool_window_manager.register_tool_window("BottomDock", self.bottom_dock)
        
        # 加载面板状态
        self.tool_window_manager.load_all_tool_window_states()
        
        # 创建侧边工具按钮栏
        self.create_side_toolbars()
    
    def create_control_library(self):
        """创建左侧控件库"""
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # 控件库标签页
        tab_widget = QTabWidget()
        
        # 控件库标签
        nodes_tab = QWidget()
        nodes_layout = QVBoxLayout()
        
        # 搜索框
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(10, 10, 10, 10)
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("搜索节点/设备/项目...")
        # 设置搜索框样式
        search_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #4285f4;
                outline: none;
            }
        """)
        search_layout.addWidget(search_edit)
        nodes_layout.addLayout(search_layout)
        
        # 树形控件
        tree_widget = QTreeWidget()
        tree_widget.setHeaderHidden(True)
        # 设置树形控件样式
        tree_widget.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: none;
            }
            QTreeWidget::item {
                height: 30px;
                padding-left: 5px;
            }
            QTreeWidget::item:hover {
                background-color: #f0f0f0;
            }
            QTreeWidget::item:selected {
                background-color: #e0e0e0;
            }
        """)
        
        # 设备控制节点
        device_control_item = QTreeWidgetItem(tree_widget, ["设备控制"])
        device_control_item.setExpanded(True)
        QTreeWidgetItem(device_control_item, ["USB_START/USB_END"])
        QTreeWidgetItem(device_control_item, ["SetLockInFreq"])
        QTreeWidgetItem(device_control_item, ["SetLockInPhase"])
        QTreeWidgetItem(device_control_item, ["SetLockInTimeCo"])
        
        # 数据采集节点
        data_acquisition_item = QTreeWidgetItem(tree_widget, ["数据采集"])
        data_acquisition_item.setExpanded(True)
        QTreeWidgetItem(data_acquisition_item, ["SetDataSampleRate"])
        QTreeWidgetItem(data_acquisition_item, ["get_max_slope"])
        
        # 信号处理节点
        signal_processing_item = QTreeWidgetItem(tree_widget, ["信号处理"])
        signal_processing_item.setExpanded(True)
        QTreeWidgetItem(signal_processing_item, ["lockin_res"])
        QTreeWidgetItem(signal_processing_item, ["log_insert_compile"])
        
        # 流程控制节点
        control_flow_item = QTreeWidgetItem(tree_widget, ["流程控制"])
        control_flow_item.setExpanded(True)
        QTreeWidgetItem(control_flow_item, ["循环_重复遍历"])
        QTreeWidgetItem(control_flow_item, ["add_row_data"])
        
        # 可视化节点
        visualization_item = QTreeWidgetItem(tree_widget, ["可视化"])
        visualization_item.setExpanded(True)
        QTreeWidgetItem(visualization_item, ["set_plot"])
        QTreeWidgetItem(visualization_item, ["add_data_line"])
        
        # 设备节点（从设备标签页合并）
        device_item = QTreeWidgetItem(tree_widget, ["设备"])
        device_item.setExpanded(True)
        QTreeWidgetItem(device_item, ["设备列表"])
        
        # 自定义节点
        custom_nodes_item = QTreeWidgetItem(tree_widget, ["自定义节点"])
        
        nodes_layout.addWidget(tree_widget)
        
        nodes_tab.setLayout(nodes_layout)
        
        # 设备标签
        devices_tab = QWidget()
        devices_layout = QVBoxLayout()
        devices_layout.addWidget(QLabel("设备列表"))
        devices_tab.setLayout(devices_layout)
        
        # 项目标签
        projects_tab = QWidget()
        projects_layout = QVBoxLayout()
        
        # 树形控件
        projects_tree = QTreeWidget()
        projects_tree.setHeaderHidden(True)
        # 设置树形控件样式
        projects_tree.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: none;
            }
            QTreeWidget::item {
                height: 30px;
                padding-left: 5px;
            }
            QTreeWidget::item:hover {
                background-color: #f0f0f0;
            }
            QTreeWidget::item:selected {
                background-color: #e0e0e0;
            }
        """)
        
        # 已有实验分类
        existing_experiments_item = QTreeWidgetItem(projects_tree, ["已有实验"])
        existing_experiments_item.setExpanded(True)
        # 原项目列表内容
        QTreeWidgetItem(existing_experiments_item, ["项目列表"])
        
        # 自定义实验分类
        custom_experiments_item = QTreeWidgetItem(projects_tree, ["自定义实验"])
        custom_experiments_item.setExpanded(True)
        
        projects_layout.addWidget(projects_tree)
        projects_tab.setLayout(projects_layout)
        
        # 设置标签页样式
        tab_widget.setStyleSheet("""
            QTabWidget {
                background-color: white;
                border: none;
            }
            QTabBar {
                background-color: white;
            }
            QTabBar::tab {
                padding: 8px 16px;
                margin-right: 2px;
                background-color: #f0f0f0;
                border: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #4285f4;
            }
        """)
        
        # 调整标签页顺序：项目（左）、控件库（右）
        tab_widget.addTab(projects_tab, "项目")
        tab_widget.addTab(nodes_tab, "控件库")
        # 注释掉设备标签页，将其内容合并到控件库
        # tab_widget.addTab(devices_tab, "设备")
        
        control_layout.addWidget(tab_widget)
        
        return control_widget
    
    def create_right_panel(self):
        """创建右侧功能面板"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 垂直分割器：上方数据可视化区，下方参数配置与执行监控区
        right_splitter = StyledSplitter(Qt.Vertical)
        
        # 上方：数据可视化区
        plot_widget = PlotWidget()
        
        # 下方：参数配置与执行监控区
        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)
        
        # 参数配置面板
        self.property_panel = PropertyPanel()
        bottom_layout.addWidget(self.property_panel)
        
        # 执行监控面板
        monitor_group = QGroupBox("执行监控")
        monitor_layout = QFormLayout()
        monitor_layout.addRow("流程名称:", QLabel("未命名"))
        monitor_layout.addRow("整体进度:", QProgressBar())
        monitor_layout.addRow("已执行节点数/总节点数:", QLabel("0/0"))
        monitor_layout.addRow("运行时间:", QLabel("00:00:00"))
        monitor_group.setLayout(monitor_layout)
        bottom_layout.addWidget(monitor_group)
        
        # 将数据可视化区和参数配置/执行监控区添加到垂直分割器
        right_splitter.addWidget(plot_widget)
        right_splitter.addWidget(bottom_panel)
        # 设置初始比例
        right_splitter.setSizes([300, 300])
        
        right_layout.addWidget(right_splitter)
        
        return right_widget
    
    def create_side_toolbars(self):
        """创建侧边工具按钮栏"""
        # 左侧工具按钮栏
        left_toolbar = QToolBar(self)
        left_toolbar.setOrientation(Qt.Vertical)
        left_toolbar.setFixedWidth(30)
        left_toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f5f5f5;
                border: none;
            }
            QToolButton {
                margin: 5px;
                padding: 10px;
                border-radius: 4px;
            }
            QToolButton:checked {
                background-color: #e0e0e0;
            }
        """)
        
        # 左侧资源栏按钮
        left_tool_button = QToolButton()
        left_tool_button.setText("资源栏")
        left_tool_button.setCheckable(True)
        left_tool_button.setChecked(self.tool_window_manager.get_tool_window("LeftDock").isVisible())
        left_tool_button.clicked.connect(lambda: self.tool_window_manager.toggle_tool_window("LeftDock"))
        left_toolbar.addWidget(left_tool_button)
        
        self.addToolBar(Qt.LeftToolBarArea, left_toolbar)
        
        # 右侧工具按钮栏
        right_toolbar = QToolBar(self)
        right_toolbar.setOrientation(Qt.Vertical)
        right_toolbar.setFixedWidth(30)
        right_toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f5f5f5;
                border: none;
            }
            QToolButton {
                margin: 5px;
                padding: 10px;
                border-radius: 4px;
            }
            QToolButton:checked {
                background-color: #e0e0e0;
            }
        """)
        
        # 数据可视化面板按钮
        plot_tool_button = QToolButton()
        plot_tool_button.setText("数据可视化")
        plot_tool_button.setCheckable(True)
        plot_tool_button.setChecked(self.tool_window_manager.get_tool_window("PlotDock").isVisible())
        plot_tool_button.clicked.connect(lambda: self.tool_window_manager.toggle_tool_window("PlotDock"))
        right_toolbar.addWidget(plot_tool_button)
        
        # 参数与执行监控面板按钮
        property_tool_button = QToolButton()
        property_tool_button.setText("参数监控")
        property_tool_button.setCheckable(True)
        property_tool_button.setChecked(self.tool_window_manager.get_tool_window("PropertyDock").isVisible())
        property_tool_button.clicked.connect(lambda: self.tool_window_manager.toggle_tool_window("PropertyDock"))
        right_toolbar.addWidget(property_tool_button)
        
        self.addToolBar(Qt.RightToolBarArea, right_toolbar)
        
        # 底部工具按钮栏 - 已删除，因为底部状态栏已被移除
        # bottom_toolbar = QToolBar(self)
        # bottom_toolbar.setOrientation(Qt.Horizontal)
        # bottom_toolbar.setFixedHeight(30)
        # bottom_toolbar.setStyleSheet("""
        #     QToolBar {
        #         background-color: #f5f5f5;
        #         border: none;
        #     }
        #     QToolButton {
        #         margin: 5px;
        #         padding: 5px 10px;
        #         border-radius: 4px;
        #     }
        #     QToolButton:checked {
        #         background-color: #e0e0e0;
        #     }
        # """)
        # 
        # # 底部状态栏按钮
        # bottom_tool_button = QToolButton()
        # bottom_tool_button.setText("状态栏")
        # bottom_tool_button.setCheckable(True)
        # bottom_tool_button.setChecked(self.tool_window_manager.get_tool_window("BottomDock").isVisible())
        # bottom_tool_button.clicked.connect(lambda: self.tool_window_manager.toggle_tool_window("BottomDock"))
        # bottom_toolbar.addWidget(bottom_tool_button)
        # 
        # self.addToolBar(Qt.BottomToolBarArea, bottom_toolbar)