# """
#  Agents - 灵活、可扩展的多智能体框架

# 基于OpenAI原生API构建，提供简洁高效的智能体开发体验。
# """

# # 配置第三方库的日志级别，减少噪音
# from agents.version import __version__, __author__, __email__, __description__

# # from agents.main import main
# # 核心组件
# from agents.core.llm_client import LlmClient
# from agents.core.config import Config
# from agents.core.message import Message
# from agents.core.exceptions import AgentsException
# from agents.core.agent import Agent

# # Agent实现
# from agents.agent.simple_agent import SimpleAgent
# # from .agent.react_agent import ReActAgent
# # from .agent.reflection_agent import ReflectionAgent
# # from .agent.plan_solve_agent import PlanAndSolveAgent

# # 工具系统
# from agents.tools.registry import ToolRegistry, global_registry
# from agents.tools.builtin.search import SearchTool, search
# from agents.tools.builtin.calculator import CalculatorTool, calculate
# from agents.tools.chain import ToolChain, ToolChainManager
# from agents.tools.async_executor import AsyncToolExecutor

# __all__ = [
#     # 版本信息
#     "__version__",
#     "__author__",
#     "__email__",
#     "__description__",

#     # 核心组件
#     "LlmClient",
#     "Config",
#     "Message",
#     "AgentsException",
#     "Agent",

#     # Agent范式
#     "SimpleAgent",
#     # "ReActAgent",
#     # "ReflectionAgent",
#     # "PlanAndSolveAgent",

#     # 工具系统
#     "ToolRegistry",
#     "global_registry",
#     "SearchTool",
#     "search",
#     "CalculatorTool",
#     "calculate",
#     "ToolChain",
#     "ToolChainManager",
#     "AsyncToolExecutor",
# ]

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