"""
 Agents - 灵活、可扩展的多智能体框架

基于OpenAI原生API构建，提供简洁高效的智能体开发体验。
"""

# 配置第三方库的日志级别，减少噪音
from agents.version import __version__, __author__, __email__, __description__

from . import main
# 核心组件
from agents.core.llm_client import LlmClient
from agents.core.config import Config
from agents.core.message import Message
from agents.core.exceptions import AgentsException

# Agent实现
from agents.agent.simple_agent import SimpleAgent
# from .agent.react_agent import ReActAgent
# from .agent.reflection_agent import ReflectionAgent
# from .agent.plan_solve_agent import PlanAndSolveAgent

# 工具系统
from agents.tools.registry import ToolRegistry, global_registry
from agents.tools.builtin.search import SearchTool, search
from agents.tools.builtin.calculator import CalculatorTool, calculate
from agents.tools.chain import ToolChain, ToolChainManager
from agents.tools.async_executor import AsyncToolExecutor

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