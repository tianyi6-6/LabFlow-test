#!/usr/bin/env python3
"""LabFlow 安装配置"""

from setuptools import setup, find_packages

setup(
    name="labflow",
    version="0.1.0",
    description="科研仪器可视化工作流系统",
    author="LabFlow Team",
    author_email="labflow@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PySide6==6.6.2",
        "numpy==1.26.4",
        "pandas==2.2.1",
        "pyqtgraph==0.13.3",
        "matplotlib==3.8.4",
        "networkx==3.2.1",
        "pyserial==3.5",
        "pyyaml==6.0.1",
        "click==8.1.7"
    ],
    entry_points={
        "console_scripts": [
            "labflow=app.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10"
)