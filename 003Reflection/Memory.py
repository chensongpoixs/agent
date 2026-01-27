"""
Docstring for 003Reflection.Memory
@author: chensong
@date: 2026-01-27 16:28
@description: 一个简单的短期记忆模块，用于存储智能体的行动与反思轨迹。
"""

from typing import Any, Dict, List, Type, Union, Optional

"""
一个简单的短期记忆模块，用于存储智能体的行动与反思轨迹。
"""
class Memory:
    def __init__(self):
        self.memories: List[Dict[str, Any]] = []

    """
    添加一条记忆
    参数:
    - record_type: 记忆的类型（如“execution”、“reflection”等）
    - content: 记忆的具体内容 (列如：生成的代码或者反思的反馈)
    """
    def add_record(self, record_type: str, content: str):
        

        memorie  = {"type": record_type, "content": content};
        
        self.memories.append(memorie)
        print(f"Added memory: {memorie}");
 
    def get_memories(self) -> List[Dict[str, Any]]:
        """获取所有记忆"""
        return self.memories
    """
        将所有记忆记录格式化为一个连贯的字符串文本，用于构建提示词。
        """
    def get_trajectory(self) -> str:
        
        trajectory_parts = []
        for memorie in self.memories:
            if memorie['type'] == 'execution':
                trajectory_parts.append(f"--- 上一轮尝试 (代码) ---\n{memorie['content']}")
            elif memorie['type'] == 'reflection':
                trajectory_parts.append(f"--- 评审员反馈 ---\n{memorie['content']}")

        return "\n\n".join(trajectory_parts)
    
    def get_last_execution(self) -> Optional[str]:
        """
        获取最近一次的执行结果 (例如，最新生成的代码)。
        如果不存在，则返回 None。
        """
        for memorie in reversed(self.memories):
            if memorie['type'] == 'execution':
                return memorie['content']
        return None
    def clear_memories(self) -> None:
        """清除所有记忆"""
        self.memories.clear()