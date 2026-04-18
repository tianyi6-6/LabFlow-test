# Checklist

## 目录骨架创建
- [ ] experiment_flow_ui/ 顶层目录已创建
- [ ] experiment_flow_ui/setup/ 目录及占位文件已创建
- [ ] experiment_flow_ui/config/ 目录及基础文件已创建
- [ ] experiment_flow_ui/ui/analysis/ 子目录已创建
- [ ] experiment_flow_ui/core/ 目录已创建
- [ ] experiment_flow_ui/nodes/ 目录已创建
- [ ] experiment_flow_ui/devices/lockin_amplifier/ 目录已创建
- [ ] experiment_flow_ui/devices/microwave/ 目录已创建
- [ ] experiment_flow_ui/devices/laser/ 目录已创建
- [ ] experiment_flow_ui/devices/motor/ 目录已创建
- [ ] experiment_flow_ui/resources/drivers/ 目录已创建
- [ ] experiment_flow_ui/resources/icons/ 目录已创建
- [ ] experiment_flow_ui/resources/themes/ 目录已创建
- [ ] experiment_flow_ui/workflows/ 目录已创建
- [ ] experiment_flow_ui/docs/ 目录已创建
- [ ] experiment_flow_ui/utils/ 目录已创建

## ui/ 目录完整性
- [ ] ui/main_window.py 存在
- [ ] ui/canvas.py 存在
- [ ] ui/node_widget.py 存在
- [ ] ui/edge_widget.py 存在
- [ ] ui/property_panel.py 存在
- [ ] ui/workflow_library.py 存在
- [ ] ui/device_library.py 存在
- [ ] ui/device_manager.py 存在
- [ ] ui/node_library.py 存在
- [ ] ui/workflow_tab_panel.py 存在
- [ ] ui/single_workflow_page.py 存在
- [ ] ui/variable_manager.py 存在
- [ ] ui/plot_manager.py 存在
- [ ] ui/plot_widget.py 存在
- [ ] ui/analysis_panel.py 存在
- [ ] ui/log_panel.py 存在
- [ ] ui/menu_bar.py 存在
- [ ] ui/status_bar.py 存在
- [ ] ui/analysis/ 子目录存在
- [ ] ui/dock_panel.py 存在
- [ ] ui/panel_state_manager.py 存在
- [ ] ui/styled_splitter.py 存在
- [ ] ui/tool_window_manager.py 存在
- [ ] ui/toolbar.py 存在
- [ ] ui/log_status_bar.py 存在
- [ ] ui/styles.qss 存在
- [ ] ui/__init__.py 存在

## core/ 目录完整性
- [ ] core/graph_executor.py 存在
- [ ] core/base_workflow.py 存在
- [ ] core/base_node.py 存在
- [ ] core/base_device.py 存在
- [ ] core/registry.py 存在
- [ ] core/execution_context.py 存在
- [ ] core/exception_handler.py 存在
- [ ] core/data_router.py 存在
- [ ] core/variables.py 存在
- [ ] core/__init__.py 存在

## nodes/ 目录完整性
- [ ] nodes/input_output.py 存在
- [ ] nodes/configure_device.py 存在
- [ ] nodes/data_read.py 存在
- [ ] nodes/data_process.py 存在
- [ ] nodes/visualization.py 存在
- [ ] nodes/debug.py 存在
- [ ] nodes/composite_workflow.py 存在
- [ ] nodes/control_flow.py 存在
- [ ] nodes/__init__.py 存在（空骨架）

## devices/ 目录完整性
- [ ] devices/lockin_amplifier/__init__.py 存在
- [ ] devices/lockin_amplifier/lockin_simulator.py 存在
- [ ] devices/lockin_amplifier/lockin_device.py 存在
- [ ] devices/microwave/__init__.py 存在
- [ ] devices/microwave/microwave_simulator.py 存在
- [ ] devices/microwave/microwave_device.py 存在
- [ ] devices/laser/__init__.py 存在
- [ ] devices/laser/laser_simulator.py 存在
- [ ] devices/laser/laser_device.py 存在
- [ ] devices/motor/__init__.py 存在
- [ ] devices/motor/motor_simulator.py 存在
- [ ] devices/motor/motor_device.py 存在

## 根目录和配置文件
- [ ] experiment_flow_ui/main.py 存在
- [ ] experiment_flow_ui/readme.md 存在
- [ ] experiment_flow_ui/requirements.txt 存在
- [ ] experiment_flow_ui/setup/system_config.ini 存在
- [ ] experiment_flow_ui/setup/device_config.ini 存在
- [ ] experiment_flow_ui/setup/setup_windows.bat 存在
- [ ] experiment_flow_ui/setup/setup_linux.sh 存在
- [ ] experiment_flow_ui/setup/windows_runtime.zip 占位存在
- [ ] experiment_flow_ui/setup/linux_runtime.zip 占位存在
- [ ] experiment_flow_ui/setup/pyenv.zip 占位存在
- [ ] experiment_flow_ui/config/config_loader.py 存在
- [ ] experiment_flow_ui/utils/file_io.py 存在
- [ ] experiment_flow_ui/utils/logger.py 存在
- [ ] experiment_flow_ui/resources/drivers/ 占位存在
- [ ] experiment_flow_ui/resources/icons/ 占位存在
- [ ] experiment_flow_ui/resources/themes/ 占位存在
- [ ] experiment_flow_ui/workflows/ 目录存在
- [ ] experiment_flow_ui/docs/ 目录存在

## MIGRATION.md 文档
- [ ] MIGRATION.md 已生成
- [ ] MIGRATION.md 包含所有旧文件到新文件的映射

## Git History 保留
- [ ] 使用 git mv 进行文件迁移
- [ ] 旧 labflow/ 目录已删除或重命名
