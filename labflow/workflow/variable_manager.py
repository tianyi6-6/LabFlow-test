#!/usr/bin/env python3
"""LabFlow 变量管理器"""

from typing import Dict, Any, Optional


class VariableManager:
    """变量管理器类"""
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.variable_history: Dict[str, list] = {}  # 变量历史记录
    
    def add_variable(self, name: str, value: Any) -> bool:
        """添加变量"""
        self.variables[name] = value
        # 记录历史
        if name not in self.variable_history:
            self.variable_history[name] = []
        self.variable_history[name].append(value)
        print(f"变量 {name} 添加成功，值: {value}")
        return True
    
    def remove_variable(self, name: str) -> bool:
        """移除变量"""
        if name not in self.variables:
            print(f"变量 {name} 不存在")
            return False
        del self.variables[name]
        if name in self.variable_history:
            del self.variable_history[name]
        print(f"变量 {name} 移除成功")
        return True
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """获取变量值"""
        return self.variables.get(name, default)
    
    def set_variable(self, name: str, value: Any) -> bool:
        """设置变量值"""
        self.variables[name] = value
        # 记录历史
        if name not in self.variable_history:
            self.variable_history[name] = []
        self.variable_history[name].append(value)
        print(f"变量 {name} 设置成功，值: {value}")
        return True
    
    def get_all_variables(self) -> Dict[str, Any]:
        """获取所有变量"""
        return self.variables
    
    def get_variable_names(self) -> list:
        """获取所有变量名称"""
        return list(self.variables.keys())
    
    def get_variable_count(self) -> int:
        """获取变量数量"""
        return len(self.variables)
    
    def clear_variables(self) -> None:
        """清空所有变量"""
        self.variables.clear()
        self.variable_history.clear()
        print("所有变量清空成功")
    
    def get_variable_history(self, name: str) -> list:
        """获取变量历史记录"""
        return self.variable_history.get(name, [])
    
    def has_variable(self, name: str) -> bool:
        """检查变量是否存在"""
        return name in self.variables
    
    def rename_variable(self, old_name: str, new_name: str) -> bool:
        """重命名变量"""
        if old_name not in self.variables:
            print(f"变量 {old_name} 不存在")
            return False
        if new_name in self.variables:
            print(f"变量 {new_name} 已存在")
            return False
        self.variables[new_name] = self.variables[old_name]
        if old_name in self.variable_history:
            self.variable_history[new_name] = self.variable_history[old_name]
            del self.variable_history[old_name]
        del self.variables[old_name]
        print(f"变量 {old_name} 重命名为 {new_name} 成功")
        return True
    
    def copy_variable(self, source_name: str, target_name: str) -> bool:
        """复制变量"""
        if source_name not in self.variables:
            print(f"变量 {source_name} 不存在")
            return False
        if target_name in self.variables:
            print(f"变量 {target_name} 已存在")
            return False
        self.variables[target_name] = self.variables[source_name]
        if source_name in self.variable_history:
            self.variable_history[target_name] = self.variable_history[source_name].copy()
        print(f"变量 {source_name} 复制为 {target_name} 成功")
        return True
    
    def import_variables(self, variables: Dict[str, Any]) -> bool:
        """导入变量"""
        try:
            for name, value in variables.items():
                self.add_variable(name, value)
            print(f"成功导入 {len(variables)} 个变量")
            return True
        except Exception as e:
            print(f"导入变量失败: {e}")
            return False
    
    def export_variables(self) -> Dict[str, Any]:
        """导出变量"""
        return self.variables.copy()
    
    def get_variable_type(self, name: str) -> Optional[str]:
        """获取变量类型"""
        if name not in self.variables:
            return None
        return type(self.variables[name]).__name__