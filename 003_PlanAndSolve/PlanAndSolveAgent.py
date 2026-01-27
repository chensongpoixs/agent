
"""
Docstring for 003_PlanAndSolve.PlanAndSolveAgent
"""


from llm_client import AgentsLLM;
from Planner import Planner;
from Executor import Executor;
from typing import List, Dict;

class PlanAndSolveAgent:
    """
        初始化智能体，同时创建规划器和执行器实例。
    """
    def __init__(self, llm_client: AgentsLLM):
        
        self.llm_client = llm_client;
        self.planner = Planner(llm_client);
        self.executor = Executor(llm_client);

    """
        运行智能体的完整流程:先规划，后执行。
    """
    def run(self, question: str) -> str:
        print(f"\n--- 开始处理问题 ---\n问题: {question}")
        print(f"\n=== 规划阶段 ===");
        # 1. 调用规划器生成计划
        plan = self.planner.plan(question);
        if not plan:
            print("错误：未能生成有效计划，流程终止。");
            return "抱歉，无法生成解决方案。"
        print(f"生成的计划: {plan}");
        
        print(f"\n=== 执行阶段 ===");
        # 2. 调用执行器执行计划
        final_answer = self.executor.execute(question, plan);
        print(f"\n ---任务完成--- \n最终答案: {final_answer}");
        return final_answer