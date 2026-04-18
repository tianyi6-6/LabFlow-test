# LabFlow 分割器样式调整说明

## 概述

本文件提供了如何调整 LabFlow 应用程序中分割器样式的详细说明，包括分割线颜色、宽度、可点击热区大小等参数的修改方法。

## 样式调整方法

### 1. 修改分割线颜色

**修改方法**：
1. 打开 `labflow/app/styled_splitter.py` 文件
2. 在 `StyledSplitterHandle` 类的 `paintEvent` 方法中，修改以下颜色值：

```python
# 默认状态：浅灰色分割线
painter.setPen(QColor(224, 224, 224))  # #E0E0E0

# 悬停状态：橙色分割线
painter.setPen(QColor(255, 122, 0))  # #FF7A00
```

**示例**：
- 将默认分割线颜色改为深灰色：`QColor(128, 128, 128)`
- 将悬停分割线颜色改为蓝色：`QColor(0, 122, 255)`

### 2. 修改分割线宽度

**修改方法**：
1. 打开 `labflow/app/styled_splitter.py` 文件
2. 在 `StyledSplitterHandle` 类的 `paintEvent` 方法中，修改以下代码：

```python
if self.is_hovered:
    # 悬停状态：橙色分割线
    painter.setPen(QColor(255, 122, 0))  # #FF7A00
    painter.drawLine(0, center - 1, self.width(), center - 1)
    painter.drawLine(0, center, self.width(), center)
else:
    # 默认状态：浅灰色分割线
    painter.setPen(QColor(224, 224, 224))  # #E0E0E0
    painter.drawLine(0, center, self.width(), center)
```

**示例**：
- 将悬停状态分割线宽度改为 3px：
  ```python
  painter.drawLine(0, center - 1, self.width(), center - 1)
  painter.drawLine(0, center, self.width(), center)
  painter.drawLine(0, center + 1, self.width(), center + 1)
  ```

### 3. 修改可点击热区大小

**修改方法**：
1. 打开 `labflow/app/styled_splitter.py` 文件
2. 在 `StyledSplitterHandle` 类的 `__init__` 方法中，修改以下代码：

```python
def __init__(self, orientation, parent):
    super().__init__(orientation, parent)
    self.setMinimumSize(8, 8)  # 增大可点击热区
    self.setCursor(QCursor(Qt.SplitHCursor if orientation == Qt.Horizontal else Qt.SplitVCursor))
    self.is_hovered = False
```

3. 在 `StyledSplitter` 类的 `__init__` 方法中，修改以下代码：

```python
def __init__(self, orientation=Qt.Horizontal, parent=None):
    super().__init__(orientation, parent)
    self.setHandleWidth(8)  # 增大分割器宽度
    self.setStyleSheet("""
        QSplitter {
            background-color: transparent;
        }
        QSplitter::handle {
            background-color: transparent;
        }
        QSplitter::handle:hover {
            background-color: rgba(255, 122, 0, 0.1);  # 悬停时的背景色
        }
    """)
```

**示例**：
- 将可点击热区大小改为 12px：
  - `self.setMinimumSize(12, 12)`
  - `self.setHandleWidth(12)`

### 4. 修改分割器悬停背景色

**修改方法**：
1. 打开 `labflow/app/styles.qss` 文件
2. 修改以下代码：

```css
/* 分割器手柄悬停状态 */
QSplitter::handle:hover {
    background-color: rgba(255, 122, 0, 0.1);
}

/* 分割器手柄拖拽状态 */
QSplitter::handle:pressed {
    background-color: rgba(255, 122, 0, 0.2);
}
```

**示例**：
- 将悬停背景色改为蓝色：`rgba(0, 122, 255, 0.1)`
- 将拖拽背景色改为绿色：`rgba(52, 168, 83, 0.2)`

## 样式调整示例

### 示例 1：调整为蓝色分割线

1. 修改 `labflow/app/styled_splitter.py` 文件：

```python
# 默认状态：浅蓝色分割线
painter.setPen(QColor(187, 222, 251))  # #BBDFFB

# 悬停状态：蓝色分割线
painter.setPen(QColor(0, 122, 255))  # #007AFF
```

2. 修改 `labflow/app/styles.qss` 文件：

```css
/* 分割器手柄悬停状态 */
QSplitter::handle:hover {
    background-color: rgba(0, 122, 255, 0.1);
}

/* 分割器手柄拖拽状态 */
QSplitter::handle:pressed {
    background-color: rgba(0, 122, 255, 0.2);
}
```

### 示例 2：增大可点击热区

修改 `labflow/app/styled_splitter.py` 文件：

```python
# StyledSplitterHandle 类
self.setMinimumSize(12, 12)  # 增大可点击热区

# StyledSplitter 类
self.setHandleWidth(12)  # 增大分割器宽度
```

## 注意事项

1. 样式调整后需要重新启动应用程序才能生效
2. 分割器样式的修改不会影响其他功能
3. 建议在调整样式时保持分割器的可用性和美观性
4. 如果需要恢复默认样式，可以参考本文件中的默认值进行修改