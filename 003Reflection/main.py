




# 编写一个Python函数，找出1到n之间所有的素数 (prime numbers)



from ReflectionAgent import ReflectionAgent;
from llm_client import AgentsLLM;



if __name__ == "__main__":
    llm_client = AgentsLLM();
    reflection_agent = ReflectionAgent(llm_client, max_iterations=3);
    
    task = "编写一个Python函数，找出1到n之间所有的素数 (prime numbers)";
    final_code = reflection_agent.run(task);