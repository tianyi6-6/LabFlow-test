# LabFlow 科研仪器工作流系统

## 概述

LabFlow 是一款类似 ComfyUI 的科研仪器可视化工作流桌面软件，基于 PySide6 构建本地 GUI，支持节点拖拽、连线、拓扑执行、设备控制、流式绘图、工作流保存加载和导出。

## 功能特点

- **拖拽式节点工作流**：通过直观的节点画布界面设计和执行复杂的科研工作流
- **DAG 拓扑执行**：支持并行子图执行，提高工作流执行效率
- **设备抽象接口**：统一的设备管理接口，支持仿真设备和真实硬件
- **流式数据可视化**：实时数据采集和可视化分析
- **工作流持久化**：支持工作流的保存、加载和导出
- **跨平台支持**：可在 Windows、Linux 和树莓派 4B 上运行
- **设备类别支持**：锁相放大器、微波设备、激光设备、电机设备
- **调试功能**：内置调试节点和日志面板，方便工作流调试
- **复合工作流**：支持嵌套工作流，提高工作流的模块化和复用性

## 技术栈

- Python 3.10+
- PySide6（GUI 框架）
- QGraphicsScene/View（节点画布）
- pyqtgraph（数据可视化）
- networkx（图论分析）
- numpy（数据处理）
- pyserial（设备通信）
- asyncio（异步执行）

## 项目结构

```
experiment_flow_ui/
├── config/           # 配置文件
│   ├── system_config.ini     # 系统配置文件
│   ├── device_config.ini     # 设备配置文件
│   └── config_loader.py      # 配置加载器
├── core/             # 核心模块
│   ├── graph_executor.py      # 工作流图执行器
│   ├── base_workflow.py       # 工作流基类
│   ├── base_node.py           # 节点基类
│   ├── base_device.py         # 设备基类
│   ├── registry.py            # 节点和设备注册表
│   ├── execution_context.py   # 执行上下文
│   ├── exception_handler.py   # 异常处理器
│   ├── data_router.py         # 数据路由器
│   └── variables.py           # 变量管理
├── devices/          # 设备驱动（按类别组织）
│   ├── lockin_amplifier/      # 锁相放大器设备
│   │   ├── __init__.py        # 包初始化文件
│   │   ├── lockin_device.py   # 锁相放大器设备类
│   │   └── lockin_simulator.py # 锁相放大器仿真器
│   ├── microwave/             # 微波设备
│   │   ├── __init__.py        # 包初始化文件
│   │   ├── microwave_device.py # 微波设备类
│   │   └── microwave_simulator.py # 微波设备仿真器
│   ├── laser/                 # 激光设备
│   │   ├── __init__.py        # 包初始化文件
│   │   ├── laser_device.py    # 激光设备类
│   │   └── laser_simulator.py # 激光设备仿真器
│   ├── motor/                 # 电机设备
│   │   ├── __init__.py        # 包初始化文件
│   │   ├── motor_device.py    # 电机设备类
│   │   └── motor_simulator.py # 电机设备仿真器
│   └── compatibility/         # 兼容性设备
│       ├── __init__.py        # 包初始化文件
│       ├── network_device.py  # 网络设备类
│       ├── serial_device.py   # 串口设备类
│       └── usb_device.py      # USB设备类
├── docs/             # 文档
├── nodes/            # 节点定义
│   ├── input_output.py        # 输入输出节点
│   ├── configure_device.py    # 设备配置节点
│   ├── data_read.py           # 数据读取节点
│   ├── data_process.py        # 数据处理节点
│   ├── visualization.py       # 可视化节点
│   ├── debug.py               # 调试节点
│   ├── composite_workflow.py  # 复合工作流节点
│   ├── control_flow.py        # 控制流节点
│   └── __init__.py            # 包初始化文件
├── resources/        # 资源文件
│   ├── drivers/               # 设备驱动
│   │   └── .gitkeep           # 保持目录结构
│   ├── icons/                 # 图标
│   │   └── .gitkeep           # 保持目录结构
│   └── themes/                # 主题
│       └── .gitkeep           # 保持目录结构
├── setup/            # 安装脚本
│   ├── setup_windows.bat      # Windows安装脚本
│   └── setup_linux.sh         # Linux安装脚本
├── ui/               # 用户界面
│   ├── main_window.py         # 主窗口
│   ├── canvas.py              # 节点画布
│   ├── node_widget.py         # 节点部件
│   ├── edge_widget.py         # 边部件
│   ├── property_panel.py      # 属性面板
│   ├── workflow_library.py    # 工作流库
│   ├── device_library.py      # 设备库
│   ├── device_manager.py      # 设备管理器
│   ├── node_library.py        # 节点库
│   ├── workflow_tab_panel.py  # 工作流标签面板
│   ├── single_workflow_page.py # 单个工作流页面
│   ├── variable_manager.py    # 变量管理器
│   ├── plot_manager.py        # 绘图管理器
│   ├── plot_widget.py         # 绘图部件
│   ├── analysis_panel.py      # 分析面板
│   ├── log_panel.py           # 日志面板
│   ├── menu_bar.py            # 菜单栏
│   ├── status_bar.py          # 状态栏
│   ├── analysis/              # 分析相关
│   ├── dock_panel.py          # 停靠面板
│   ├── log_status_bar.py      # 日志状态栏
│   ├── main.py                # UI主入口
│   ├── plot_panel.py          # 绘图面板
│   ├── toolbar.py             # 工具栏
│   ├── tool_window_manager.py # 工具窗口管理器
│   ├── styled_splitter.py     # 样式分割器
│   └── panel_state_manager.py # 面板状态管理器
├── utils/            # 工具函数
│   ├── file_io.py             # 文件IO操作
│   ├── logger.py              # 日志工具
│   ├── config.py              # 配置工具
│   ├── data_structures.py     # 数据结构
│   ├── helpers.py             # 辅助函数
│   └── persistence.py         # 持久化工具
├── workflows/        # 工作流示例
├── main.py           # 主入口文件
├── README.md         # 项目说明
├── requirements.txt  # 依赖项
├── run.py            # 运行脚本
├── setup.py          # 安装配置
├── __init__.py       # 包初始化文件
└── __main__.py       # 包执行文件
```

## 安装

### 方法一：使用 pip 安装

1. 克隆项目：
   ```bash
   git clone https://github.com/tianyi6-6/LabFlow-test.git
   cd LabFlow-test/experiment_flow_ui
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 方法二：使用安装脚本

- Windows：运行 `setup/setup_windows.bat`
- Linux：运行 `setup/setup_linux.sh`

## 运行

```bash
python run.py
```

或者直接运行：

```bash
python main.py
```

## 使用指南

1. **添加节点**：右键点击画布，选择"添加节点"，从列表中选择节点类型
2. **连接节点**：从一个节点的输出端口拖拽到另一个节点的输入端口
3. **配置节点**：选中节点后，在右侧属性面板中修改节点属性
4. **执行工作流**：点击工具栏中的"执行工作流"按钮
5. **保存/加载工作流**：使用工具栏中的"保存工作流"和"加载工作流"按钮

## 支持的节点类型

- **输入输出节点**：数据输入和输出
- **设备配置节点**：设备连接和配置
- **数据读取节点**：从设备读取数据
- **数据处理节点**：数据过滤、转换等处理
- **可视化节点**：数据可视化
- **控制流节点**：条件执行和控制逻辑
- **调试节点**：工作流调试
- **复合工作流节点**：嵌套工作流

## 设备支持

- **仿真设备**：用于测试和开发
- **真实硬件**：支持通过串口、网络等方式连接的科研仪器
- **设备类别**：锁相放大器、微波设备、激光设备、电机设备

## 开发指南

### 编写自定义节点

1. 继承 `BaseNode` 类
2. 实现 `execute` 方法
3. 在 `nodes/__init__.py` 中注册节点

### 编写自定义设备

1. 继承 `BaseDevice` 类
2. 实现 `connect`、`disconnect`、`read`、`write` 方法
3. 在 `devices/[设备类别]/__init__.py` 中注册设备

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License