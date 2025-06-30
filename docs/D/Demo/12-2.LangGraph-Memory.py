from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
anthropic_group_id = os.getenv('ANTHROPIC_BASE_URL')


llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=anthropic_api_key,
    openai_api_base=anthropic_group_id
)


checkpointer = InMemorySaver()


@tool
def get_weather(city: str) -> str:
    """获取城市天气"""
    return f"城市{city}的天气是晴天"


agent = create_react_agent(
    model=llm,
    tools=[get_weather],
    prompt="你是一个天气助手，请根据用户的问题，使用工具获取当前天气",
    checkpointer=checkpointer,
)

config = {
    "configurable":
        {
            "thread_id": "123"
        }
}

def print_detailed_process(user_input, result):
    """打印详细的调用过程"""
    print("=" * 60)
    print(f"👤 用户输入: {user_input}")
    print("-" * 60)
    
    # 遍历所有消息，显示详细过程
    for i, message in enumerate(result['messages']):
        message_type = type(message).__name__
        print(f"步骤 {i+1}: {message_type}")
        
        if message_type == 'HumanMessage':
            print(f"👤 用户: {message.content}")
            
        elif message_type == 'AIMessage':
            # 检查是否有工具调用
            if hasattr(message, 'tool_calls') and message.tool_calls:
                if message.content:
                    print(f"🤖 AI思考: {message.content}")
                print(f"🔧 准备调用工具:")
                for j, tool_call in enumerate(message.tool_calls):
                    print(f"   工具 {j+1}: {tool_call['name']}")
                    print(f"   参数: {tool_call['args']}")
                    print(f"   调用ID: {tool_call['id']}")
            else:
                # 最终 AI 回复
                print(f"🤖 AI最终回复: {message.content}")
        
        elif message_type == 'ToolMessage':
            print(f"⚙️  工具 '{message.name}' 返回结果: {message.content}")
            print(f"   对应调用ID: {message.tool_call_id}")
        
        print()
    
    print("=" * 60)
    print()

# 使用流式处理来更好地观察过程
def print_stream_process(user_input, agent, config):
    """使用流式处理显示详细过程"""
    print("=" * 60)
    print(f"👤 用户输入: {user_input}")
    print("-" * 60)
    
    step_count = 0
    for chunk in agent.stream(
        {"message": [{"role": "user", "content": user_input}]},
        config=config,
        stream_mode="updates"
    ):
        step_count += 1
        print(f"步骤 {step_count}:")
        for node_name, node_output in chunk.items():
            if 'messages' in node_output:
                for message in node_output['messages']:
                    message_type = type(message).__name__
                    
                    if message_type == 'AIMessage':
                        if hasattr(message, 'tool_calls') and message.tool_calls:
                            if message.content:
                                print(f"🤖 [{node_name}] AI思考: {message.content}")
                            for tool_call in message.tool_calls:
                                print(f"🔧 [{node_name}] 调用工具: {tool_call['name']}")
                                print(f"   参数: {tool_call['args']}")
                        else:
                            print(f"🤖 [{node_name}] AI回复: {message.content}")
                    
                    elif message_type == 'ToolMessage':
                        print(f"⚙️  [{node_name}] 工具返回: {message.content}")
        print()
    
    print("=" * 60)
    print()

# 第一次对话 - 使用流式处理
print("🌟 第一次对话 - 流式处理")
user_input_1 = "上海今天天气怎么样？"
print_stream_process(user_input_1, agent, config)

# 第二次对话 - 使用流式处理  
print("🌟 第二次对话 - 流式处理")
user_input_2 = "北京今天天气怎么样？"
print_stream_process(user_input_2, agent, config)

# 第三次对话 - 测试记忆功能
print("🌟 第三次对话 - 测试记忆功能")
user_input_3 = "刚才我问了哪些城市的天气？"
print_stream_process(user_input_3, agent, config)

