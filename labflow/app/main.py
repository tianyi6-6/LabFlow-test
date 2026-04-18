#!/usr/bin/env python3
"""LabFlow 主应用入口"""

import sys
from PySide6.QtWidgets import QApplication
from .main_window import MainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    # 程序退出时保存工具窗口状态
    def save_state():
        from .tool_window_manager import ToolWindowManager
        tool_window_manager = ToolWindowManager()
        tool_window_manager.save_all_tool_window_states()
    
    app.aboutToQuit.connect(save_state)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()