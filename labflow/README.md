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
labflow/
├── app/               # 应用界面模块
├── core/              # 核心逻辑模块
├── nodes/             # 节点系统模块
├── devices/           # 设备抽象模块
├── workflow/          # 工作流系统模块
├── utils/             # 工具模块
├── docs/              # 文档
├── scripts/           # 脚本
├── requirements.txt   # 依赖项
├── setup.py           # 安装配置
└── README.md          # 项目说明
```

## 安装

### 方法一：使用 pip 安装

1. 克隆项目：
   ```bash
   git clone https://github.com/yourusername/labflow.git
   cd labflow
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 安装项目：
   ```bash
   pip install -e .
   ```

### 方法二：使用安装脚本

- Windows：运行 `scripts/install_windows.py`
- Linux：运行 `scripts/install_linux.py`

## 运行

```bash
labflow
```

或者直接运行：

```bash
python app/main.py
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

## 设备支持

- **仿真设备**：用于测试和开发
- **真实硬件**：支持通过串口、网络等方式连接的科研仪器

## 开发指南

### 编写自定义节点

1. 继承 `BaseNode` 类
2. 实现 `execute` 方法
3. 在 `nodes/__init__.py` 中注册节点

### 编写自定义设备

1. 继承 `BaseDevice` 类
2. 实现 `connect`、`disconnect`、`read`、`write` 方法
3. 在 `devices/__init__.py` 中注册设备

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License