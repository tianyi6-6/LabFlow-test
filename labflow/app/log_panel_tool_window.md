# LabFlow 底部日志面板工具窗口使用说明

## 概述

本文件提供了如何使用和调整 LabFlow 底部日志面板工具窗口的详细说明，包括如何修改日志面板默认高度、默认停靠位置、快捷键等参数。

## 日志面板的基本使用

### 显示/隐藏日志面板

有三种方式可以显示/隐藏日志面板：

1. **底部侧边工具按钮**：点击主窗口底部边缘的「日志」按钮
2. **顶部视图菜单**：通过「视图 → 工具窗口 → 日志」菜单项
3. **快捷键**：按下 `Ctrl+3` 快捷键

### 日志面板的停靠与分离

- **拖拽分离**：拖拽日志面板的标题栏，可以将其分离为独立的浮动窗口
- **重新停靠**：拖拽浮动窗口的标题栏到主窗口的左、右、上、下四个边缘，可以重新停靠日志面板
- **调整大小**：拖拽日志面板的边缘，可以调整其大小

### 日志系统功能

日志面板包含以下功能：

- **日志标签页**：包括「全部」、「信息」、「警告」、「错误」四个标签页
- **搜索框**：可以搜索日志内容
- **导出按钮**：可以导出日志到文件
- **清空按钮**：可以清空所有日志

## 如何修改日志面板默认设置

### 修改日志面板默认高度

**修改方法**：
1. 打开 `labflow/app/tool_window_manager.py` 文件
2. 在 `default_layouts` 字典中，为 `LogPanel` 添加 `default_size` 键，设置默认高度

```python
self.default_layouts = {
    # 其他面板设置...
    "LogPanel": {
        "area": Qt.BottomDockWidgetArea,
        "visible": True,
        "geometry": None,
        "default_size": 200  # 默认高度为 200px
    }
}
```

### 修改日志面板默认停靠位置

**修改方法**：
1. 打开 `labflow/app/tool_window_manager.py` 文件
2. 在 `default_layouts` 字典中，修改 `LogPanel` 的 `area` 值

```python
self.default_layouts = {
    # 其他面板设置...
    "LogPanel": {
        "area": Qt.BottomDockWidgetArea,  # 默认停靠在底部
        "visible": True,
        "geometry": None
    }
}
```

**可选的停靠位置**：
- `Qt.LeftDockWidgetArea`：左侧
- `Qt.RightDockWidgetArea`：右侧
- `Qt.TopDockWidgetArea`：顶部
- `Qt.BottomDockWidgetArea`：底部

### 修改日志面板快捷键

**修改方法**：
1. 打开 `labflow/app/main_window.py` 文件
2. 在 `create_menu_bar` 方法中，修改日志面板菜单项的快捷键

```python
# 日志面板菜单项
log_dock_action = QAction("日志", self)
log_dock_action.setCheckable(True)
log_dock_action.setChecked(self.tool_window_manager.get_tool_window("LogPanel").isVisible())
log_dock_action.triggered.connect(lambda: self.tool_window_manager.toggle_tool_window("LogPanel"))
# 添加快捷键
log_dock_action.setShortcut("Ctrl+3")  # 修改这里的快捷键
tool_windows_menu.addAction(log_dock_action)
```

### 重置窗口布局

如果需要将所有面板恢复到默认布局，可以通过以下方式：

1. 点击「视图 → 重置窗口布局」菜单项
2. 所有面板（包括日志面板）会恢复到默认位置和大小

## 状态持久化

- 程序退出时会自动保存日志面板的显示/隐藏状态、停靠位置、大小
- 程序启动时会自动恢复上述状态
- 无需手动保存配置

## 注意事项

1. 底部系统状态栏始终固定在主窗口最底部，永不消失
2. 日志面板的功能和样式与之前保持一致
3. 日志面板的状态会自动持久化，下次启动时恢复
4. 如果需要恢复默认布局，可以使用「重置窗口布局」功能
