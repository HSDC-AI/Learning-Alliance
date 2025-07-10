from typing import TypedDict, Annotated
from operator import add

from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.config import get_stream_writer
from langchain_openai import ChatOpenAI


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

nodes = ["supervisor", "travel", "joke", "couplet", "other"]

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add] # 添加消息
    type: str
    
    
def supervisor_node(state: State):
    """根据用户的问题进行分类，分类的结果保存到Type当中"""
    print(">>> supervisor_node")
    writer = get_stream_writer() # type: ignore
    writer({"node": ">>> supervisor_node"})
    prompt = """
    你是一个专业的客服助手，负责对用户的问题进行分类
    如果用户问的问题是旅游规划相关的就返回  travel
    如果用户问的问题是笑话相关的就返回  joke
    如果用户问的问题是对联相关的就返回  couplet
    如果用户问的问题是其他问题就返回  other
    除了这几个选项不返回任何其他内容
    """
    prompts = [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": state["messages"][0]
        }
    ]
    if "type" in state:
        writer({"supervisor_step": f"已获得：{state["type"]} Agent处理结果" })
        return {"type": END}
    else:
        res = llm.invoke(prompts)
        typeRes = res.content
        writer({"supervisor_step": f"问题分类结果：{typeRes}"})
        if typeRes in nodes:
            return {"type": typeRes}
        else:
            return ValueError("type is not in nodes")
        
# 动态路由
def routing_func(state: State):
    writer = get_stream_writer() # type: ignore
    writer({"node": ">>> routing_func"})
    if state["type"] == "travel":
        return "travel_node"
    elif state["type"] == "joke":
        return "joke_node"
    elif state["type"] == "couplet":
        return "couplet_node"
    elif state["type"] == END:
        writer({"state": ">>> END"})
        return END
    else:
        return "other_node"


def travel_node(state: State):
    print(">>> travel_node")
    writer = get_stream_writer() # type: ignore
    writer({"node": ">>> travel_node"})
    return {"messages": [HumanMessage(content="travel_node")], "type": "travel"}
    
def joke_node(state: State):
    print(">>> joke_node")
    writer = get_stream_writer() # type: ignore
    writer({"node": ">>> joke_node"})
    prompt = """
    你是一个专业的笑话助手，负责根据用户的问题生成一个笑话
    用户的问题是：{user_question}
    请返回一个笑话
    除了笑话不返回任何其他内容
    """
    prompts = [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": state["messages"][0]
        }
    ]
    res = llm.invoke(prompts)
    jokeRes = res.content
    writer({"joke_node": f"笑话：{jokeRes}"})
    return {"messages": [AIMessage(content=jokeRes)], "type": "joke"}
    
def couplet_node(state: State):
    print(">>> couplet_node")
    writer = get_stream_writer() # type: ignore
    writer({"node": ">>> couplet_node"})
    
    
    
    
    
    
    
    return {"messages": [HumanMessage(content="couplet_node")], "type": "couplet"}
    
def other_node(state: State):
    print(">>> other_node")
    writer = get_stream_writer() # type: ignore
    writer({"node": ">>> other_node"})
    return {"messages": [HumanMessage(content="我暂时无法回答这个问题")], "type": "other"}
    

builder = StateGraph(State) 

builder.add_node("supervisor_node", supervisor_node)
builder.add_node("travel_node", travel_node)
builder.add_node("joke_node", joke_node)
builder.add_node("couplet_node", couplet_node)
builder.add_node("other_node", other_node)

builder.add_edge(START, "supervisor_node")
builder.add_conditional_edges(
    "supervisor_node",
    routing_func,
    ["travel_node", "joke_node", "couplet_node", "other_node", END]
)
builder.add_edge("travel_node", "supervisor_node")
builder.add_edge("joke_node", "supervisor_node")
builder.add_edge("couplet_node", "supervisor_node")
builder.add_edge("other_node", "supervisor_node")



graph = builder.compile(checkpointer=InMemorySaver())


if __name__ == "__main__":
    with open("./graph.png", "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())

    config = {
        "configurable": {
            "thread_id": "111test"
        }
    }
    for chunk in graph.stream({"messages": ["给我讲一个笑话"]}, config=config, stream_mode="custom"):
        print(chunk)
    
    # res = graph.invoke({"messages": ["今天天气怎么样"]}, config=config)
    # # print(res["messages"])
    # print(res["messages"][-1].content)



    
    






