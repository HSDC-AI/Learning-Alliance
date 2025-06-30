import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain_mcp_adapters.tools import load_mcp_tools # type: ignore
import os
load_dotenv()

class MCPClient:
    def __init__(self):
        #初始化会话和客户端对象
        self.session: Optional[ClientSession] = None
        # 异步上下文管理器工具
        self.exit_stack = AsyncExitStack()
        self.llm = ChatOpenAI(
            model="gpt-4o",
            openai_api_key=os.getenv("ANTHROPIC_API_KEY"),  # 这里用你的 Anthropic Key
            base_url="https://globalai.vip/v1"
        )
        self.tools = []
        
    async def connect_to_server(self, server_script_path: str):
        """连接到 MCP 服务器

        Args:
            server_script_path: 服务器脚本的路径 (.py 或 .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("服务器脚本必须是.py 或 .js 文件")
        
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        self.tools = await load_mcp_tools(self.session)
        
        print("\n已连接到服务器，工具包括：", [tool.name for tool in self.tools])

        
        
    async def process_query(self, query: str) -> str:
        """使用 Claude 和可用的工具处理查询"""
        
        translate_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个有用的AI助手。"),
            ("user", "{input}"),
            ("assistant", "{agent_scratchpad}")
        ])
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=translate_prompt
        )

        # 创建智能体执行器
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        result = await agent_executor.ainvoke({"input": query})

        print(result)  # 打印回答结果
        return result["output"]
    
    async def chat_loop(self):
        """运行交互式聊天循环"""
        print("欢迎使用 MCP 客户端！")
        print("输入你的查询或输入 'quit' 退出。")
        
        while True:
            try:
                query = input("\n查询: ").strip()
                
                if query.lower() == 'quit':
                    print("退出聊天。")
                    break
                
                response = await self.process_query(query)
                print("\n" + response)
                
            except Exception as e:
                print(f"\n错误: {str(e)}")
                
    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()
        
    # 主入口
    
async def main():
        if len(sys.argv) < 2:
            # uv run client.py ../weather/weather/weather.py
            print("使用方法: python client.py <path_to_server_script>")
            sys.exit(1)
        
        client = MCPClient()
        try:
            await client.connect_to_server(sys.argv[1])
            await client.chat_loop()
        finally:
            await client.cleanup()
        
if __name__ == "__main__":
        import sys
        asyncio.run(main())
        
        
        
        

                
        
        
    
        
        

        
        
        



