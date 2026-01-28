"""核心框架模块"""

from .simple_agent import SimpleAgent
# from .react_agent import ReActAgent
# from .reflection_agent import ReflectionAgent
# from .plan_solve_agent import PlanAndSolveAgent
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
# 保持向后兼容性
try:
    # from .tool_agent import ToolAgent
    # from .conversational import ConversationalAgent
    __all__ = [
        "SimpleAgent",
        # "ReActAgent",
        # "ReflectionAgent",
        # "PlanAndSolveAgent",
        # "ToolAgent",
        # "ConversationalAgent"
    ]
except ImportError:
    __all__ = [
        "SimpleAgent",
        # "ReActAgent",
        # "ReflectionAgent",
        # "PlanAndSolveAgent"
    ]