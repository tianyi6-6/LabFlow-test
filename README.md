# LabFlow 科研仪器可视化工作流系统

LabFlow 是一款类似 ComfyUI 的科研仪器可视化工作流桌面软件，面向实验室仪器自动化控制场景，提供图形化拖拽式工作流编排、拓扑执行、设备控制、实时数据可视化、工作流持久化等核心能力，替代传统脚本式仪器控制，降低科研人员开发门槛。

## 功能特性

- **可视化工作流编排**：提供无限缩放/平移的图形化画布，支持节点拖拽、复制、删除、对齐，支持节点自定义样式，端口支持连线和类型校验
- **节点系统**：支持设备控制、数据采集、信号处理、流程控制、可视化、自定义节点等6大类节点
- **工作流拓扑执行**：自动解析画布节点连线，生成有向无环图（DAG），按拓扑顺序执行节点，支持单步执行、连续执行、暂停/终止执行
- **设备控制与通信**：支持多设备同时连接，状态实时显示，设备通信层抽象，支持USB、串口、网口等协议扩展
- **实时数据可视化**：支持折线图、散点图等实时绘图，数据流式更新，支持坐标拾取
- **工作流持久化**：支持工作流保存、加载和导出，支持JSON格式、可执行脚本、实验报告
- **跨平台支持**：支持Windows、Linux、macOS平台

## 技术栈

- Python 3.10+
- PySide6（GUI）
- NetworkX（拓扑排序）
- NumPy/Pandas（数据处理）
- Matplotlib/PyQtGraph（绘图）
- pyserial（设备通信）
- asyncio（异步执行）

## 安装与运行

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourusername/labflow.git
cd labflow

# 安装依赖
pip install -r labflow/requirements.txt
```

### 运行应用

```bash
# 运行应用
python main.py
```

## 项目结构

```
labflow/
├── app/             # 应用界面模块
│   ├── main.py      # 主应用入口
│   ├── main_window.py # 主窗口
│   ├── node_canvas.py # 节点画布
│   ├── property_panel.py # 属性面板
│   ├── plot_panel.py # 绘图面板
│   ├── log_panel.py # 日志面板
│   └── status_bar.py # 状态栏
├── core/            # 核心逻辑模块
│   ├── graph_executor.py # 图执行器
│   ├── device_manager.py # 设备管理器
│   └── logger.py    # 日志系统
├── nodes/           # 节点模块
│   ├── base_node.py # 基础节点
│   ├── device_control.py # 设备控制节点
│   ├── data_acquisition.py # 数据采集节点
│   ├── signal_processing.py # 信号处理节点
│   ├── control_flow.py # 控制流节点
│   ├── visualization.py # 可视化节点
│   └── custom_nodes.py # 自定义节点
├── devices/         # 设备模块
│   ├── base_device.py # 基础设备
│   ├── simulated/   # 仿真设备
│   ├── usb/         # USB设备
│   ├── serial/      # 串口设备
│   └── network/     # 网络设备
├── workflow/        # 工作流模块
│   ├── workflow.py  # 工作流
│   ├── persistence.py # 工作流持久化
│   └── variable_manager.py # 变量管理器
├── utils/           # 工具模块
│   ├── data_structures.py # 数据结构
│   ├── config.py    # 配置
│   └── helpers.py   # 辅助函数
├── requirements.txt # 依赖项
└── main.py          # 主应用入口
```

## 使用指南

1. **添加节点**：从左侧控件库中拖拽节点到中央画布
2. **连接节点**：从一个节点的输出端口拖拽到另一个节点的输入端口
3. **配置节点**：选中节点后，在右侧属性面板中修改节点参数
4. **执行工作流**：点击顶部工具栏的「运行」按钮执行工作流
5. **查看日志**：在右侧日志面板中查看执行日志
6. **查看数据**：在右侧绘图面板中查看实时数据可视化
7. **保存工作流**：点击顶部工具栏的「保存」按钮保存工作流
8. **导出工作流**：点击顶部工具栏的「导出」按钮导出工作流

## 示例节点

### 设备控制类
- `SetLockInFreq`：锁相放大器频率设置
- `SetLockInPhase`：锁相放大器相位设置
- `SetLockInTimeCo`：锁相放大器时间常数设置
- `USB_START`：USB设备启动
- `USB_END`：USB设备结束

### 数据采集类
- `SetDataSampleRate`：设置数据采样率
- `get_max_slope`：获取最大斜率

### 信号处理类
- `lockin_res`：锁相放大器信号处理
- `log_insert_compile`：日志插入编译

### 流程控制类
- `LoopRepeat`：循环重复遍历
- `add_row_data`：添加行数据

### 可视化类
- `set_plot`：设置绘图
- `add_data_line`：添加数据线条

## 开发指南

### 添加自定义节点

1. 在 `labflow/nodes/` 目录下创建新的节点文件
2. 继承 `BaseNode` 类并实现 `execute` 方法
3. 在 `labflow/nodes/__init__.py` 中添加新节点的导入

### 添加设备驱动

1. 在 `labflow/devices/` 目录下创建新的设备目录
2. 继承 `BaseDevice` 类并实现 `connect`、`disconnect`、`read`、`write` 方法
3. 在 `labflow/devices/__init__.py` 中添加新设备的导入

## 许可证

MIT License

## 联系方式

如果您有任何问题或建议，请通过以下方式联系我们：

- 邮箱：contact@labflow.com
- GitHub：https://github.com/yourusername/labflow