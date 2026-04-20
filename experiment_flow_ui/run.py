#!/usr/bin/env python3
"""LabFlow 运行脚本"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from experiment_flow_ui.ui.main import main

if __name__ == "__main__":
    main()