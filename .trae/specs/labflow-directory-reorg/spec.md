# LabFlow 目录结构重构规范

## Why
根据需求文档第三章 3.1 节程序架构要求，现有 LabFlow 仓库的目录结构与文档规定不一致，需要进行重构以完全对齐文档规范，同时尽可能无损迁移旧代码并保留 git history。

## What Changes

### 顶层目录调整
- `labflow/` → `experiment_flow_ui/`（或保留 LabFlow/ 但内部完全对齐文档）
- 保留 `main.py`、`readme.md`、`requirements.txt`

### 新增 setup/ 目录
- `setup/setup_windows.bat`
- `setup/setup_linux.sh`
- `setup/windows_runtime.zip`（占位）
- `setup/linux_runtime.zip`（占位）
- `setup/pyenv.zip`（占位）

### 新增 config/ 目录
- `config/system_config.ini`
- `config/device_config.ini`
- `config/config_loader.py`

### ui/ 目录重构（按文档 3.1.2 节）
原有 `app/` 目录重命名为 `ui/`，并补充缺失文件：
- `ui/main_window.py`（原有 main_window.py）
- `ui/canvas.py`（原有 node_canvas.py）
- `ui/node_widget.py`（新增）
- `ui/edge_widget.py`（新增）
- `ui/property_panel.py`（原有 property_panel.py）
- `ui/workflow_library.py`（新增）
- `ui/device_library.py`（新增）
- `ui/device_manager.py`（原有 core/device_manager.py 迁移）
- `ui/node_library.py`（新增）
- `ui/workflow_tab_panel.py`（新增）
- `ui/single_workflow_page.py`（新增）
- `ui/variable_manager.py`（原有 workflow/variable_manager.py 迁移）
- `ui/plot_manager.py`（新增）
- `ui/plot_widget.py`（原有 plot_widget.py）
- `ui/analysis_panel.py`（新增）
- `ui/log_panel.py`（原有 log_panel.py）
- `ui/menu_bar.py`（新增）
- `ui/status_bar.py`（原有 status_bar.py）
- `ui/analysis/` 子目录（新增）

其他 UI 相关文件：
- `ui/dock_panel.py`（原有 dock_panel.py）
- `ui/panel_state_manager.py`（原有 panel_state_manager.py）
- `ui/styled_splitter.py`（原有 styled_splitter.py）
- `ui/tool_window_manager.py`（原有 tool_window_manager.py）
- `ui/toolbar.py`（原有 toolbar.py）
- `ui/log_status_bar.py`（原有 log_status_bar.py）
- `ui/styles.qss`（原有 styles.qss）

### core/ 目录重构（按文档 3.1.3 节）
- `core/graph_executor.py`（原有）
- `core/base_workflow.py`（新增）
- `core/base_node.py`（原有 nodes/base_node.py 迁移）
- `core/base_device.py`（原有 devices/base_device.py 迁移）
- `core/registry.py`（新增）
- `core/execution_context.py`（新增）
- `core/exception_handler.py`（新增）
- `core/data_router.py`（新增）
- `core/variables.py`（新增）

### nodes/ 目录重构（按文档 3.1 节）
- `nodes/input_output.py`（原有 input_output.py）
- `nodes/configure_device.py`（原有 device_config.py 重命名）
- `nodes/data_read.py`（原有 data_read.py）
- `nodes/data_process.py`（原有 data_process.py）
- `nodes/visualization.py`（原有 visualization.py）
- `nodes/debug.py`（新增）
- `nodes/composite_workflow.py`（原有 custom_nodes.py 或新增）
- `nodes/control_flow.py`（原有 control_flow.py）
- `nodes/__init__.py`（空骨架，自动注册逻辑由 Spec 1 实现）

注：以下旧文件需迁移或废弃：
- `nodes/device_config.py` → `nodes/configure_device.py`
- `nodes/device_control.py` → `nodes/configure_device.py` 或 `nodes/debug.py`
- `nodes/data_acquisition.py` → `nodes/data_read.py`
- `nodes/signal_processing.py` → `nodes/data_process.py`
- `nodes/custom_nodes.py` → `nodes/composite_workflow.py`

### devices/ 目录重构（按设备大类分层）
原有 `devices/` 下的网络/串口/USB/模拟设备结构重组为：
- `devices/lockin_amplifier/__init__.py`（空骨架）
- `devices/lockin_amplifier/lockin_simulator.py`（新增占位）
- `devices/lockin_amplifier/lockin_device.py`（新增占位真实驱动）
- `devices/microwave/__init__.py`（空骨架）
- `devices/microwave/microwave_simulator.py`（新增占位）
- `devices/microwave/microwave_device.py`（新增占位真实驱动）
- `devices/laser/__init__.py`（空骨架）
- `devices/laser/laser_simulator.py`（新增占位）
- `devices/laser/laser_device.py`（新增占位真实驱动）
- `devices/motor/__init__.py`（空骨架）
- `devices/motor/motor_simulator.py`（新增占位）
- `devices/motor/motor_device.py`（新增占位真实驱动）

原有设备文件迁移：
- `devices/base_device.py` → `core/base_device.py`
- `devices/network/network_device.py` → `devices/` 各类下或保留兼容性
- `devices/serial/serial_device.py` → `devices/` 各类下或保留兼容性
- `devices/usb/usb_device.py` → `devices/` 各类下或保留兼容性
- `devices/simulated/simulated_device.py` → 各类的 simulator.py

### 新增 resources/ 目录
- `resources/drivers/`（占位）
- `resources/icons/`（占位）
- `resources/themes/`（占位）

### 新增 workflows/ 目录
- `workflows/` 放置示例 JSON 文件

### 新增 docs/ 目录
- `docs/`（占位）

### 新增 utils/ 文件补充
- `utils/file_io.py`（新增）
- `utils/logger.py`（新增）

### 根目录文件
- `main.py`（保留）
- `readme.md`（保留）
- `requirements.txt`（保留）

## Impact

### 受影响的规范
- Spec 1（节点自动注册系统）依赖于 `nodes/__init__.py` 骨架
- Spec 1（设备自动注册系统）依赖于 `devices/*/__init__.py` 骨架

### 受影响的代码
关键迁移文件映射：
| 旧路径 | 新路径 |
|--------|--------|
| `labflow/app/main_window.py` | `experiment_flow_ui/ui/main_window.py` |
| `labflow/app/node_canvas.py` | `experiment_flow_ui/ui/canvas.py` |
| `labflow/app/property_panel.py` | `experiment_flow_ui/ui/property_panel.py` |
| `labflow/app/plot_widget.py` | `experiment_flow_ui/ui/plot_widget.py` |
| `labflow/app/log_panel.py` | `experiment_flow_ui/ui/log_panel.py` |
| `labflow/app/status_bar.py` | `experiment_flow_ui/ui/status_bar.py` |
| `labflow/core/device_manager.py` | `experiment_flow_ui/ui/device_manager.py` |
| `labflow/workflow/variable_manager.py` | `experiment_flow_ui/ui/variable_manager.py` |
| `labflow/nodes/base_node.py` | `experiment_flow_ui/core/base_node.py` |
| `labflow/devices/base_device.py` | `experiment_flow_ui/core/base_device.py` |
| `labflow/devices/simulated/simulated_device.py` | `experiment_flow_ui/devices/*/*_simulator.py` |

## 约束条件
- 旧代码以尽可能无损的方式迁移到对应新位置
- 重命名时使用 `git mv` 保留 git history
- 所有 `__init__.py` 在本次仅搭空骨架，具体注册逻辑由 Spec 1 实现
- 输出一份 `MIGRATION.md` 说明每个旧文件迁移到的新位置

## ADDED Requirements

### Requirement: 目录结构完全对齐文档
系统 SHALL 按照 `可视化工作流软件需求文档-V0.1.pdf` 第三章 3.1 节完全重构目录结构

### Requirement: Git History 保留
系统 SHALL 使用 `git mv` 命令进行文件和目录重命名，以保留 git history

### Requirement: __init__.py 骨架
所有 `__init__.py` 文件 SHALL 仅包含空骨架，不含具体注册逻辑

### Requirement: MIGRATION.md 文档
系统 SHALL 生成一份 `MIGRATION.md` 文档，详细说明每个旧文件迁移到的新位置

## REMOVED Requirements

### Requirement: 旧目录结构
**Reason**: 旧目录结构与文档规范不一致，需要按照文档重新组织
**Migration**: 所有文件迁移到新位置后，删除旧目录
