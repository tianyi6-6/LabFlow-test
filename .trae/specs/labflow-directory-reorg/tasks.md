# Tasks

## 任务 1: 创建规范文档
- [ ] 创建 spec.md、tasks.md、checklist.md 规范文档

## 任务 2: 准备阶段 - 创建新目录骨架
- [ ] 创建 `experiment_flow_ui/` 顶层目录
- [ ] 创建 `experiment_flow_ui/setup/` 目录及占位文件
- [ ] 创建 `experiment_flow_ui/config/` 目录及基础文件
- [ ] 创建 `experiment_flow_ui/ui/analysis/` 子目录
- [ ] 创建 `experiment_flow_ui/core/` 目录
- [ ] 创建 `experiment_flow_ui/nodes/` 目录
- [ ] 创建 `experiment_flow_ui/devices/lockin_amplifier/` 目录
- [ ] 创建 `experiment_flow_ui/devices/microwave/` 目录
- [ ] 创建 `experiment_flow_ui/devices/laser/` 目录
- [ ] 创建 `experiment_flow_ui/devices/motor/` 目录
- [ ] 创建 `experiment_flow_ui/resources/drivers/` 目录
- [ ] 创建 `experiment_flow_ui/resources/icons/` 目录
- [ ] 创建 `experiment_flow_ui/resources/themes/` 目录
- [ ] 创建 `experiment_flow_ui/workflows/` 目录
- [ ] 创建 `experiment_flow_ui/docs/` 目录
- [ ] 创建 `experiment_flow_ui/utils/` 目录

## 任务 3: 迁移 app/ → ui/
- [ ] 迁移 app/main_window.py → ui/main_window.py
- [ ] 迁移 app/node_canvas.py → ui/canvas.py
- [ ] 迁移 app/property_panel.py → ui/property_panel.py
- [ ] 迁移 app/plot_widget.py → ui/plot_widget.py
- [ ] 迁移 app/log_panel.py → ui/log_panel.py
- [ ] 迁移 app/status_bar.py → ui/status_bar.py
- [ ] 迁移 app/dock_panel.py → ui/dock_panel.py
- [ ] 迁移 app/panel_state_manager.py → ui/panel_state_manager.py
- [ ] 迁移 app/styled_splitter.py → ui/styled_splitter.py
- [ ] 迁移 app/tool_window_manager.py → ui/tool_window_manager.py
- [ ] 迁移 app/toolbar.py → ui/toolbar.py
- [ ] 迁移 app/log_status_bar.py → ui/log_status_bar.py
- [ ] 迁移 app/styles.qss → ui/styles.qss
- [ ] 迁移 app/__init__.py → ui/__init__.py

## 任务 4: 创建 ui/ 新文件
- [ ] 创建 ui/node_widget.py（空骨架）
- [ ] 创建 ui/edge_widget.py（空骨架）
- [ ] 创建 ui/workflow_library.py（空骨架）
- [ ] 创建 ui/device_library.py（空骨架）
- [ ] 创建 ui/node_library.py（空骨架）
- [ ] 创建 ui/workflow_tab_panel.py（空骨架）
- [ ] 创建 ui/single_workflow_page.py（空骨架）
- [ ] 创建 ui/plot_manager.py（空骨架）
- [ ] 创建 ui/analysis_panel.py（空骨架）
- [ ] 创建 ui/menu_bar.py（空骨架）
- [ ] 迁移 core/device_manager.py → ui/device_manager.py
- [ ] 迁移 workflow/variable_manager.py → ui/variable_manager.py

## 任务 5: 迁移 core/ 文件
- [ ] 迁移 core/graph_executor.py → core/graph_executor.py（保持）
- [ ] 迁移 core/__init__.py → core/__init__.py（保持）
- [ ] 创建 core/base_workflow.py（空骨架）
- [ ] 迁移 nodes/base_node.py → core/base_node.py
- [ ] 迁移 devices/base_device.py → core/base_device.py
- [ ] 创建 core/registry.py（空骨架）
- [ ] 创建 core/execution_context.py（空骨架）
- [ ] 创建 core/exception_handler.py（空骨架）
- [ ] 创建 core/data_router.py（空骨架）
- [ ] 创建 core/variables.py（空骨架）

## 任务 6: 迁移和重构 nodes/ 文件
- [ ] 迁移 nodes/input_output.py → nodes/input_output.py（保持）
- [ ] 迁移 nodes/device_config.py → nodes/configure_device.py
- [ ] 迁移 nodes/device_control.py → nodes/configure_device.py（合并）
- [ ] 迁移 nodes/data_read.py → nodes/data_read.py（保持）
- [ ] 迁移 nodes/data_acquisition.py → nodes/data_read.py（合并）
- [ ] 迁移 nodes/data_process.py → nodes/data_process.py（保持）
- [ ] 迁移 nodes/signal_processing.py → nodes/data_process.py（合并）
- [ ] 迁移 nodes/visualization.py → nodes/visualization.py（保持）
- [ ] 创建 nodes/debug.py（空骨架）
- [ ] 迁移 nodes/custom_nodes.py → nodes/composite_workflow.py
- [ ] 迁移 nodes/control_flow.py → nodes/control_flow.py（保持）
- [ ] 创建 nodes/__init__.py（空骨架，仅自动导入）
- [ ] 删除 nodes/custom_nodes.py（已迁移）
- [ ] 删除 nodes/data_acquisition.py（已迁移）
- [ ] 删除 nodes/signal_processing.py（已迁移）
- [ ] 删除 nodes/device_control.py（已迁移）

## 任务 7: 重构 devices/ 目录
- [ ] 创建 devices/lockin_amplifier/__init__.py（空骨架）
- [ ] 创建 devices/lockin_amplifier/lockin_simulator.py（占位）
- [ ] 创建 devices/lockin_amplifier/lockin_device.py（占位）
- [ ] 创建 devices/microwave/__init__.py（空骨架）
- [ ] 创建 devices/microwave/microwave_simulator.py（占位）
- [ ] 创建 devices/microwave/microwave_device.py（占位）
- [ ] 创建 devices/laser/__init__.py（空骨架）
- [ ] 创建 devices/laser/laser_simulator.py（占位）
- [ ] 创建 devices/laser/laser_device.py（占位）
- [ ] 创建 devices/motor/__init__.py（空骨架）
- [ ] 创建 devices/motor/motor_simulator.py（占位）
- [ ] 创建 devices/motor/motor_device.py（占位）

## 任务 8: 迁移设备文件到新结构
- [ ] 迁移 devices/simulated/simulated_device.py → 各类 *_simulator.py
- [ ] 迁移 devices/network/network_device.py → 兼容性保留或各类 device.py
- [ ] 迁移 devices/serial/serial_device.py → 兼容性保留或各类 device.py
- [ ] 迁移 devices/usb/usb_device.py → 兼容性保留或各类 device.py

## 任务 9: 创建 utils/ 新文件和补充
- [ ] 创建 utils/file_io.py（空骨架）
- [ ] 创建 utils/logger.py（空骨架）
- [ ] 保留 utils/__init__.py
- [ ] 保留 utils/config.py
- [ ] 保留 utils/data_structures.py
- [ ] 保留 utils/helpers.py

## 任务 10: 迁移 workflow/ 内容
- [ ] 迁移 workflow/persistence.py → experiment_flow_ui/（根目录或 utils/）
- [ ] 迁移 workflow/workflow.py → core/base_workflow.py
- [ ] 删除 workflow/variable_manager.py（已迁移至 ui/variable_manager.py）

## 任务 11: 迁移根目录文件
- [ ] 迁移 labflow/main.py → experiment_flow_ui/main.py
- [ ] 迁移 labflow/readme.md → experiment_flow_ui/readme.md
- [ ] 迁移 labflow/requirements.txt → experiment_flow_ui/requirements.txt
- [ ] 迁移 labflow/__main__.py → experiment_flow_ui/__main__.py
- [ ] 迁移 labflow/run.py → experiment_flow_ui/run.py
- [ ] 迁移 labflow/setup.py → experiment_flow_ui/setup.py

## 任务 12: 清理和生成文档
- [ ] 删除空的旧目录 labflow/（确认所有文件已迁移）
- [ ] 生成 MIGRATION.md 文档
- [ ] 验证所有迁移文件位置正确

# Task Dependencies
- 任务 2 必须在任务 3-11 之前完成（创建目录骨架）
- 任务 3、4、5、6、7、8、9、10、11 可以并行执行（相互独立）
- 任务 12 必须在所有其他任务完成后执行
