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

from langgraph.types import interrupt, Command

@tool(return_direct=True)
def book_hotel(hotel_name: str):
    """预订酒店的工具。当用户提到要预订、预定任何酒店时，必须调用此工具。
    参数:
    hotel_name: 用户想要预订的酒店名称
    """
    res = interrupt(
        f"正在准备执行 `book_hotel` 工具，预订酒店: {hotel_name}。"
        "请选择ok表示同意，选择edit提出补充意见"
    )
    
    if res["type"] == "ok":
        pass
    elif res["type"] == "edit":
        hotel_name = res["args"]["hotel_name"]
    else:
        return f"预定宾馆{hotel_name}失败" 
    return f"预定宾馆{hotel_name}成功"


agent = create_react_agent(
    model=llm,
    tools=[book_hotel],
    prompt="""你是一个酒店预订助手。
    当用户说要预订、预定任何酒店时，你必须调用book_hotel工具来完成预订。
    不要只是询问用户，而是要直接使用工具进行
    预订操作。""",
    checkpointer=checkpointer,
)

config = {
    "configurable":
        {
            "thread_id": "124"
        }
}

print("=== 第一次流式调用（会被中断）===")
for msg in agent.stream(
    {"messages": [{"role":"user", "content":"我想预订希尔顿酒店"}]},
    config=config
):
    print("第一次流:", msg)
    print("\n")

print("=== 恢复执行（发送确认信号）===")
for msg in agent.stream(
    Command(resume={"type": "ok"}),
    config=config
):
    print("恢复流:", msg)
    # 安全地访问消息内容
    try:
        if "tools" in msg and "messages" in msg["tools"] and msg["tools"]["messages"]:
            print("工具消息内容:", msg["tools"]["messages"][-1].content)
        elif "agent" in msg and "messages" in msg["agent"] and msg["agent"]["messages"]:
            print("代理消息内容:", msg["agent"]["messages"][-1].content)
        else:
            print("消息结构:", list(msg.keys()))
    except (KeyError, IndexError, AttributeError) as e:
        print(f"访问消息内容时出错: {e}")
    print("\n")