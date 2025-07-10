
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, MessagesState, END, START
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langgraph.types import Command, interrupt
from typing import Literal

load_dotenv()

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
anthropic_group_id = os.getenv('ANTHROPIC_BASE_URL')

llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=anthropic_api_key,
    openai_api_base=anthropic_group_id
)


def call_model(state: MessagesState):
    res = llm.invoke(state["messages"])
    return {"messages": [res]}


def human_approval(state: MessagesState) -> Command[Literal["call_model", END]]:
    is_approved = interrupt(
        {
            "是否继续执行？"
        }
    )
    if is_approved:
        return Command(goto="call_model")
    else:
        return Command(goto=END)


checkpointer = InMemorySaver()

graph = (StateGraph(MessagesState)
         .add_node("call_model", call_model)
         .add_node("human_approval", human_approval)
         .add_edge(START, "human_approval")
         .compile(checkpointer=checkpointer)
         )

config = {
    "configurable": {
        "thread_id": "123"
    }
}

for chunk in graph.stream(
    {"messages": [{"role": "user", "content": "湖南的省会是哪里？"}]},
    config=config, 
    stream_mode="messages"
):
    print(chunk["messages"][-1].pretty_print())


# for chunk in graph.stream(
#     Command(resume=True),
#     config=config,
#     stream_mode="values"
# ):
#     print(chunk["messages"][-1].pretty_print())


# for chunk in graph.stream({"messages": [{"role": "user", "content": "湖北呢？"}]}, config=config, stream_mode="values"):
#     print(chunk["messages"][-1].pretty_print())

# for chunk in graph.stream({"messages": [{"role": "user", "content": "北京呢？"}]}, config=config, stream_mode="values"):
#     print(chunk["messages"][-1].pretty_print())


print("\n" + "=" * 20 + "Time Travel 时间回溯" + "=" * 20 + "\n")

from typing_extensions import NotRequired
from typing import TypedDict
class State(TypedDict):
    author: NotRequired[str]
    joke: NotRequired[str]


def author_node(state: State):
    prompt = "帮我推荐一个收人环境的作家，只需要给出作家的名字即可"
    author = llm.invoke(prompt)
    return {"author": author}

def joke_node(state: State):
    prompt = f"用作家{state["author"]}的风格，写一个100字以内的笑话, 并带上他的名字"
    joke = llm.invoke(prompt)
    return {"joke": joke}

builder = StateGraph(State)
builder.add_node("author_node", author_node)
builder.add_node("joke_node", joke_node)

builder.add_edge(START, "author_node")
builder.add_edge("author_node", "joke_node")
builder.add_edge("joke_node", END)

checkpointer = InMemorySaver()

graph = builder.compile(checkpointer=checkpointer)

with open("graph_state.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())

import uuid
config = {
    "configurable": {
        "thread_id": str(uuid.uuid4())
    }
}

state = graph.invoke({}, config=config)
print("\n" + "-" * 20 + "初始状态" + "-" * 20 + "\n")
print(state["author"])
print(state["joke"])



print("\n" + "-" * 20 + "状态历史" + "-" * 20 + "\n")
states = list(graph.get_state_history(config=config))
for state in states:
    print(state.next)
    print(state.config["configurable"]["checkpoint_id"])
    print("-" * 20)
    
print("\n" + "-" * 20 + "回溯状态" + "-" * 20 + "\n")
selected_state = states[1]
print(selected_state.next)
print(selected_state.values)

    
print("\n" + "-" * 20 + "回溯" + "-" * 20 + "\n")
new_config = graph.update_state(selected_state.config, values={"author": "郭德纲"})
print(new_config)
state = graph.invoke(None, config=new_config)
print(state["author"])
print(state["joke"])





