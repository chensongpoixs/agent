

from unicodedata import name
from urllib import response
from agents  import llm  ,  Config 
from typeing import Optional
from  agents import Agent
from agents import LlmClient
from agents import Message;
import re


class SimpleAgent(Agent):
    def __init__(
            self, 
            name: str, 
            llm: LlmClient,
            system_prompt: Optional[str] = None,
            config: Optional[Config] = None,
            tool_registry: Optional["ToolRegistry"] = None,
            enable_tool_calling:    bool = True):
        super().__init__(name=name, llm=llm, system_prompt=system_prompt, config=config);
        self.tool_registry = tool_registry
        self.enable_tool_calling = enable_tool_calling
        print(f"✅ {name} 初始化完成，工具调用: {'启用' if self.enable_tool_calling else '禁用'}")

    def run(self, input_text: str, max_tool_iterations: int = 3, **kwargs) -> str:
        """运行Agent"""
        print(f"🤖 {self.name} 收到输入: {input_text}");
        # 构建初始消息列表
        messages = [];

        # 添加系统信息（可能）
        enhanced_system_prompt = self._get_enhanced_system_prompt();
        messages.append({"role": "system", "content": enhanced_system_prompt});


        # 添加历史消息
        for msg in self.get_history():
            messages.append({"role": msg.role, "content": msg.content});
        

        # 添加当前用户输入
        messages.append({"role": "user", "content": input_text});

        # 如果没有启用工具调用
        if not self.enable_tool_calling:
            response = self.llm.invoke(messages=messages, kwargs=kwargs);
            self.add_message(message=Message(content=input_text, role="user"));
            self.add_message(message=Message(content=response, role="assistant"));
            print(f"✅ {self.name} 响应完成");
            return response
        
        # 支持多轮工具调的逻辑
        return self._run_with_tools(messages, input_text, max_tool_iterations, **kwargs)
         
        # return response
    

    def _get_enhanced_system_prompt(self) -> str:
        """构建增强的系统提示词，包含工具信息"""
        base_prompt = self.system_prompt or "你是一个有用的AI助手。"

        if not self.enable_tool_calling or not self.tool_registry:
            return base_prompt

        # 获取工具描述
        tools_description = self.tool_registry.get_tools_description()
        if not tools_description or tools_description == "暂无可用工具":
            return base_prompt

        tools_section = "\n\n## 可用工具\n"
        tools_section += "你可以使用以下工具来帮助回答问题:\n"
        tools_section += tools_description + "\n"

        tools_section += "\n## 工具调用格式\n"
        tools_section += "当需要使用工具时，请使用以下格式:\n"
        tools_section += "`[TOOL_CALL:{tool_name}:{parameters}]`\n"
        tools_section += "例如:`[TOOL_CALL:search:Python编程]` 或 `[TOOL_CALL:memory:recall=用户信息]`\n\n"
        tools_section += "工具调用结果会自动插入到对话中，然后你可以基于结果继续回答。\n"

        return base_prompt + tools_section
    

    """
    工具使用
    """
    def _run_with_tools(self, messages: list, input_text: str, max_tool_iterations: int, **kwargs) -> str:
        current_iteration = 0;
        final_response = "";

        while current_iteration < max_tool_iterations:
            # 调用LLM
            response = self.llm.invoke(messages, kwargs);

            # 检查是否有工具调用
            tool_calls = self._parse_tool_calls(response);
            
            if tool_calls:
                print(f"🔧 检测到 {len(tool_calls)} 个工具调用");
                
                # 执行所有工具调用并收集结果
                tool_results = [];
                clean_reponse = response;

                for call in tool_calls:
                    result = self._ex

    """
    @author: chensong
    @date: 2026-01-27
    解析文本中的工具调用
    """
    def _parse_tool_calls(self, text: str) -> list:
        pattern = r'\[TOOL_CALL:([^:]+):([^\]]+)\]';
        matches = re.findall(pattern=pattern, text = text);
        tool_calls = [];
        for tool_name, parameters in matches:
            tool_calls.append({
                'tool_name': tool_name.strip(),
                'parameters': parameters.strip(),
                'original': f'[TOOL_CALL:{tool_name}:{parameters}]'
            });

        return tool_calls;


    """
    @author: chensong
    执行工具调用
    """
    def _execute_tool_call(self, tool_name: str, parameters: str) -> str:
        if not self.tool_registry:
            return f"❌ 错误:未配置工具注册表";
        try:
            # 智能参数解析
            if tool_name == 'calculator':
                # 计算器工具之间转入表达式
                result = self.tool_registry.ex



