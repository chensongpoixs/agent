


# my_main.py
from dotenv import load_dotenv
from agents.core.llm_client import LlmClient    # 注意:这里导入我们自己的类
 
from agents.agent.simple_agent import SimpleAgent
from agents.tools.registry import ToolRegistry
from agents.tools.async_executor import AsyncToolExecutor
from agents.tools.builtin.calculator import CalculatorTool
from agents.agent.react_agent import ReActAgent
from agents.agent.reflection_agent import ReflectionAgent
# from agents import create_calculator_registry

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
    print("ModelScope Response:")
    for chunk in response_stream:
        # chunk在my_llm库中已经打印过一遍，这里只需要pass即可
        print(chunk, end="", flush=True)
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
    print("=== 测试1:基础对话 ===")
    basic_agent = SimpleAgent(
        name="基础助手",
        llm=llm,
        system_prompt="你是一个友好的AI助手，请用简洁明了的方式回答问题。"
    )

    response1 = basic_agent.run("你好，请介绍一下自己")
    print(f"基础对话响应: {response1}\n")

    # 测试2:带工具的Agent
    print("=== 测试2:工具增强对话 ===")
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
    print(f"工具增强响应: {response2}\n")

    # 测试3:流式响应
    print("=== 测试3:流式响应 ===")
    print("流式响应: ", end="")
    chunk_data = "";
    for chunk in basic_agent.stream_run("请解释什么是人工智能"):
        # print(f"{chunk}");
        #
        #pass  # 内容已在stream_run中实时打印
        pass

    # 测试4:动态添加工具
    print("\n=== 测试4:动态工具管理 ===")
    print(f"添加工具前: {basic_agent.has_tools()}")
    basic_agent.add_tool(calculator)
    print(f"添加工具后: {basic_agent.has_tools()}")
    print(f"可用工具: {basic_agent.list_tools()}")

    # 查看对话历史
    print(f"\n对话历史: {len(basic_agent.get_history())} 条消息")




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
    print(f"最终结果:{result}");

if __name__ == "__main__":
    #test_swiatch_provider()
    # test_simaple_agent()
    test_reflection_agent()