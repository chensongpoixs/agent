"""通用工具模块"""

from .logging import setup_logger, get_logger
from .serialization import serialize_object, deserialize_object
from .helpers import format_time, validate_config, safe_import
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
    "setup_logger", "get_logger",
    "serialize_object", "deserialize_object", 
    "format_time", "validate_config", "safe_import"
]