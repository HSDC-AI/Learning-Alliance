from operator import add
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, AIMessage
from pydantic import BaseModel
from IPython.display import Image, display
from typing import Annotated, TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.constants import START, END
from langgraph.graph import StateGraph

load_dotenv()

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
anthropic_group_id = os.getenv('ANTHROPIC_BASE_URL')


llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=anthropic_api_key,
    openai_api_base=anthropic_group_id
)


# 输入的状态
class InputState(TypedDict):
    user_input: str

# 输出的状态


class OutputState(TypedDict):
    graph_output: str

# 传递的状态


class OverallState(TypedDict):
    foo: str        # 节点间传递的中间数据
    input: InputState
    output: OutputState

# 内部私有状态
class PrivateState(TypedDict):
    bar: str


def node_1(state: InputState) -> OverallState:
    return {"foo": state["user_input"] + ">是一个"}


def node_2(state: OverallState) -> PrivateState:
    return {"bar": state["foo"] + ">非常"}


def node_3(state: PrivateState) -> OutputState:
    return {"graph_output": state["bar"] + ">厉害的人"}


builder = StateGraph(OverallState, input=InputState, output=OutputState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)

graph = builder.compile()

print(graph.invoke({"user_input": "小明"}))


with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    list_field: Annotated[list[int], add]
    extra_field: int


def node(state: State) -> State:
    return {"messages": [{"role": "user", "content": "Hello, world!"}]}


class OverallState(BaseModel):
    a: str


def node(state: OverallState) -> OverallState:
    return {"a": "good"}


class OverallState(BaseModel):
    a: str


def node(state: OverallState) -> OverallState:
    return {"a": "good"}


# State  消息传递
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    list_field: Annotated[list[int], add]
    extra_field: int


def node1(state: State) -> State:
    new_message = AIMessage(content="Hello")
    return {"messages": [new_message], "list_field": [10], "extra_field": 10}


def node2(state: State) -> State:
    new_message = AIMessage(content="world!")
    return {"messages": [new_message], "list_field": [20], "extra_field": 20}


graph = (StateGraph(State)
         .add_node("node1", node1)
         .add_node("node2", node2)
         .add_edge(START, "node1")
         .add_edge("node1", "node2")
         .add_edge("node2", END).compile()
         )
input_message = {"role": "user", "content": "Hi"}

result = graph.invoke({"messages": [input_message], "list_field": [1, 2, 3]})
print(result)



# class MessagesState(TypedDict):
#     messages: Annotated[list[AnyMessage], add_messages]
    




# Node 节点
print("\n" + "=" * 20 + "Node 节点" + "=" * 20 + "\n")
import time
from langgraph.types import CachePolicy
from langchain_core.runnables import RunnableConfig
from langgraph.cache.memory import InMemoryCache

class State(TypedDict):
    number: int
    user_id: str
    
class ConfigSchema(TypedDict):
    user_id: str
    
def node_1(state: State, config: RunnableConfig):
    time.sleep(3)
    user_id = config["configurable"]["user_id"]
    return {"number": state["number"] + 1, "user_id": user_id}


builder = StateGraph(State, config_schema=ConfigSchema)

builder.add_node("node_1", node_1, cache_policy=CachePolicy(ttl=5))

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

graph = builder.compile(cache=InMemoryCache())

# print("第一次调用（会执行3秒）：")
# print(graph.invoke({"number": 5}, config={"configurable": {"user_id": "123"}}, stream_mode="updates"))

# print("第二次调用（应该从缓存返回，瞬间完成）：")
# print(graph.invoke({"number": 5}, config={"configurable": {"user_id": "123"}}, stream_mode="updates"))

# print("第三次调用（不同user_id，瞬间完成，userid是123）：")
# print(graph.invoke({"number": 5}, config={"configurable": {"user_id": "456"}}, stream_mode="updates"))

# with open("graph_cache.png", "wb") as f:
#     f.write(graph.get_graph().draw_mermaid_png())




# Edges 边
print("\n" + "=" * 20 + "Edges 边" + "=" * 20 + "\n")

class State(TypedDict):
    number: int

def node_1(state: State) -> State:
    return {"number": state["number"] + 1}

builder = StateGraph(State)
builder.add_node("node1", node_1)

# def routing_func(state: State) -> str:
#     if state["number"] > 5:
#         return "node1"
#     else:
#         return END
def routing_func(state: State) -> bool:
    if state["number"] > 5:
        return True
    else:
        return False

# builder.add_edge("node1", END)

# builder.add_conditional_edges(START, routing_func)
builder.add_conditional_edges(START, routing_func, {True: "node1", False: END})

graph = builder.compile()

print(graph.invoke({"number": 4}))
print(graph.invoke({"number": 6}))
with open("graph_edges.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())



print("\n" + "=" * 20 + "Edges 边 - Send 动态路由" + "=" * 20 + "\n")

from langgraph.types import Send
class State(TypedDict):
    message: Annotated[list[str], add]
    
class PrivateState(TypedDict):
    msg: str

def node_1(state: PrivateState) -> State:
    res = state["msg"] + "@@@"
    return {"message": [res]}

def routing_func(state: State):
    result = []
    for msg in state["message"]:
        result.append(Send(
            "node1",
            {"msg": msg}
        ))
    return result
    

builder = StateGraph(State)
builder.add_node("node1", node_1)

builder.add_conditional_edges(START, routing_func, ["node1"])
builder.add_edge("node1", END)

graph = builder.compile()

print(graph.invoke({"message": ["Hello", "World"]}))

with open("graph_send.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())




print("\n" + "=" * 20 + "Edges 边 - Command 命令" + "=" * 20 + "\n")

from langgraph.types import Command
class State(TypedDict):
    message: Annotated[list[str], add]
    
def node_1(state: State) -> State:
    new_message = []
    for msg in state["message"]:
        new_message.append( msg + "!!!")
    return Command(
        goto=END,
        update={"message": new_message}
    )
    
builder = StateGraph(State)
builder.add_node("node1", node_1)
builder.add_edge(START, "node1")

graph = builder.compile()

print(graph.invoke({"message": ["Hello", "World"]}))

with open("graph_command.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())


print("\n" + "=" * 20 + "SubGraph 子图" + "=" * 20 + "\n")

from langgraph.graph import MessagesState

class State(TypedDict):
    messages: Annotated[list[str], add]
    
def sub_node_1(state: State) -> MessagesState:
    return {"messages": ["hahah hahah haha"]}

sub_builder = StateGraph(State)
sub_builder.add_node("sub_node_1", sub_node_1)
sub_builder.add_edge(START, "sub_node_1")
sub_builder.add_edge("sub_node_1", END) 

sub_graph = sub_builder.compile()

builder = StateGraph(State)
builder.add_node("sub_graph", sub_graph)
builder.add_edge(START, "sub_graph")
builder.add_edge("sub_graph", END)

graph = builder.compile()

print(graph.invoke({"messages": ["Hello"]}))

# with open("graph_subgraph.png", "wb") as f:
#     f.write(graph.get_graph().draw_mermaid_png())
    
    
    
print("\n" + "=" * 20 + "流式输出" + "=" * 20 + "\n")

# for chunk in graph.stream({"messages": ["Hello"]}, stream_mode="values"):
    # print(chunk)

from langgraph.config import get_stream_writer

class State(TypedDict):
    query: str
    answer: str
    
def node_1(state: State):
    writer = get_stream_writer()
    writer({"自定义Key":"在节点内返回自定义信息"})
    writer("直接返回字符串")
    return {"answer": "some data"}

graph = (StateGraph(State)
         .add_node("node1", node_1)
         .add_edge(START, "node1")
         .add_edge("node1", END)
         .compile()
         )

for chunk in graph.stream({"query": "Hello"}, stream_mode="custom"):
    print(chunk)

    