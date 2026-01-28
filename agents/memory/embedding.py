"""统一嵌入服务（可运行 + 向后兼容 RAG 导出）。

当前仓库的记忆模块会导入：
- get_text_embedder()
- get_dimension()

同时 `agents.memory.rag.__init__` 还会从本模块导入：
- EmbeddingModel / LocalTransformerEmbedding / TFIDFEmbedding
- create_embedding_model / create_embedding_model_with_fallback

因此这里提供“最小可运行 + 可选依赖”的实现：优先 sentence-transformers / sklearn，
不可用时自动回退到哈希嵌入（永不失败），以保证 `python -m agents.main` 能启动。
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from typing import List, Optional, Union, Protocol, runtime_checkable, Any

try:  # numpy 非强依赖
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover
    np = None  # type: ignore


Vector = Union[List[float], "np.ndarray"]  # type: ignore[name-defined]


@runtime_checkable
class EmbeddingModel(Protocol):
    """RAG/Memory 统一嵌入接口（最小约定）"""

    @property
    def dimension(self) -> int: ...

    def encode(self, texts: Union[str, List[str]]) -> Any: ...


@dataclass
class HashTextEmbedder:
    """确定性哈希文本嵌入（用于兜底跑通流程）。"""

    dimension: int = 384

    def encode(self, text: str) -> Vector:
        text = text or ""
        needed_bytes = self.dimension * 4  # uint32
        buf = b""
        counter = 0
        while len(buf) < needed_bytes:
            buf += hashlib.sha256((text + f"#{counter}").encode("utf-8")).digest()
            counter += 1
        raw = buf[:needed_bytes]

        # numpy 可用则返回 ndarray，否则返回 list[float]
        if np is None:
            out: List[float] = []
            for i in range(0, needed_bytes, 4):
                n = int.from_bytes(raw[i : i + 4], "little", signed=False)
                out.append((n % 10_000_000) / 10_000_000.0)
            return out

        arr = np.frombuffer(raw, dtype=np.uint32)
        vec = (arr % 10_000_000).astype(np.float32) / 10_000_000.0
        return vec


class LocalTransformerEmbedding:
    """可选：sentence-transformers 本地嵌入；不可用时抛 ImportError。"""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer  # type: ignore

        self.model_name = model_name
        self._model = SentenceTransformer(model_name)
        # dimension 探测
        try:
            self._dimension = int(self._model.get_sentence_embedding_dimension())
        except Exception:
            test = self._model.encode("health_check")
            self._dimension = int(len(test))

    @property
    def dimension(self) -> int:
        return int(self._dimension)

    def encode(self, texts: Union[str, List[str]]):
        return self._model.encode(texts)


class TFIDFEmbedding:
    """可选：sklearn 的 TF-IDF；未 fit 时自动用哈希兜底（避免启动失败）。"""

    def __init__(self, max_features: int = 1000):
        self.max_features = int(max_features)
        self._dimension = self.max_features
        self._fallback = HashTextEmbedder(dimension=min(384, self.max_features))
        self._vectorizer = None
        self._is_fitted = False
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore

            self._vectorizer = TfidfVectorizer(max_features=self.max_features)
        except Exception:
            self._vectorizer = None

    @property
    def dimension(self) -> int:
        return int(self._dimension)

    def fit(self, texts: List[str]) -> None:
        if self._vectorizer is None:
            return
        self._vectorizer.fit(texts)
        self._is_fitted = True
        try:
            self._dimension = int(len(self._vectorizer.get_feature_names_out()))
        except Exception:
            self._dimension = self.max_features

    def encode(self, texts: Union[str, List[str]]):
        if isinstance(texts, str):
            if not self._is_fitted or self._vectorizer is None:
                return self._fallback.encode(texts)
            return self._vectorizer.transform([texts]).toarray()[0]
        # list[str]
        inputs = list(texts)
        if not self._is_fitted or self._vectorizer is None:
            return [self._fallback.encode(t) for t in inputs]
        return self._vectorizer.transform(inputs).toarray()


_EMBEDDER: Optional[HashTextEmbedder] = None


def create_embedding_model(model_type: str = "hash", **kwargs):
    """RAG 侧工厂：local/tfidf/hash（dashscope 未在最小实现中启用）。"""
    t = (model_type or "hash").strip().lower()
    if t in {"local", "sentence_transformer", "sentence-transformers", "huggingface"}:
        return LocalTransformerEmbedding(model_name=kwargs.get("model_name") or "sentence-transformers/all-MiniLM-L6-v2")
    if t == "tfidf":
        return TFIDFEmbedding(max_features=int(kwargs.get("max_features", 1000)))
    if t == "hash":
        return HashTextEmbedder(dimension=int(kwargs.get("dimension", 384)))
    raise ValueError(f"不支持的模型类型: {model_type}")


def create_embedding_model_with_fallback(preferred_type: str = "local", **kwargs):
    """优先 preferred_type，不可用时回退到 hash（保证永不失败）。"""
    for t in [preferred_type, "local", "tfidf", "hash"]:
        try:
            return create_embedding_model(t, **kwargs)
        except Exception:
            continue
    return HashTextEmbedder(dimension=int(kwargs.get("dimension", 384)))


def get_text_embedder() -> EmbeddingModel:
    """获取全局 embedder 单例。"""
    global _EMBEDDER
    if _EMBEDDER is None:
        # 默认选择 hash 以保证无依赖也能启动；如安装了 sentence-transformers，可通过环境变量切换
        preferred = (os.getenv("EMBED_MODEL_TYPE") or "hash").strip().lower()
        model_name = (os.getenv("EMBED_MODEL_NAME") or "sentence-transformers/all-MiniLM-L6-v2").strip()
        dim = int(os.getenv("EMBEDDING_DIM", "384"))
        try:
            emb = create_embedding_model_with_fallback(
                preferred_type=preferred,
                model_name=model_name,
                dimension=dim,
            )
        except Exception:
            emb = HashTextEmbedder(dimension=dim)
        # 我们缓存 hash embedder（满足 Memory 侧调用）；若返回的是非 HashTextEmbedder 也可用
        _EMBEDDER = emb if isinstance(emb, HashTextEmbedder) else HashTextEmbedder(dimension=dim)
    return _EMBEDDER


def get_dimension(default: int = 384) -> int:
    """返回 embedder 维度。"""
    try:
        return int(getattr(get_text_embedder(), "dimension", default))
    except Exception:
        return int(default)
