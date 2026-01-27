"""
Docstring for example003.Planner
规划器模块


"""


from llm_client import AgentsLLM;
from typing import List, Dict;
from plan_prompt_template import PLANNER_PROMPT_TEMPLATE;

class Planner:
    def __init__(self, llm_client: AgentsLLM):
        self.llm_client = llm_client;

    """
        Docstring for plan
        
        :param self: Description
        :param question: Description
        :type question: str
        :return: Description
        :rtype: List[str]
    """
    def plan(self, question: str) -> List[str]:
        

        
        prompt =  PLANNER_PROMPT_TEMPLATE.format(question=question);
        # 调用 LLM 客户端生成计划
        messages = [{"role": "user", "content": prompt}];
        response_text = self.llm_client.think(messages=messages) or "";
        print(f"完整响应文本: {response_text}");
        # 提取 Python 列表格式的计划
        try:
            plan_start = response_text.index("```python") + len("```python");
            plan_end = response_text.index("```", plan_start);
            plan_str = response_text[plan_start:plan_end].strip();
            plan = eval(plan_str);
            if isinstance(plan, list) and all(isinstance(step, str) for step in plan):
                return plan;
            else:
                print("警告：解析的计划格式不正确，返回空计划。");
                return [];
        except (ValueError, SyntaxError) as e:
            print(f"错误：无法解析计划，返回默认计划。详情: {e}");

        return [f"计划回答问题: {question}"]



