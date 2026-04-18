#!/usr/bin/env python3
"""LabFlow 样式分割器"""

from PySide6.QtWidgets import QSplitter, QSplitterHandle
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QCursor, QPainter, QColor


class StyledSplitterHandle(QSplitterHandle):
    """样式化的分割器手柄"""
    
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)
        self.setMinimumSize(8, 8)  # 增大可点击热区
        self.setCursor(QCursor(Qt.SplitHCursor if orientation == Qt.Horizontal else Qt.SplitVCursor))
        self.is_hovered = False
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        self.is_hovered = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        self.is_hovered = False
        self.update()
        super().leaveEvent(event)
    
    def paintEvent(self, event):
        """绘制分割器"""
        painter = QPainter(self)
        
        if self.orientation() == Qt.Horizontal:
            # 水平分割器（左右方向）
            center = self.height() // 2
            if self.is_hovered:
                # 悬停状态：橙色分割线
                painter.setPen(QColor(255, 122, 0))  # #FF7A00
                painter.drawLine(0, center - 1, self.width(), center - 1)
                painter.drawLine(0, center, self.width(), center)
            else:
                # 默认状态：浅灰色分割线
                painter.setPen(QColor(224, 224, 224))  # #E0E0E0
                painter.drawLine(0, center, self.width(), center)
        else:
            # 垂直分割器（上下方向）
            center = self.width() // 2
            if self.is_hovered:
                # 悬停状态：橙色分割线
                painter.setPen(QColor(255, 122, 0))  # #FF7A00
                painter.drawLine(center - 1, 0, center - 1, self.height())
                painter.drawLine(center, 0, center, self.height())
            else:
                # 默认状态：浅灰色分割线
                painter.setPen(QColor(224, 224, 224))  # #E0E0E0
                painter.drawLine(center, 0, center, self.height())


class StyledSplitter(QSplitter):
    """样式化的分割器"""
    
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
                background-color: rgba(255, 122, 0, 0.1);
            }
        """)
    
    def createHandle(self):
        """创建分割器手柄"""
        return StyledSplitterHandle(self.orientation(), self)
