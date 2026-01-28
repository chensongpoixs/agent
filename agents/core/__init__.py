"""核心框架模块"""

from .agent import Agent
from .llm_client import LlmClient
from .message import Message
from .config import Config
from .exceptions import AgentsException
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
    "Agent",
    "LlmClient", 
    "Message",
    "Config",
    "AgentsException"
]