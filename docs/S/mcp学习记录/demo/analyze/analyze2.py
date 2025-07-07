from langgraph.graph import StateGraph, END
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import markdown
from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator
import json
from docs.S.LangChain学习记录.demo.getchat import get_chat

# ===== MCP 协议工具封装 =====
@tool
def get_monitoring_data(start_time: str, end_time: str) -> str:
    """获取指定时间范围内的监控数据"""
    return f"监控数据（{start_time} 至 {end_time}）: CPU峰值80%, 内存使用率90%, 网络流量突增"


@tool
def get_change_list(start_time: str, end_time: str) -> str:
    """获取指定时间范围内的变更清单"""
    return f"变更清单（{start_time} 至 {end_time}）:\n1. 数据库配置更新\n2. 应用版本v2.3部署\n3. 网络策略调整"


@tool
def get_query_list(start_time: str, end_time: str) -> str:
    """获取指定时间范围内的慢查询列表"""
    print(1)
    return f"慢查询列表（{start_time} 至 {end_time}）:\n1. SELECT * FROM large_table (耗时12s)\n2. UPDATE user_stats (耗时8s)"


@tool
def get_query_list2(start_time: str, end_time: str) -> str:
    """获取指定时间范围内的慢查询列表2"""
    print(2)
    return f"慢查询列表2（{start_time} 至 {end_time}）:\n1. SELECT * FROM large_table2 (耗时12s)\n2. UPDATE user_stats2(耗时8s)"

@tool
def rga_search(input_text: str) -> str:
    """使用RGA搜索引擎检索相关信息"""
    return f"RGA搜索结果:\n- 相关事件: 数据库维护窗口\n- 相关配置变更: 索引优化\n- 相关告警: 慢查询告警"


@tool
def detect_anomaly(monitoring_data: str) -> str:
    """分析监控数据并检测是否存在异常突刺"""
    return "检测到内存使用率和网络流量存在明显突刺"


@tool
def generate_report(analysis_data: str) -> str:
    """根据分析数据生成根因报告"""
    return "根因分析报告:\n## 突刺分析\n监控数据显示内存使用率和网络流量存在明显突刺\n## 可能原因\n1. 慢查询导致资源争用\n2. 新版本应用内存泄漏\n## 建议\n1. 优化慢查询\n2. 回滚应用版本检查"


# 创建工具列表
tools = [
    get_monitoring_data,
    get_change_list,
    get_query_list,
    get_query_list2,
    rga_search,
    detect_anomaly,
    generate_report
]

tool_executor = ToolExecutor(tools)

# ===== MCP 协议状态结构 =====
class MCPState(TypedDict):
    """MCP协议状态，包含整个分析过程的信息"""
    start_time: str
    end_time: str
    # 代理消息历史
    messages: Annotated[List[Dict[str, Any]], operator.add]
    # 中间分析结果
    monitoring_data: Optional[str]
    change_list: Optional[str]
    query_list: Optional[str]
    rga_result: Optional[str]
    anomaly_detected: Optional[bool]
    # 最终报告
    root_cause_report_markdown: Optional[str]
    root_cause_report_html: Optional[str]


# ===== LLM 初始化 =====
llm = get_chat(model="gpt-4o")


# ===== MCP 工具函数 =====
def markdown_to_html(markdown_text: str) -> str:
    """将Markdown转换为HTML"""
    return markdown.markdown(markdown_text, extensions=['tables', 'fenced_code'])


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """执行指定工具并返回结果"""
    for t in tools:
        if t.name == tool_name:
            return t.run(tool_input)
    return f"错误: 找不到工具 {tool_name}"


# ===== 消息序列化函数 =====
def serialize_message(message: Any) -> Dict:
    """序列化LangChain消息对象为字典"""
    if isinstance(message, (HumanMessage, AIMessage, ToolMessage)):
        return {
            "type": type(message).__name__,
            "content": message.content,
            "additional_kwargs": message.additional_kwargs
        }
    return str(message)


def serialize_state(state: Dict) -> Dict:
    """序列化整个状态为JSON可序列化的格式"""
    serialized = state.copy()

    # 序列化消息列表
    if "messages" in serialized:
        serialized["messages"] = [serialize_message(msg) for msg in serialized["messages"]]

    return serialized


# ===== 创建 MCP 代理 =====
# 定义代理提示模板
prompt = (
    f"请你分析间的系统突刺情况。你可以调用tools里面的所有工具"
    "请按需多轮调用，最终输出一个根因分析报告（Markdown 格式）。"
)

MCP_PROMPT = ChatPromptTemplate.from_messages([
    ("system", prompt),
    MessagesPlaceholder(variable_name="messages"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 创建代理
agent = create_openai_tools_agent(
    llm,
    tools,
    MCP_PROMPT
)

# 创建智能体节点
agent_node = ToolCallingAgentNode.from_llm_and_tools(
    llm=llm,
    tools=tools,
    prompt=MCP_PROMPT
)

# 创建代理执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True
)


# ===== MCP 代理节点 =====
def agent_node(state: MCPState) -> dict:
    """代理节点：执行一次 agent 调用或处理工具结果"""
    input_data = {
        "messages": state["messages"],
        "start_time": state["start_time"],
        "end_time": state["end_time"]
    }

    response = agent_executor.invoke(input_data)

    # 收集新消息
    new_messages = []

    # 如果直接输出报告
    if "output" in response:
        new_messages.append(AIMessage(content=response["output"]))
        return {
            "messages": new_messages,
            "root_cause_report_markdown": response["output"]
        }

    # 否则是中间步骤（调用了工具）
    if "intermediate_steps" in response and response["intermediate_steps"]:
        action, observation = response["intermediate_steps"][-1]
        tool_name = action.tool
        tool_input = json.loads(action.tool_input) if isinstance(action.tool_input, str) else action.tool_input

        # 调用工具
        tool_result = execute_tool(tool_name, tool_input)

        # 更新 state 中间字段
        if tool_name == "get_monitoring_data":
            state["monitoring_data"] = tool_result
        elif tool_name == "get_change_list":
            state["change_list"] = tool_result
        elif tool_name == "get_query_list":
            state["query_list"] = tool_result
        elif tool_name == "get_query_list2":
            state["query_list"] = tool_result + "\n" + (state["query_list"] or "")
        elif tool_name == "rga_search":
            state["rga_result"] = tool_result
        elif tool_name == "detect_anomaly":
            state["anomaly_detected"] = "突刺" in tool_result

        # 添加工具响应消息
        new_messages.append(ToolMessage(content=tool_result, name=tool_name))

    return {
        "messages": new_messages
    }


# ===== MCP 报告生成节点 =====
def report_node(state: MCPState) -> dict:
    """生成最终报告"""
    if state.get("root_cause_report_markdown"):
        return {
            "root_cause_report_html": markdown_to_html(state["root_cause_report_markdown"])
        }
    return {}


# ===== MCP 状态图构建 =====
graph = StateGraph(MCPState)

# 添加节点
graph.add_node("agent", agent_node)
graph.add_node("report", report_node)

# 设置入口点
graph.set_entry_point("agent")

# 定义边
graph.add_edge("report", END)


# 添加条件边
def route_after_agent(state: MCPState) -> str:
    """根据代理输出决定下一步"""
    if state.get("root_cause_report_markdown"):
        return "report"
    else:
        return "agent"

graph.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "report": "report",
        "agent": "agent"
    }
)

# 编译图
mcp_app = graph.compile()

# 保存生成的图片
graph_png = mcp_app.get_graph().draw_mermaid_png()
with open("plan.png", "wb") as f:
    f.write(graph_png)

# ===== MCP 协议运行入口 =====
def run_mcp_analysis(start_time: str, end_time: str) -> Dict:
    """运行MCP协议分析"""
    # 初始状态
    initial_state = {
        "start_time": start_time,
        "end_time": end_time,
        "messages": [
            HumanMessage(content=f"请分析从 {start_time} 到 {end_time} 的性能突刺问题。")
        ],
        "monitoring_data": None,
        "change_list": None,
        "query_list": None,
        "rga_result": None,
        "anomaly_detected": None,
        "root_cause_report_markdown": None,
        "root_cause_report_html": None
    }

    # 运行MCP协议
    final_state = mcp_app.invoke(initial_state, {"recursion_limit": 10})

    # 生成HTML报告
    if final_state.get("root_cause_report_markdown"):
        final_state["root_cause_report_html"] = markdown_to_html(
            final_state["root_cause_report_markdown"]
        )

    return final_state


# ===== 主程序 =====
if __name__ == "__main__":
    # 运行MCP分析
    result = run_mcp_analysis(
        start_time="2025-06-30 12:00",
        end_time="2025-06-30 13:00"
    )

    # 输出结果
    print("\n" + "=" * 50)
    print("MCP协议分析完成！")
    print("=" * 50)

    # 输出中间结果
    print("\n监控数据:")
    print(result.get("monitoring_data", "无"))

    print("\n变更清单:")
    print(result.get("change_list", "无"))

    print("\n慢查询列表:")
    print(result.get("query_list", "无"))

    print("\nRGA搜索结果:")
    print(result.get("rga_result", "无"))

    # 输出最终报告
    if result.get("root_cause_report_markdown"):
        print("\n" + "=" * 50)
        print("根因分析报告 (Markdown):")
        print("=" * 50)
        print(result["root_cause_report_markdown"])

        # 保存HTML报告
        with open("mcp_root_cause_report.html", "w") as f:
            f.write(result["root_cause_report_html"])
        print("\n✅ HTML报告已保存到 mcp_root_cause_report.html")
    else:
        print("\n❌ 未生成分析报告")

    # 序列化状态并保存
    serialized_state = serialize_state(result)
    with open("mcp_analysis_state.json", "w") as f:
        json.dump(serialized_state, f, indent=2, ensure_ascii=False)
    print("✅ 完整分析状态已保存到 mcp_analysis_state.json")

    # 打印序列化后的消息
    if "messages" in serialized_state:
        print("\n消息历史:")
        for i, msg in enumerate(serialized_state["messages"]):
            print(f"[消息 {i + 1}] {msg.get('type', '未知类型')}: {msg.get('content', '无内容')}")