"""
 Agents - 灵活、可扩展的多智能体框架

基于OpenAI原生API构建，提供简洁高效的智能体开发体验。
"""

# 配置第三方库的日志级别，减少噪音
from .version import __version__, __author__, __email__, __description__

# 核心组件
from .core.llm import LlmClient
from .core.config import Config
from .core.message import Message
from .core.exceptions import AgentsException

# Agent实现
from .agent.simple_agent import SimpleAgent
# from .agent.react_agent import ReActAgent
# from .agent.reflection_agent import ReflectionAgent
# from .agent.plan_solve_agent import PlanAndSolveAgent

# 工具系统
from .tools.registry import ToolRegistry, global_registry
from .tools.builtin.search import SearchTool, search
from .tools.builtin.calculator import CalculatorTool, calculate
from .tools.chain import ToolChain, ToolChainManager
from .tools.async_executor import AsyncToolExecutor

__all__ = [
    # 版本信息
    "__version__",
    "__author__",
    "__email__",
    "__description__",

    # 核心组件
    "LlmClient",
    "Config",
    "Message",
    "AgentsException",

    # Agent范式
    "SimpleAgent",
    # "ReActAgent",
    # "ReflectionAgent",
    # "PlanAndSolveAgent",

    # 工具系统
    "ToolRegistry",
    "global_registry",
    "SearchTool",
    "search",
    "CalculatorTool",
    "calculate",
    "ToolChain",
    "ToolChainManager",
    "AsyncToolExecutor",
]