#!/usr/bin/env python3
"""LabFlow 包标准入口点

该文件是 Python 包的标准入口点，支持通过 `python -m experiment_flow_ui` 命令启动应用。
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiment_flow_ui.ui.main import main

if __name__ == "__main__":
    main()