"""
Docstring for example003.Executor
执行器模块


"""


from llm_client import AgentsLLM;
from typing import List, Dict;
from ExecutorPromptTemplate import EXECUTOR_PROMPT_TEMPLATE;

class Executor:
    def __init__(self, llm_client: AgentsLLM):
        self.llm_client = llm_client;

    def execute(self, question: str, plan: List[str]) -> str:
         

        """
        Docstring for execute
        """


        history = [];
        for i, step in enumerate(plan):
            print(f"\n--- 执行计划步骤 {i+1}/{len(plan)}: {step} ---");
            current_step = step;
            history_str = "\n".join(history);
            prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                question=question,
                plan="\n".join(plan),
                history=history_str,
                current_step=current_step
            );
            messages = [{"role": "user", "content": prompt}];
            response_text = self.llm_client.think(messages=messages) or "";

            history.append(f"步骤 {i+1}:{step}\n 结果: {response_text}\n\n");
            print(f"✅ 步骤 {i+1} 已完成，结果: {response_text}")

        # 循环结束后，最后一步的响应就是最终答案
        final_answer = response_text
        return final_answer