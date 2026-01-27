

from ExecutionPrompt import INITIAL_PROMPT_TEMPLATE
from ReflectionPrompt import REFLECT_PROMPT_TEMPLATE
from RefinementPrompt import REFINE_PROMPT_TEMPLATE
from llm_client import AgentsLLM;
from Memory import Memory;

class ReflectionAgent:
    def __init__(self, llm_client: AgentsLLM, max_iterations: int = 3):
        self.llm_client = llm_client
        self.memory = Memory();
        self.max_iterations = max_iterations;




    def run(self, task: str) -> str:
        print(f"Starting ReflectionAgent for task: {task}");
        # 初始执行阶段
        print("\n --- 初始执行阶段 ---");
        
        initial_prompt = INITIAL_PROMPT_TEMPLATE.format(task=task)
        code_attempt = self._get_llm_response(initial_prompt)
        # 记录初始尝试的代码
        self.memory.add_record("execution", code_attempt)

        # 2. 迭代循环: 反思与优化
        for iteration in range(self.max_iterations):
            print(f"\n--- 迭代循环 第 {iteration + 1}/{self.max_iterations} 轮 ---");
            # 反思阶段
            print("\n--- 正在进行反思... ---");
            last_code = self.memory.get_last_execution()
            reflect_prompt = REFLECT_PROMPT_TEMPLATE.format(task=task, code=last_code)
            feedback = self._get_llm_response(reflect_prompt)
            # 记录反思反馈
            self.memory.add_record("reflection", feedback);



            if "无需改进" in feedback:
                print("\n✅ 反思认为代码已无需改进，任务完成。");
                break;

            # 优化阶段
            print("\n--- 正在进行代码优化... ---");
            refine_prompt = REFINE_PROMPT_TEMPLATE.format(
                task=task,
                last_code_attempt=code_attempt,
                feedback=feedback
            )
            refined_code = self._get_llm_response(refine_prompt)
            self.memory.add_record("refinement", refined_code)

        final_code = self.memory.get_last_execution()
        print(f"\n--- 任务完成 ---\n最终生成的代码:\n```python\n{final_code}\n```")
        return final_code
    

    """一个辅助方法，用于调用LLM并获取完整的流式响应。"""
    def _get_llm_response(self, prompt: str) -> str:
        
        messages = [{"role": "user", "content": prompt}]
        response_text = self.llm_client.think(messages=messages) or ""
        return response_text