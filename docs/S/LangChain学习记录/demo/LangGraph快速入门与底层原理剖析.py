from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from typing import Literal
from docs.S.LangChain学习记录.demo.getchat import get_chat
from langgraph.graph import END, StateGraph, MessagesState

# 定义一个查询工具
@tool
def search(query: str):
    """模拟一个搜索工具"""
    if "上海" in query.lower() or "Shanghai" in query.lower():
        return "现在是30度 高温"
    return "现在是35度 特别热"

tools = [search]

# 创建工具节点
tool_node = ToolNode(tools)

llm = get_chat("gpt-4o")

#将工具和模型绑定
model = llm.bind_tools(tools)

# 判断是否继续执行
def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return END

# 定义调用模型
def call_model(message: MessagesState):
    messages = message['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

# 定义一个状态图
workflow = StateGraph(MessagesState)
# 添加节点
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
# 设置agent为入口
workflow.set_entry_point("agent")

# 添加条件边
workflow.add_conditional_edges(
    "agent",
    should_continue
)

# 添加普通边
workflow.add_edge("tools", 'agent')

# 初始化在内存中的持久状态
checkpoint = MemorySaver()

# 编译图 编辑过程中传递checkpointer 是可选的
app = workflow.compile(checkpointer=checkpoint)

# 执行图
final_state = app.invoke(
    {
        "messages": [
            HumanMessage(content="上海的天气怎么样?")
        ]
    },
    config={"configurable": {"thread_id": 42}}
)

result = final_state["messages"][-1].content

print(final_state)

final_state = app.invoke(
    {
        "messages": [
            HumanMessage(content="我刚刚问了什么")
        ]

    },
    config={"configurable": {"thread_id": 42}}
)

result = final_state["messages"][-1].content

print(result)