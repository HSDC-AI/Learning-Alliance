from datetime import datetime
import os
import asyncio
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack
from typing import Optional, List

load_dotenv()


class MCPClient:
    def __init__(self):
        self.exit_stack = AsyncExitStack() # 异步上下文管理器工具
        self.llm = OpenAI(
            model=os.getenv("DEEPSEEK_R1_MODEL"),
            api_key=os.getenv("DEEPSEEK_API_KEY"),  # 这里用你的 Anthropic Key
            base_url=os.getenv("DEEPSEEK_BASE_URL")
        )
       
        self.session: Optional[ClientSession] = None # 和服务器端通信的 会话对象
        
    async def connect_to_server(self, server_script_path: str):
        """连接到 MCP 服务器

        Args:
            server_script_path: 服务器脚本的路径 (.py 或 .js)
        """
        is_python = server_script_path.endswith(".py")
        is_javascript = server_script_path.endswith(".js")
        if not is_python and not is_javascript:
            raise ValueError("服务器脚本必须是 .py 或 .js 文件")
        
        command = "python" if is_python else "node"
        
        # 构建 MCP 服务器参数，包含启动命令，基本路径参数 环境变量
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        # 启动 MCP 工具服务进程 并建立 stdio 通信
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        
        # 拆包通信通道，读取服务端返回诗句，并向服务端发送请求
        self.stdio, self.write = stdio_transport

        # 创建MCO客户端会话对象
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )
        response = await self.session.initialize()
        tools = response.tools
        print("\n 已连接服务，支持一下工具：", [tool.name for tool in tools])
        

        # 加载MCP工具
        # self.tools = await load_mcp_tools(self.session)
    async def process_query(self, query: str) -> str:
        """处理用户查询"""
        messages = [
            {"role": "user", "content": query}
        ]
        response = await self.session.list_tools()
        available_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in response.tools
        ]
        
        # 提取问题的关几次，对文件名进行生成
        # 在接收到用户提问后就应该生成出最后输出的 md文件档的文件名
        # 因为导出时若在生成文件名会导致部分组件无法识别该名称
        keyword_match = re.search(pattern=r"(关于|分析|查询|搜索|查看)([^的\s, . / ? \n]+)", string=query)
        keyword = keyword_match.group(2) if keyword_match else "分析对象"
        safe_keyword= re.sub(pattern=r"[\\/:*?\"<>|]", repl="", string=keyword)[:20]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        md_filename = f"sentiment_{safe_keyword}_{timestamp}.md"
        md_path = os.path.join("./sentiment_reports", md_filename)
        
        # 更新查询没见过文件名添加到原始查询中，使大模型在调用工具随时可以识别到该信息
        # 然后调用  plan_tool_usage 获取工具调用计划
        query = query.strip() + f"[md_filename={md_filename}] [md_path={md_path}]"
        messages = [{
            "role": "user",
            "content": query
        }]
        tool_plan = await self.plan_tool_usage(messages, available_tools)
        
        tool_outputs = []
        
        #一次执行工具调用，并收集结果
        for step in tool_plan:
            tool_name = step["tool"]
            tool_args = step["arguments"]
            for key, val in tool_args.items():
                if isinstance(val, list) and val.startswith("{{") and val.endswith("}}"):
                    ref_key = val.strip("{}")
                    resolved_val = tool_outputs.get(ref_key, val)
                    tool_args[key] = resolved_val
                
            # 注入同意的文件名或路径 
            if tool_name == "analyze_sentiment" and "filename" not in tool_args:
                tool_args["filename"] = md_filename
            
            if tool_name == "send_email" and "attachment_path" not in tool_args:
                tool_args["attachment_path"] = md_path
            
            # 执行工具调用
            result = await self.session.call_tool(
                tool_name,
                tool_args
            )
            tool_outputs[tool_name] = result.content[0].text
            messages.append({
                "role": "tool",
                "tool_call_id": tool_name,
                "content": result.content[0].text,
            })
        # 调用大模型  生成回复信息 并保存结果
        final_response = self.llm.chat.completions.create(
            model=os.getenv("DEEPSEEK_R1_MODEL"),
            messages=messages,
        )
        final_output = final_response.choices[0].message.content
        return final_output
        
        
    async def chat_loop(self):
        print("欢迎使用智能舆情分析系统")
        print("输入你的查询或输入 'quit' 退出")
        
        while True:
            try:
                query = input("\n查询: ").strip()
                
                if query.lower() == "quit":
                    print("退出系统")
                    break
                
                response = await self.process_query(query)
            except Exception as e:
                print(f"发生错误: {e}")
                response = "处理查询时出错，请重试"
                
    # async def plan_tool_usage(self, messages: List[Dict], available_tools: List[Dict]) -> List[Dict]:
        
            
        # 将工具输出结果写入到 md 文件中
        



# if __name__ == "__main__":
#     client = MCPClient()