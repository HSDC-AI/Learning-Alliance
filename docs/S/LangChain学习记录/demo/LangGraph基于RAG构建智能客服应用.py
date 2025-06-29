import json

import streamlit as st
from langchain_core.messages import AIMessageChunk, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from docs.S.LangChain学习记录.demo.getchat import get_key, get_chat

def get_rag_graph(selected_kbs, KBS):
    # 根据选择的知识库从字典中获取工具
    tools = [KBS[k] for k in selected_kbs]
    # 创建工具节点
    tool_node = ToolNode(tools)

    # 定义调用模型的内部函数
    def call_model(state):
        llm = get_chat("gpt-4o")
        llm_with_tools = llm.bind_tools(tools)
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    # 创建状态图
    workflow = StateGraph(MessagesState)

    # 添加节点到状态图
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    # 添加条件边
    workflow.add_conditional_edges("agent", tools_condition)

    # 添加普通边
    workflow.add_edge("tools", "agent")

    # 设置图入口
    workflow.set_entry_point("agent")

    # 创建内存保存期
    checkpointer = MemorySaver()

    # 编译应用
    app = workflow.compile(checkpointer=checkpointer)

    # 生成对应的图片
    graph_png = app.get_graph().draw_mermaid_png()

    with open("rag.png", "wb") as f:
        f.write(graph_png)
    return app

# 定义函数用于处理图的响应
def graph_response(graph, input):

    # 调用图并处理事件
    for event in graph.invoke(
        {"messages": input},
        config={"configurable": {"thread_id": 42}},
        stream_mode="messages"
    ):
        if type(event[0]) == AIMessageChunk:
            # 是否有工具调用
            if len(event[0].tool_calls):
                # 添加工具调用信息到会话状态
                st.session_state["rag_tool_calls"].append(
                    {
                        "status": "正在查询中....",
                        "knowledge_base": event[0].tool_calls[0]["name"].replace("_knowledge_base_tool", ""),
                        "query": ""
                    }
                )
            # 生成事件内容
            yield event[0].content
        elif type(event[0]) == ToolMessage:
            # 创建状态占位符
            status_placeholder = st.empty()
            # 显示查询状态
            with (status_placeholder.status("正在查询。。。", expanded=True) as s):
                # 显示调用的知识库
                st.write("已调用 `", event[0].name.replace("_knowledge_base_tool", ""), "` 知识库正在查询")
                # 初始化继续保存标志
                continue_save = False
                # 检查是否需要继续保存
                if len(st.session_state["rag_tool_calls"]):
                    if "content" not in st.session_state["rag_tool_calls"][-1].keys():
                        continue_save = True
                # 显示知识库检索结果
                st.write("知识库检索结果：")
                st.code(event[0].content, wrap_lines=True)
                # 更新状态
                s.update(label="已完成知识检索", expanded=False)
            # 如果需要继续保存
            if continue_save:
                st.session_state["rag_tool_calls"][-1]["status"] = "已完成知识库检索！"
                st.session_state["rag_tool_calls"][-1]["content"] = json.loads(event[0].content)
            else:
                st.session_state["rag_tool_calls"].append(
                    {
                        "status": "已完成知识库检索",
                        "knowledge_base": event[0].name.replace("_knowledge_base_tool", ""),
                        "content": json.loads(event[0].content),
                    }
                )

# 定义函数用于获取RAG聊天响应
def get_rag_chat_response(platform, model, temperature, input, selected_tools, KBS):
    app = get_rag_graph(platform, model, temperature, selected_tools, KBS)
    return graph_response(graph=app, input=input)

# 定义函数用于显示聊天历史
def display_chat_history():
    # 遍历聊天历史中的所有消息
    for message in st.session_state["rag_chat_history_with_tool_call"]:
        with st.chat_message(message["role"], avatar=get_img_base64()):
            pass