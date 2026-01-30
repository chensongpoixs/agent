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

# import torch
# # from sentence_transformers import SentenceTransformer  # type: ignore
# try:  # numpy 非强依赖
#     import numpy as np  # type: ignore
# except Exception:  # pragma: no cover
#     np = None  # type: ignore


# import logging

# logger = logging.Logger(__name__)

# # import torch

# # 检查 GPU
# # device = "cuda" if torch.cuda.is_available() else "cpu"
# # logger.info(f"Using device: {device}")

# Vector = Union[List[float], "np.ndarray"]  # type: ignore[name-defined]


# @runtime_checkable
# class EmbeddingModel(Protocol):
#     """RAG/Memory 统一嵌入接口（最小约定）"""

#     @property
#     def dimension(self) -> int: ...

#     def encode(self, texts: Union[str, List[str]]) -> Any: ...


# @dataclass
# class HashTextEmbedder:
#     """确定性哈希文本嵌入（用于兜底跑通流程）。"""

#     dimension: int = 384

#     def encode(self, text: str) -> Vector:
#         logger.info(f"encode --->>>>> text:{text}")
#         text = text or ""
#         needed_bytes = self.dimension * 4  # uint32
#         buf = b""
#         counter = 0
#         while len(buf) < needed_bytes:
#             buf += hashlib.sha256((text + f"#{counter}").encode("utf-8")).digest()
#             counter += 1
#         raw = buf[:needed_bytes]

#         # numpy 可用则返回 ndarray，否则返回 list[float]
#         if np is None:
#             out: List[float] = []
#             for i in range(0, needed_bytes, 4):
#                 n = int.from_bytes(raw[i : i + 4], "little", signed=False)
#                 out.append((n % 10_000_000) / 10_000_000.0)
#             return out

#         arr = np.frombuffer(raw, dtype=np.uint32)
#         vec = (arr % 10_000_000).astype(np.float32) / 10_000_000.0
#         return vec


# class LocalTransformerEmbedding:
#     """可选：sentence-transformers 本地嵌入；不可用时抛 ImportError。"""

#     def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
#         from sentence_transformers import SentenceTransformer  # type: ignore

#         self.model_name = model_name
#         self._model = SentenceTransformer(model_name,
#                                         #    device=device )#, ignore_mismatched_sizes=True)
#         logger.info(f"model:{self._model}")
#         # dimension 探测
#         try:
#             self._dimension = int(self._model.get_sentence_embedding_dimension())
#         except Exception:
#             logger.warning(f"SentenceTransformer model_name:{self.model_name}  init failed !!!")
#             test = self._model.encode("health_check")
#             self._dimension = int(len(test))

#     @property
#     def dimension(self) -> int:
#         return int(self._dimension)

#     def encode(self, texts: Union[str, List[str]]):
#         logger.info(f"texts:{texts}");
#         results = [];
#         for text in texts:
#             result = self._model.encode(text)
#             results.append(result);
        
#         return results;
#         return self._model.encode(texts)
#     # def encode(self, text: str):
#     #     logger.info(f"text:{text}");
#     #     return self._model.encode(text)


# class TFIDFEmbedding:
#     """可选：sklearn 的 TF-IDF；未 fit 时自动用哈希兜底（避免启动失败）。"""

#     def __init__(self, max_features: int = 1000):
#         self.max_features = int(max_features)
#         self._dimension = self.max_features
#         self._fallback = HashTextEmbedder(dimension=min(384, self.max_features))
#         self._vectorizer = None
#         self._is_fitted = False
#         try:
#             from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore

#             self._vectorizer = TfidfVectorizer(max_features=self.max_features)
#         except Exception:
#             self._vectorizer = None

#     @property
#     def dimension(self) -> int:
#         return int(self._dimension)

#     def fit(self, texts: List[str]) -> None:
#         if self._vectorizer is None:
#             return
#         self._vectorizer.fit(texts)
#         self._is_fitted = True
#         try:
#             self._dimension = int(len(self._vectorizer.get_feature_names_out()))
#         except Exception:
#             self._dimension = self.max_features

#     def encode(self, texts: Union[str, List[str]]):
#         logger.info(f"encode, texts:{texts}")
#         if isinstance(texts, str):
#             if not self._is_fitted or self._vectorizer is None:
#                 return self._fallback.encode(texts)
#             return self._vectorizer.transform([texts]).toarray()[0]
#         # list[str]
#         inputs = list(texts)
#         if not self._is_fitted or self._vectorizer is None:
#             return [self._fallback.encode(t) for t in inputs]
#         return self._vectorizer.transform(inputs).toarray()


# _EMBEDDER: Optional[HashTextEmbedder] = None


# def create_embedding_model(model_type: str = "hash", **kwargs):
#     """RAG 侧工厂：local/tfidf/hash（dashscope 未在最小实现中启用）。"""
#     t = (model_type or "hash").strip().lower()
#     if t in {"local", "sentence_transformer", "sentence-transformers", "huggingface"}:
#         return LocalTransformerEmbedding(model_name=kwargs.get("model_name") or "sentence-transformers/all-MiniLM-L6-v2")
#     if t == "tfidf":
#         return TFIDFEmbedding(max_features=int(kwargs.get("max_features", 1000)))
#     if t == "hash":
#         return HashTextEmbedder(dimension=int(kwargs.get("dimension", 384)))
#     raise ValueError(f"不支持的模型类型: {model_type}")


# def create_embedding_model_with_fallback(preferred_type: str = "local", **kwargs):
#     """优先 preferred_type，不可用时回退到 hash（保证永不失败）。"""
#     logger.info(f"=======================create_embedding_model_with_fallback, preferred_type:{preferred_type}")
#     for t in [preferred_type, "local", "tfidf", "hash"]:
#         try:
#             return create_embedding_model(t, **kwargs)
#         except Exception:
#             continue
#     return HashTextEmbedder(dimension=int(kwargs.get("dimension", 384)))


# def get_text_embedder() -> EmbeddingModel:
#     """获取全局 embedder 单例。"""
#     global _EMBEDDER
#     logger.info(f"========================>_EMBEDDER:{_EMBEDDER}")
#     if _EMBEDDER is None:
#         # 默认选择 hash 以保证无依赖也能启动；如安装了 sentence-transformers，可通过环境变量切换
#         preferred = (os.getenv("EMBED_MODEL_TYPE") or "hash").strip().lower()
#         model_name = (os.getenv("EMBED_MODEL_NAME") or "sentence-transformers/all-MiniLM-L6-v2").strip()
#         dim = int(os.getenv("EMBEDDING_DIM", "384"))
#         try:
#             emb = create_embedding_model_with_fallback(
#                 preferred_type=preferred,
#                 model_name=model_name,
#                 dimension=dim,
#             )
#         except Exception:
#             logger.warning("text embedder failed !!!");
#             emb = HashTextEmbedder(dimension=dim)
#         # 我们缓存 hash embedder（满足 Memory 侧调用）；若返回的是非 HashTextEmbedder 也可用
#         _EMBEDDER = emb if isinstance(emb, HashTextEmbedder) else HashTextEmbedder(dimension=dim)
#     return _EMBEDDER


# def get_dimension(default: int = 384) -> int:
#     """返回 embedder 维度。"""
#     try:
#         return int(getattr(get_text_embedder(), "dimension", default))
#     except Exception:
#         return int(default)



"""统一嵌入模块（实现 + 提供器）

说明（中文）：
- 提供统一的文本嵌入接口与多实现：本地Transformer、DashScope（通义千问）、TF-IDF兜底。
- 暴露 get_text_embedder()/get_dimension()/refresh_embedder() 供各记忆类型统一使用。
- 通过环境变量优先级：dashscope > local > tfidf。

环境变量：
- EMBED_MODEL_TYPE: "dashscope" | "local" | "tfidf"（默认 dashscope）
- EMBED_MODEL_NAME: 模型名称（dashscope默认 text-embedding-v3；local默认 sentence-transformers/all-MiniLM-L6-v2）
- EMBED_API_KEY: Embedding API Key（统一命名）
- EMBED_BASE_URL: Embedding Base URL（统一命名，可选）
"""

from typing import List, Union, Optional
import threading
import os
import numpy as np


# ==============
# 抽象与实现
# ==============

class EmbeddingModel:
    """嵌入模型基类（最小接口）"""

    def encode(self, texts: Union[str, List[str]]):
        raise NotImplementedError

    @property
    def dimension(self) -> int:
        raise NotImplementedError


class LocalTransformerEmbedding(EmbeddingModel):
    """本地Transformer嵌入（优先 sentence-transformers，缺失回退 transformers+torch）"""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._backend = None  # "st" 或 "hf"
        self._st_model = None
        self._hf_tokenizer = None
        self._hf_model = None
        self._dimension = None
        self._load_backend()

    def _load_backend(self):
        # 优先 sentence-transformers
        try:
            from sentence_transformers import SentenceTransformer
            self._st_model = SentenceTransformer(self.model_name)
            test_vec = self._st_model.encode("test_text")
            self._dimension = len(test_vec)
            self._backend = "st"
            return
        except Exception:
            self._st_model = None

        # 回退 transformers
        try:
            from transformers import AutoTokenizer, AutoModel
            import torch
            self._hf_tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self._hf_model = AutoModel.from_pretrained(self.model_name)
            with torch.no_grad():
                inputs = self._hf_tokenizer("test_text", return_tensors="pt", padding=True, truncation=True)
                outputs = self._hf_model(**inputs)
                test_embedding = outputs.last_hidden_state.mean(dim=1)
                self._dimension = int(test_embedding.shape[1])
            self._backend = "hf"
            return
        except Exception:
            self._hf_tokenizer = None
            self._hf_model = None

        raise ImportError("未找到可用的本地嵌入后端，请安装 sentence-transformers 或 transformers+torch")

    def encode(self, texts: Union[str, List[str]]):
        if isinstance(texts, str):
            inputs = [texts]
            single = True
        else:
            inputs = list(texts)
            single = False

        if self._backend == "st":
            vecs = self._st_model.encode(inputs)
            if hasattr(vecs, "tolist"):
                vecs = [v for v in vecs]
        else:
            import torch
            tokenized = self._hf_tokenizer(inputs, return_tensors="pt", padding=True, truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self._hf_model(**tokenized)
                embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
            vecs = [v for v in embeddings]

        if single:
            return vecs[0]
        return vecs

    @property
    def dimension(self) -> int:
        return int(self._dimension or 0)


class TFIDFEmbedding(EmbeddingModel):
    """TF-IDF 简易兜底（在无深度模型时保证可用）"""

    def __init__(self, max_features: int = 1000):
        self.max_features = max_features
        self._vectorizer = None
        self._is_fitted = False
        self._dimension = max_features
        self._init_vectorizer()

    def _init_vectorizer(self):
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            self._vectorizer = TfidfVectorizer(max_features=self.max_features, stop_words='english')
        except ImportError:
            raise ImportError("请安装 scikit-learn: pip install scikit-learn")

    def fit(self, texts: List[str]):
        self._vectorizer.fit(texts)
        self._is_fitted = True
        self._dimension = len(self._vectorizer.get_feature_names_out())

    def encode(self, texts: Union[str, List[str]]):
        if not self._is_fitted:
            raise ValueError("TF-IDF模型未训练，请先调用fit()方法")
        if isinstance(texts, str):
            texts = [texts]
            single = True
        else:
            single = False
        tfidf_matrix = self._vectorizer.transform(texts)
        embeddings = tfidf_matrix.toarray()
        if single:
            return embeddings[0]
        return [e for e in embeddings]

    @property
    def dimension(self) -> int:
        return self._dimension


class DashScopeEmbedding(EmbeddingModel):
    """阿里云 DashScope（通义千问）Embedding / OpenAI兼容REST 模式

    行为：
    - 如提供 base_url，则优先使用 OpenAI 兼容的 REST 接口（POST {base_url}/embeddings）。
    - 否则使用官方 dashscope SDK 的 TextEmbedding.call。
    """

    def __init__(self, model_name: str = "text-embedding-v3", api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        self._dimension = None
        # 仅在非REST情况下初始化SDK
        if not self.base_url:
            self._init_client()
        # 探测维度
        test = self.encode("health_check")
        self._dimension = len(test)

    def _init_client(self):
        try:
            if self.api_key:
                # 将统一命名的 API Key 注入到 SDK 期望的位置
                os.environ["DASHSCOPE_API_KEY"] = self.api_key
            import dashscope  # noqa: F401
        except ImportError:
            raise ImportError("请安装 dashscope: pip install dashscope")

    def encode(self, texts: Union[str, List[str]]):
        if isinstance(texts, str):
            inputs = [texts]
            single = True
        else:
            inputs = list(texts)
            single = False

        # REST 模式（OpenAI兼容）
        if self.base_url:
            import requests
            url = self.base_url.rstrip("/") + "/embeddings"
            headers = {
                "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                "Content-Type": "application/json",
            }
            payload = {"model": self.model_name, "input": inputs}
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code >= 400:
                raise RuntimeError(f"Embedding REST 调用失败: {resp.status_code} {resp.text}")
            data = resp.json()
            # 期望结构：{"data": [{"embedding": [...]}]}
            items = data.get("data") or []
            vecs = [np.array(item.get("embedding")) for item in items]
            if single:
                return vecs[0]
            return vecs

        # SDK 模式
        from dashscope import TextEmbedding
        rsp = TextEmbedding.call(model=self.model_name, input=inputs)
        embeddings_obj = None
        if isinstance(rsp, dict):
            embeddings_obj = (rsp.get("output") or {}).get("embeddings")
        else:
            embeddings_obj = getattr(getattr(rsp, "output", None), "embeddings", None)
        if not embeddings_obj:
            raise RuntimeError("DashScope 返回为空或格式不匹配")
        vecs = [np.array(item.get("embedding") or item.get("vector")) for item in embeddings_obj]
        if single:
            return vecs[0]
        return vecs

    @property
    def dimension(self) -> int:
        return int(self._dimension or 0)


# ==============
# 工厂与回退
# ==============

def create_embedding_model(model_type: str = "local", **kwargs) -> EmbeddingModel:
    """创建嵌入模型实例

    model_type: "dashscope" | "local" | "tfidf"
    kwargs: model_name, api_key
    """
    if model_type in ("local", "sentence_transformer", "huggingface"):
        return LocalTransformerEmbedding(**kwargs)
    elif model_type == "dashscope":
        return DashScopeEmbedding(**kwargs)
    elif model_type == "tfidf":
        return TFIDFEmbedding(**kwargs)
    else:
        raise ValueError(f"不支持的模型类型: {model_type}")


def create_embedding_model_with_fallback(preferred_type: str = "dashscope", **kwargs) -> EmbeddingModel:
    """带回退的创建：dashscope -> local -> tfidf"""
    if preferred_type in ("sentence_transformer", "huggingface"):
        preferred_type = "local"
    fallback = ["dashscope", "local", "tfidf"]
    # 将首选放最前
    if preferred_type in fallback:
        fallback.remove(preferred_type)
        fallback.insert(0, preferred_type)
    for t in fallback:
        try:
            return create_embedding_model(t, **kwargs)
        except Exception:
            continue
    raise RuntimeError("所有嵌入模型都不可用，请安装依赖或检查配置")


# ==================
# Provider（单例）
# ==================

_lock = threading.RLock()
_embedder: Optional[EmbeddingModel] = None


def _build_embedder() -> EmbeddingModel:
    preferred = os.getenv("EMBED_MODEL_TYPE", "dashscope").strip()
    # 根据提供商选择默认模型
    default_model = "text-embedding-v3" if preferred == "dashscope" else "sentence-transformers/all-MiniLM-L6-v2"
    model_name = os.getenv("EMBED_MODEL_NAME", default_model).strip()
    kwargs = {}
    if model_name:
        kwargs["model_name"] = model_name
    # 仅使用统一命名
    api_key = os.getenv("EMBED_API_KEY")
    if api_key:
        kwargs["api_key"] = api_key
    base_url = os.getenv("EMBED_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url
    return create_embedding_model_with_fallback(preferred_type=preferred, **kwargs)


def get_text_embedder() -> EmbeddingModel:
    """获取全局共享的文本嵌入实例（线程安全单例）"""
    global _embedder
    if _embedder is not None:
        return _embedder
    with _lock:
        if _embedder is None:
            _embedder = _build_embedder()
        return _embedder


def get_dimension(default: int = 384) -> int:
    """获取统一向量维度（失败回退默认值）"""
    try:
        return int(getattr(get_text_embedder(), "dimension", default))
    except Exception:
        return int(default)


def refresh_embedder() -> EmbeddingModel:
    """强制重建嵌入实例（可用于动态切换环境变量）"""
    global _embedder
    with _lock:
        _embedder = _build_embedder()
        return _embedder


