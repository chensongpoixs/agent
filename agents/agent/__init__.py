"""核心框架模块"""

from .simple_agent import SimpleAgent
# from .react_agent import ReActAgent
# from .reflection_agent import ReflectionAgent
# from .plan_solve_agent import PlanAndSolveAgent
# your_package/__init__.py
import logging
import sys
import os
# 只在第一次导入时配置
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

class ProjectPathFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, project_root=None):
        super().__init__(fmt, datefmt)
        self.project_root = os.path.abspath(project_root) if project_root else None

    def format(self, record):
        if self.project_root:
            try:
                record.project_path = os.path.relpath(
                    record.pathname, self.project_root
                )
            except ValueError:
                record.project_path = record.pathname
        else:
            record.project_path = record.pathname

        return super().format(record)

# 只在第一次导入时配置
# 只在第一次导入时配置
if not hasattr(sys, '_logging_configured'):
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s',
    #     datefmt='%Y-%m-%d %H:%M:%S',
    #     handlers=[
    #         logging.StreamHandler(sys.stdout),
    #         logging.FileHandler('app.log', encoding='utf-8')
    #     ]
    # )
    # sys._logging_configured = True
    formatter = ProjectPathFormatter(
        fmt='[%(asctime)s][%(levelname)s][%(project_path)s][%(lineno)d][%(funcName)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        project_root=PROJECT_ROOT
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # stdout
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)

    # file
    fh = logging.FileHandler('app.log', encoding='utf-8')
    fh.setFormatter(formatter)

    root_logger.addHandler(sh)
    root_logger.addHandler(fh)

    sys._logging_configured = True

# 或者使用函数方式
def init_logging(level=logging.INFO, project_root=None):
    # logging.basicConfig(
    #     level=level,
    #     format='[%(asctime)s][%(levelname)s][%(filename)s][%(lineno)d][%(funcName)s] %(message)s',
    #     datefmt='%Y-%m-%d %H:%M:%S'
    # )
    formatter = ProjectPathFormatter(
        fmt='[%(asctime)s][%(levelname)s][%(project_path)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        project_root=project_root
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    root_logger.addHandler(sh)
    # 可选：写文件
    fh = logging.FileHandler('app.log', encoding='utf-8')
    fh.setFormatter(formatter)
    root_logger.addHandler(fh)
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