"""工具系统"""

from .base import Tool, ToolParameter
from .registry import ToolRegistry, global_registry

# 内置工具
from .builtin.search import SearchTool
from .builtin.calculator import CalculatorTool
from .builtin.memory_tool import MemoryTool
from .builtin.rag_tool import RAGTool
# 高级功能
from .chain import ToolChain, ToolChainManager, create_research_chain, create_simple_chain
from .async_executor import AsyncToolExecutor, run_parallel_tools, run_batch_tool, run_parallel_tools_sync, run_batch_tool_sync
# your_package/__init__.py
import logging
import sys

# 只在第一次导入时配置
if not hasattr(sys, '_logging_configured'):
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log', encoding='utf-8')
        ]
    )
    sys._logging_configured = True

# 或者使用函数方式
def init_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
__all__ = [
    # 基础工具系统
    "Tool",
    "ToolParameter",
    "ToolRegistry",
    "global_registry",

    # 内置工具
    "SearchTool",
    "CalculatorTool",
    "MemoryTool",
    "RAGTool",

    # 工具链功能
    "ToolChain",
    "ToolChainManager",
    "create_research_chain",
    "create_simple_chain",

    # 异步执行功能
    "AsyncToolExecutor",
    "run_parallel_tools",
    "run_batch_tool",
    "run_parallel_tools_sync",
    "run_batch_tool_sync",
]
