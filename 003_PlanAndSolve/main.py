"""
Docstring for 003_PlanAndSolve.main
"""


from llm_client import AgentsLLM;
from PlanAndSolveAgent import PlanAndSolveAgent;
from Executor import Executor;

# --- 5. 主函数入口 ---
if __name__ == '__main__':
    try:
        llm_client = AgentsLLM()
        agent = PlanAndSolveAgent(llm_client)
        question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
        agent.run(question)
    except ValueError as e:
        print(e)

