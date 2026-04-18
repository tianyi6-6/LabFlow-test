#!/usr/bin/env python3
"""LabFlow 辅助函数"""

import uuid
import time
from datetime import datetime
from typing import Optional


def generate_id(prefix: str = "") -> str:
    """生成唯一ID"""
    return f"{prefix}{uuid.uuid4().hex[:8]}"


def format_time(timestamp: Optional[float] = None, format_str: str = "%Y-%m-%d %H:%M:%S.%f") -> str:
    """格式化时间"""
    if timestamp is None:
        timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime(format_str)


def format_log_time(timestamp: Optional[float] = None) -> str:
    """格式化日志时间"""
    if timestamp is None:
        timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S.%f")[:-3]


def get_file_size(file_path: str) -> int:
    """获取文件大小"""
    import os
    return os.path.getsize(file_path)


def human_readable_size(size: int) -> str:
    """将文件大小转换为人类可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """安全除法"""
    if b == 0:
        return default
    return a / b


def clamp(value: float, min_value: float, max_value: float) -> float:
    """限制值在指定范围内"""
    return max(min(value, max_value), min_value)


def linear_interpolate(x: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """线性插值"""
    if x1 == x2:
        return y1
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1)