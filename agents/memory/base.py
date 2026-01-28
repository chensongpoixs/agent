"""记忆系统基础结构（最小可运行实现）。

当前仓库的多个模块会直接导入：
- MemoryConfig
- MemoryItem
- BaseMemory

该文件被回滚为占位注释时，会导致 `ImportError: cannot import name 'MemoryConfig'`，
从而阻断 `python -m agents.main` 启动链。这里提供一个轻量实现用于恢复运行能力。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class MemoryConfig:
    """记忆系统配置（默认值覆盖当前代码中被访问到的字段）。"""

    # 通用
    max_capacity: int = 1000
    importance_threshold: float = 0.1
    decay_factor: float = 0.95

    # working
    working_memory_capacity: int = 50
    working_memory_tokens: int = 4000
    # working_memory_ttl_minutes: Optional[int]  # 通过 getattr 扩展

    # episodic/perceptual 本地存储
    storage_path: str = "./memory_data"

    # perceptual
    perceptual_memory_modalities: List[str] = field(
        default_factory=lambda: ["text", "image", "audio"]
    )


@dataclass
class MemoryItem:
    """单条记忆的统一数据结构。"""

    id: str
    content: str
    memory_type: str = "working"
    user_id: str = "default_user"
    timestamp: datetime = field(default_factory=datetime.now)
    importance: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseMemory:
    """各类记忆（working/episodic/semantic/perceptual）的抽象基类。"""

    def __init__(self, config: MemoryConfig, storage_backend: Any = None):
        self.config = config
        self.storage_backend = storage_backend

    def add(self, memory_item: MemoryItem) -> str:  # pragma: no cover
        raise NotImplementedError

    def retrieve(self, query: str, limit: int = 5, **kwargs) -> List[MemoryItem]:  # pragma: no cover
        raise NotImplementedError

    def remove(self, memory_id: str) -> bool:  # pragma: no cover
        raise NotImplementedError

    # ---- optional helpers (best-effort defaults) ----
    def get_all(self) -> List[MemoryItem]:
        for attr in ("memories", "semantic_memories", "perceptual_memories"):
            if hasattr(self, attr):
                try:
                    return list(getattr(self, attr))
                except Exception:
                    pass
        return []

    def clear(self) -> None:
        for attr in ("memories", "semantic_memories", "perceptual_memories"):
            if hasattr(self, attr):
                try:
                    getattr(self, attr).clear()
                except Exception:
                    pass

    def get_stats(self) -> Dict[str, Any]:
        try:
            all_items = self.get_all()
            return {"count": len(all_items), "total_count": len(all_items)}
        except Exception:
            return {"count": 0, "total_count": 0}
