


# my_main.py
from dotenv import load_dotenv
from core.llm import LlmClient    # 注意:这里导入我们自己的类



# from agents import create_calculator_registry

# 加载环境变量
load_dotenv()



def test_swiatch_provider():
    
    # 实例化我们重写的客户端，并指定provider
    llm = LlmClient(provider="modelscope1") 
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