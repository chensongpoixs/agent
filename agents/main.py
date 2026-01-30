


# my_main.py
from dotenv import load_dotenv
from agents.core.llm_client import LlmClient    # 注意:这里导入我们自己的类
 
from agents.agent.simple_agent import SimpleAgent
from agents.tools.registry import ToolRegistry
from agents.tools.async_executor import AsyncToolExecutor
from agents.tools.builtin.calculator import CalculatorTool
from agents.agent.react_agent import ReActAgent
from agents.agent.reflection_agent import ReflectionAgent
from agents.agent.plan_solve_agent import PlanAndSolveAgent
from agents.tools.builtin.memory_tool import MemoryTool
from agents.tools.builtin.rag_tool import RAGTool
from agents.context import ContextBuilder, ContextConfig
from agents.tools import MemoryTool, RAGTool
from agents.core.message import Message
from datetime import datetime

import logging

import os
import logging
import sys

# 创建logger
logger = logging.getLogger(__name__)
# from agents import create_calculator_registry
# logging.basicConfig(level=logging.INFO)
# # 创建formatter，添加文件名和行号
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
# )

#     # 创建控制台handler
# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)
# 加载环境变量
load_dotenv()



def test_swiatch_provider():
    
    # 实例化我们重写的客户端，并指定provider
    llm = LlmClient(provider="llama.cpp") 
    # llm = LLM(provider="modelscope1") # 也可以这样指定

    # 准备消息
    messages = [{"role": "user", "content": "你好，请介绍一下你自己。"}]

    # 发起调用，think等方法都已从父类继承，无需重写
    response_stream = llm.think(messages)

    # 打印响应
    logger.info("ModelScope Response:")
    for chunk in response_stream:
        # chunk在my_llm库中已经打印过一遍，这里只需要pass即可
        logger.info(chunk, end="", flush=True)
        pass



# def test_calculator_tool():
#     """测试自定义计算器工具"""

#     # 创建包含计算器的注册表
#     registry = create_calculator_registry()

#     print("🧪 测试自定义计算器工具\n")

#     # 简单测试用例
#     test_cases = [
#         "2 + 3",           # 基本加法
#         "10 - 4",          # 基本减法
#         "5 * 6",           # 基本乘法
#         "15 / 3",          # 基本除法
#         "sqrt(16)",        # 平方根
#     ]

#     for i, expression in enumerate(test_cases, 1):
#         print(f"测试 {i}: {expression}")
#         result = registry.execute_tool("my_calculator", expression)
#         print(f"结果: {result}\n")

# def test_with_simple_agent():
#     """测试与SimpleAgent的集成"""
#     from agents import AgentsLLM

#     # 创建LLM客户端
#     llm = AgentsLLM()

#     # 创建包含计算器的注册表
#     registry = create_calculator_registry()

#     print("🤖 与SimpleAgent集成测试:")

#     # 模拟SimpleAgent使用工具的场景
#     user_question = "请帮我计算 sqrt(16) + 2 * 3"

#     print(f"用户问题: {user_question}")

#     # 使用工具计算
#     calc_result = registry.execute_tool("my_calculator", "sqrt(16) + 2 * 3")
#     print(f"计算结果: {calc_result}")

#     # 构建最终回答
#     final_messages = [
#         {"role": "user", "content": f"计算结果是 {calc_result}，请用自然语言回答用户的问题:{user_question}"}
#     ]

#     print("\n🎯 SimpleAgent的回答:")
#     response = llm.think(final_messages)
#     for chunk in response:
#         print(chunk, end="", flush=True)
#     print("\n")

# if __name__ == "__main__":
#     test_calculator_tool()
#     test_with_simple_agent()







def test_simaple_agent():
    # 创建LLM实例
    llm = LlmClient(provider="llama.cpp")

    # 测试1:基础对话Agent（无工具）
    logger.info("=== 测试1:基础对话 ===")
    basic_agent = SimpleAgent(
        name="基础助手",
        llm=llm,
        system_prompt="你是一个友好的AI助手，请用简洁明了的方式回答问题。"
    )

    response1 = basic_agent.run("你好，请介绍一下自己")
    logger.info(f"基础对话响应: {response1}\n")

    # 测试2:带工具的Agent
    logger.info("=== 测试2:工具增强对话 ===")
    tool_registry = ToolRegistry()
    calculator = CalculatorTool()
    tool_registry.register_tool(calculator)

    enhanced_agent = SimpleAgent(
        name="增强助手",
        llm=llm,
        system_prompt="你是一个智能助手，可以使用工具来帮助用户。",
        tool_registry=tool_registry,
        enable_tool_calling=True
    )

    response2 = enhanced_agent.run("请帮我计算 15 * 8 + 32")
    logger.info(f"工具增强响应: {response2}\n")

    # 测试3:流式响应
    logger.info("=== 测试3:流式响应 ===")
    logger.info("流式响应: ")
    chunk_data = "";
    for chunk in basic_agent.stream_run("请解释什么是人工智能"):
        # logger.info(f"{chunk}");
        #
        #pass  # 内容已在stream_run中实时打印
        pass

    # 测试4:动态添加工具
    logger.info("\n=== 测试4:动态工具管理 ===")
    logger.info(f"添加工具前: {basic_agent.has_tools()}")
    basic_agent.add_tool(calculator)
    logger.info(f"添加工具后: {basic_agent.has_tools()}")
    logger.info(f"可用工具: {basic_agent.list_tools()}")

    # 查看对话历史
    logger.info(f"\n对话历史: {len(basic_agent.get_history())} 条消息")




def test_reflection_agent():
    llm = LlmClient(provider="llama.cpp");

    # 使用默认通用提示词
    general_agent = ReflectionAgent(name="我的反思助手", llm=llm);
    
    # 使用自定义代码生成提示词(类似第四章)
    code_prompts = {
        "initial": "你是Python专家， 请编写函数:{task}",
        "reflect": "请审查代码的算法效率:\n任务:{task}\n代码:{content}",
        "refine": "请根据反馈优化代码:\n任务:{task}\n反馈:{feedback}",
    }

    code_agent = ReflectionAgent(name="我的代码生成助手",
                                 llm=llm,
                                 custom_prompts=code_prompts);

    # 测试使用
    result = general_agent.run("写一篇关于人工智能发展历程的简短文章")
    logger.info(f"最终结果:{result}");


def test_plan_solve_agent():

    # 1. create LLM Client
    llm = LlmClient(provider="llama.cpp");
    
    # 2. 创建自定义 PlanAndSolveAgent
    agent = PlanAndSolveAgent(name="我的规划执行助手", llm=llm);

    # 3. 测试复杂问题
    question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？";
    result = agent.run(question)
    logger.info(f"\n最终结果: {result}")

    # 查看对话历史
    logger.info(f"对话历史: {len(agent.get_history())} 条消息")



def test_memory_agent():

    # 1. create LLM Client
    # llm = LlmClient(provider="llama.cpp");
    agent = SimpleAgent(name="学习助手", llm=LlmClient(provider="llama.cpp"));

    # 第一次对话
    response1 = agent.run("我叫张三, 正在学习Python, 目前掌握了基础语法");
    logger.info(response1)  # "很好！Python基础语法是编程的重要基础..."

    # 第二次对话 (新的会话)
    response2 = agent.run("你还记得我的学习进度吗？")

    logger.info(response2)  # "抱歉，我不知道您的学习进度..."



def  test_memory_rag():
    #print(__path__);
    # 创建LLM实例
    llm = LlmClient()

    # 创建Agent
    agent = SimpleAgent(
        name="智能助手",
        llm=llm,
        system_prompt="你是一个有记忆和知识检索能力的AI助手"
    )

    # 创建工具注册表
    tool_registry = ToolRegistry()

    # 添加记忆工具
    memory_tool = MemoryTool(user_id="user123")
    tool_registry.register_tool(memory_tool)

    # 添加RAG工具
    rag_tool = RAGTool(knowledge_base_path="./knowledge_base")
    tool_registry.register_tool(rag_tool)

    # 为Agent配置工具
    agent.tool_registry = tool_registry

    # 开始对话
    response = agent.run("你好！请记住我叫张三，我是一名Python开发者")
    logger.info(response)


def test_memory_rag_v0():
    # 创建具有记忆能力的Agent
    llm = LlmClient()
    agent = SimpleAgent(name="记忆助手", llm=llm)

    # 创建记忆工具
    memory_tool = MemoryTool(user_id="user123")
    tool_registry = ToolRegistry()
    tool_registry.register_tool(memory_tool)
    agent.tool_registry = tool_registry
    logger.info("\n=== 搜索特定记忆 ===")
    # 搜索前端相关的记忆
    logger.info("🔍 搜索 '前端工程师':")
    result = memory_tool.run({"action": "search", "query":"前端工程师", "limit":3})
    logger.info(result)

    logger.info("\n=== 记忆摘要 ===")
    result = memory_tool.run({"action": "summary"})
    logger.info(result)
    return
    # 体验记忆功能
    logger.info("=== 添加多个记忆 ===")

    # 添加第一个记忆
    result1 = memory_tool.run({"action": "add", "content":"用户张三是一名Python开发者，专注于机器学习和数据分析", "memory_type":"semantic", "importance":0.8}  )
    logger.info(f"记忆1: {result1}")

    # 添加第二个记忆
    result2 = memory_tool.run({"action": "add", "content":"李四是前端工程师，擅长React和Vue.js开发", "memory_type":"semantic", "importance":0.7})
    logger.info(f"记忆2: {result2}")

    # 添加第三个记忆
    result3 = memory_tool.run({"action": "add",  "content":"王五是产品经理，负责用户体验设计和需求分析", "memory_type":"semantic", "importance":0.6})
    logger.info(f"记忆3: {result3}")

    logger.info("\n=== 搜索特定记忆 ===")
    # 搜索前端相关的记忆
    logger.info("🔍 搜索 '前端工程师':")
    result = memory_tool.run({"action": "search", "query":"前端工程师", "limit":3})
    logger.info(result)

    logger.info("\n=== 记忆摘要 ===")
    result = memory_tool.run({"action": "summary"})
    logger.info(result)



    logger.info("===========================");
    # 1. 工作记忆 - 临时信息，容量有限
    memory_tool.run({"action": "add", "content":"用户刚才问了关于Python函数的问题", "memory_type":"working",  "importance":0.6})

    # 2. 情景记忆 - 具体事件和经历
    memory_tool.run({"action":"add",
        "content":"2024年3月15日，用户张三完成了第一个Python项目",
       "memory_type":"episodic",
        "importance":0.8,
        "event_type":"milestone",
        "location":"在线学习平台"
    })

    # 3. 语义记忆 - 抽象知识和概念
    memory_tool.run({"action":"add",
        "content":"Python是一种解释型、面向对象的编程语言",
        "memory_type":"semantic",
        "importance":0.9,
        "knowledge_type":"factual"
    })

    # 4. 感知记忆 - 多模态信息
    memory_tool.run({"action":"add",
        "content":"用户上传了一张Python代码截图，包含函数定义",
        "memory_type":"perceptual",
        "importance": 0.7,
        "modality":"image",
        "file_path":"./uploads/code_screenshot.png"
    })

    logger.info("\n=== 搜索特定记忆 ===")
    # 搜索前端相关的记忆
    logger.info("🔍 搜索 '前端工程师':")
    result = memory_tool.run({"action": "search", "query":"前端工程师", "limit":3})
    logger.info(result)

    logger.info("\n=== 记忆摘要 ===")
    result = memory_tool.run({"action": "summary"})
    logger.info(result)



def  test_add_working_semantic_episodic():
    #  # 创建具有记忆能力的Agent
    llm = LlmClient()
    agent = SimpleAgent(name="记忆助手", llm=llm)

    # 创建记忆工具
    memory_tool = MemoryTool(user_id="user123")
    tool_registry = ToolRegistry()
    tool_registry.register_tool(memory_tool)
    agent.tool_registry = tool_registry
    # logger.info("\n=== 搜索特定记忆 ===")
    # # 搜索前端相关的记忆
    # logger.info("🔍 搜索 '前端工程师':")
    # result = memory_tool.run({"action": "search", "query":"前端工程师", "limit":3})
    # logger.info(result)
    logger.info("=1. 工作记忆 - 临时信息，容量有限=======增加 working  one info 用户刚才问了关于Python函数的问题=============")
    # agent.add_message()
    
    result = memory_tool.run({"action": "add", "content": "用户刚才问了关于Python函数的问题", "memory_type": "working", "importance":0.6});
    logger.info(f"result:{result}");
    # logger.info("===2. 情景记忆 - 具体事件和经历=====增加 episodic  one info 2024年3月15日，用户张三完成了第一个Python项目=============")
    # result = memory_tool.run({"action": "add", "content": "2024年3月15日，用户张三完成了第一个Python项目", "memory_type": "episodic", "importance":0.8, "event_type": "milestone", "localtion":"在线学习平台"});
    # logger.info(f"result:{result}");



    # logger.info("====3. 语义记忆 - 抽象知识和概念====增加 semantic  one info Python是一种解释型、面向对象的编程语言=============")
    # result = memory_tool.run({"action": "add", "content": "Python是一种解释型、面向对象的编程语言", "memory_type": "episodic", "semantic":0.9, "knowledge_type": "factual"});
    # logger.info(f"result:{result}");

    logger.info("====4. 感知记忆 - 多模态信息====增加 perceptual  one info 用户上传了一张Python代码截图，包含函数定义=============")
    result = memory_tool.run({"action": "add", "content": "用户上传了一张Python代码截图，包含函数定义", "memory_type": "episodic", "file_path":"./uploads/code_screenshot.png", "modality": "image"});
    logger.info(f"result:{result}");


def  test_search_working_semantic_episodic():
    #  # 创建具有记忆能力的Agent
    llm = LlmClient()
    agent = SimpleAgent(name="记忆助手", llm=llm)

    # 创建记忆工具
    memory_tool = MemoryTool(user_id="user123")
    tool_registry = ToolRegistry()
    tool_registry.register_tool(memory_tool)
    agent.tool_registry = tool_registry
    # 基础搜索
    logger.info("基础搜索 --->Python编程 ")
    result = memory_tool.run({"action":"search", "query":"Python编程", "limit":5})
    logger.info(f"result:{result}")
    # 指定记忆类型搜索
    logger.info("指定记忆类型搜索 --->学习进度 ")
    result = memory_tool.run({"action":"search",
        "query":"学习进度",
        "memory_type":"episodic",
        "limit":3
    })
    logger.info(f"result:{result}")
    # 多类型搜索
    logger.info("多类型搜索 --->函数定义 ")
    result = memory_tool.run({"action":"search", "query":"函数定义",
        "memory_types":"semantic,episodic",
        "min_importance":0.5
    })
    logger.info(f"result:{result}")



# 三种遗忘策略的使用：
def test_froget_working_semantic_episodic():
    llm = LlmClient()
    agent = SimpleAgent(name="记忆助手", llm=llm)

    # 创建记忆工具
    memory_tool = MemoryTool(user_id="user123")
    tool_registry = ToolRegistry()
    tool_registry.register_tool(memory_tool)
    agent.tool_registry = tool_registry

    logger.info(f"1. 基于重要性的遗忘 - 删除重要性低于阈值的记忆");
    result = memory_tool.run({"action":"forget", "strategy": "importance_based", "threshold":0.2});
    logger.info(f"result:{result}")

    logger.info(f" 2. 基于时间的遗忘 - 删除超过指定天数的记忆");
    result = memory_tool.run({"action":"forget", "strategy":"time_based", "max_age_days":30});
    logger.info(f"result:{result}");

    logger.info(f"3. 基于容量的遗忘 - 当记忆数量超限时删除最不重要的")
    result = memory_tool.run({"action":"forget", "strategy":"capacity_based", "threshold":0.3})
    logger.info(f"result:{result}")


def test_consolidate_working_semantic_episodic():
    llm = LlmClient()
    agent = SimpleAgent(name="记忆助手", llm=llm)

    # 创建记忆工具
    memory_tool = MemoryTool(user_id="user123")
    tool_registry = ToolRegistry()
    tool_registry.register_tool(memory_tool)
    agent.tool_registry = tool_registry

    logger.info(f"1. 将重要的工作记忆转为情景记忆");
    result = memory_tool.run({"action":"consolidate", "from_type": "working", "to_type":"episodic", "importance_threshold":0.7});
    logger.info(f"result:{result}")

    logger.info(f" 2. 将重要的情景记忆转为语义记忆");
    result = memory_tool.run({"action":"consolidate", "from_type":"episodic", "to_type":"semantic", "importance_threshold":0.8});
    logger.info(f"result:{result}");
 


def test_rag01():
    # 创建具有RAG能力的Agent
    llm = LlmClient()
    agent = SimpleAgent(name="知识助手", llm=llm)

    # 创建RAG工具
    rag_tool = RAGTool(
        knowledge_base_path="./knowledge_base",
        collection_name="test_collection",
        rag_namespace="test"
    )

    tool_registry = ToolRegistry()
    tool_registry.register_tool(rag_tool)
    agent.tool_registry = tool_registry

    # 体验RAG功能
    # 添加第一个知识
    # logger.info("添加第一个知识")
    # result1 = rag_tool.run({"action":"add_text", 
    #     "text":"Python是一种高级编程语言，由Guido van Rossum于1991年首次发布。Python的设计哲学强调代码的可读性和简洁的语法。",
    #     "document_id":"python_intro"})
    # logger.info(f"知识1: {result1}")

    # # 添加第二个知识  
    # logger.info("添加第二个知识")
    # result2 = rag_tool.run({"action":"add_text",
    #     "text":"机器学习是人工智能的一个分支，通过算法让计算机从数据中学习模式。主要包括监督学习、无监督学习和强化学习三种类型。",
    #     "document_id":"ml_basics"})
    # logger.info(f"知识2: {result2}")

    # # 添加第三个知识
    # logger.info("添加第三个知识")
    # result3 = rag_tool.run({"action":"add_text",
    #     "text":"RAG（检索增强生成）是一种结合信息检索和文本生成的AI技术。它通过检索相关知识来增强大语言模型的生成能力。",
    #     "document_id":"rag_concept"})
    # logger.info(f"知识3: {result3}")
    # D:/Work/AI/agent/docs/rtc.md
    # logger.info("添加Makdowndow")
    # result2 = rag_tool.run({"action":"add_document",
    #     "file_path":"D:/Work/AI/agent/docs/rtc.md",
    #     "chunk_size":1000,
    #     "chunk_overlap":200
    #     })
    # logger.info(f"知识2: {result2}")
    logger.info("\n=== 搜索知识 ===")
    result = rag_tool.run({"action":"search",
        "query":"RTC",
        "limit":3,
        "min_score":0.1
    })
    logger.info(result)

    logger.info("\n=== 知识库统计 ===")
    result = rag_tool.run({"action":"stats"})
    logger.info(result)



def  test_rag_context():


    # 1. 初始化工具
    memory_tool = MemoryTool(user_id="user123")
    rag_tool = RAGTool(knowledge_base_path="./knowledge_base")

    # 2. 创建 ContextBuilder
    config = ContextConfig(
        max_tokens=30000,
        reserve_ratio=0.2,
        min_relevance=0.0,
        enable_compression=True
    )

    builder = ContextBuilder(
        memory_tool=memory_tool,
        rag_tool=rag_tool,
        config=config
    )

    # 3. 准备对话历史
    conversation_history = [
        Message(content="我正在开发一个数据分析工具", role="user", timestamp=datetime.now()),
        Message(content="很好!数据分析工具通常需要处理大量数据。您计划使用什么技术栈?", role="assistant", timestamp=datetime.now()),
        Message(content="我打算使用Python和Pandas,已经完成了CSV读取模块", role="user", timestamp=datetime.now()),
        Message(content="不错的选择!Pandas在数据处理方面非常强大。接下来您可能需要考虑数据清洗和转换。", role="assistant", timestamp=datetime.now()),
    ]

    # 4. 添加一些记忆
    memory_tool.run({
        "action": "add",
        "content": "用户正在开发数据分析工具,使用Python和Pandas",
        "memory_type": "semantic",
        "importance": 0.8
    })

    memory_tool.run({
        "action": "add",
        "content": "已完成CSV读取模块的开发",
        "memory_type": "episodic",
        "importance": 0.7
    })

    # 5. 构建上下文
    context = builder.build(
        user_query="如何优化Pandas的内存占用?",
        conversation_history=conversation_history,
        system_instructions="你是一位资深的Python数据工程顾问。你的回答需要:1) 提供具体可行的建议 2) 解释技术原理 3) 给出代码示例"
    )

    logger.info("=" * 80)
    logger.info("构建的上下文:")
    logger.info("=" * 80)
    logger.info(context)
    logger.info("=" * 80)



def test_rag_context_class():
    # from agents import SimpleAgent, LlmClient, ToolRegistry
    # from agents.context import ContextBuilder, ContextConfig
    # from agents.tools import MemoryTool, RAGTool

    class ContextAwareAgent(SimpleAgent):
        """具有上下文感知能力的 Agent"""

        def __init__(self, name: str, llm: LlmClient, **kwargs):
            super().__init__(name=name, llm=llm, system_prompt=kwargs.get("system_prompt", ""))

            # 初始化上下文构建器
            self.memory_tool = MemoryTool(user_id=kwargs.get("user_id", "default"))
            self.rag_tool = RAGTool(knowledge_base_path=kwargs.get("knowledge_base_path", "./kb"))

            self.context_builder = ContextBuilder(
                memory_tool=self.memory_tool,
                rag_tool=self.rag_tool,
                config=ContextConfig(max_tokens=4000)
            )

            self.conversation_history = []

        def run(self, user_input: str) -> str:
            """运行 Agent,自动构建优化的上下文"""

            # 1. 使用 ContextBuilder 构建优化的上下文
            optimized_context = self.context_builder.build(
                user_query=user_input,
                conversation_history=self.conversation_history,
                system_instructions=self.system_prompt
            )

            # 2. 使用优化后的上下文调用 LLM
            messages = [
                {"role": "system", "content": optimized_context},
                {"role": "user", "content": user_input}
            ]
            response = self.llm.invoke(messages)

            # 3. 更新对话历史
            from agents.core.message import Message
            from datetime import datetime

            self.conversation_history.append(
                Message(content=user_input, role="user", timestamp=datetime.now())
            )
            self.conversation_history.append(
                Message(content=response, role="assistant", timestamp=datetime.now())
            )

            # 4. 将重要交互记录到记忆系统
            self.memory_tool.run({
                "action": "add",
                "content": f"Q: {user_input}\nA: {response[:200]}...",  # 摘要
                "memory_type": "episodic",
                "importance": 0.6
            })

            return response

    # 使用示例
    agent = ContextAwareAgent(
        name="数据分析顾问",
        llm=LlmClient(),
        system_prompt="你是一位资深的Python数据工程顾问。",
        user_id="user123",
        knowledge_base_path="./data_science_kb"
    )

    response = agent.run("如何优化Pandas的内存占用?")
    print(response)



if __name__ == "__main__":

      # 创建具有记忆能力的Agent
    # llm = LlmClient()
    # agent = SimpleAgent(name="记忆助手", llm=llm)

    # # 创建记忆工具
    # memory_tool = MemoryTool(user_id="user123")
    # tool_registry = ToolRegistry()
    # tool_registry.register_tool(memory_tool)
    # agent.tool_registry = tool_registry
    #test_swiatch_provider()
    # test_simaple_agent()
    #test_reflection_agent()
    # test_plan_solve_agent()
    #test_memory_agent()
    

    # test_memory_rag()
    # test_memory_rag_v0()

    # 三种遗忘策略的使用：
    #test_froget_working_semantic_episodic();
    # test_search_working_semantic_episodic( );
    # test_consolidate_working_semantic_episodic()
    # test_search_working_semantic_episodic();
    # test_rag01()
    # 
    # test_rag_context();
    test_rag_context_class()