from datetime import datetime
import os
from dotenv import load_dotenv 

load_dotenv()
minimax_api_key = os.getenv('MINIMAX_API_KEY')  
minimax_group_id = os.getenv('MINIMAX_GROUP_ID')  
minimax_base_url = os.getenv('MINIMAX_BASE_URL_V1') 

LANGSMITH_API_KEY = os.getenv('LANGSMITH_API_KEY') 
LANGSMITH_ENDPOINT = os.getenv('LANGSMITH_ENDPOINT') 

os.environ['LANGSMITH_TRACING'] = "true"
os.environ['LANGSMITH_PROJECT'] = "test-001"

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')  
anthropic_group_id = os.getenv('ANTHROPIC_BASE_URL')  

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=anthropic_api_key,
    openai_api_base=anthropic_group_id
)

# print(llm.invoke("你好"))

from langgraph.prebuilt import create_react_agent
# agent = create_react_agent(
#     model=llm,
#     tools=[],
#     prompt="你是一个只能回答问题，不能做其他事情的助手",
# )

# result = agent.invoke({"message": [{"role":"user", "content":"你好"}]})
# print(result)

from langchain_core.tools import tool

@tool
def get_current_time(input: str) -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

agent = create_react_agent(
    model=llm,
    tools=[get_current_time],
    prompt="你是一个智能助手，请根据用户的问题，使用工具获取当前时间",
)

print("=" * 50)
print("方法1: 使用 invoke() 获取完整结果")
print("=" * 50)

result = agent.invoke({"message": [{"role":"user", "content":"今天的日期是什么？"}]})

# 打印最终答案
final_answer = result['messages'][-1].content
print(f"最终答案: {final_answer}")

print("\n" + "=" * 50)
print("方法2: 使用 stream() 流式输出过程")
print("=" * 50)

for chunk in agent.stream(
    {"message": [{"role":"user", "content":"今天几点了？"}]},
    stream_mode="messages"
):
    message, metadata = chunk
    # 只打印有内容的消息
    if hasattr(message, 'content') and message.content:
        print(f"输出: {message.content}")
    # 如果是工具调用，显示调用信息
    elif hasattr(message, 'tool_calls') and message.tool_calls:
        print(f"工具调用: {message.tool_calls[0]['name']}")







# 