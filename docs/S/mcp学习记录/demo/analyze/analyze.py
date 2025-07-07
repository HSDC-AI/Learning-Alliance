from langgraph.graph import StateGraph, END
from langchain.tools import tool
import markdown
from typing import TypedDict, Annotated
import operator
import json
from docs.S.LangChain学习记录.demo.getchat import get_chat


# ===== 工具封装 =====
# 修复工具调用方式
@tool
def get_monitoring_data(start_time: str, end_time: str) -> str:
    """获取监控数据"""
    return f"模拟监控数据 from {start_time} to {end_time}"


@tool
def get_change_list(start_time: str, end_time: str) -> str:
    """获取变更清单"""
    return "变更清单：变更A、变更B..."


@tool
def get_query_list(start_time: str, end_time: str) -> str:
    """获取查询列表"""
    return "查询清单：慢SQL1，慢SQL2..."


@tool
def rga_search(input_text: str) -> str:
    """RGA 搜索"""
    return f"RGA 检索结果：与'{input_text}'相关的记录"

# ===== 状态结构 - 使用 TypedDict =====
class State(TypedDict):
    start_time: str
    end_time: str
    monitoring_data: Annotated[str, operator.add]
    anomaly_detected: bool
    change_list: Annotated[str, operator.add]
    query_list: Annotated[str, operator.add]
    rga_result: Annotated[str, operator.add]
    root_cause_report_markdown: Annotated[str, operator.add]
    root_cause_report_html: Annotated[str, operator.add]

# ===== LLM 初始化 =====
llm = get_chat(model="gpt-4o")

# ===== 工具函数 =====
def markdown_to_html(markdown_text: str) -> str:
    return markdown.markdown(markdown_text, extensions=['tables', 'fenced_code'])

# ===== 各节点逻辑 - 修复工具调用 =====
def fetch_monitoring_data(state: State) -> dict:
    # 确保参数存在
    if "start_time" not in state or "end_time" not in state:
        raise ValueError("缺少 start_time 或 end_time 参数")

    # 修复：使用正确的工具调用方式
    result = get_monitoring_data.run({
        "start_time": state["start_time"],
        "end_time": state["end_time"]
    })
    return {"monitoring_data": result}

def detect_anomaly(state: State) -> dict:
    if "monitoring_data" not in state:
        raise ValueError("缺少监控数据")

    prompt = f"请判断以下监控数据是否存在突刺行为：{state['monitoring_data']}"
    result = llm.invoke(prompt)
    return {"anomaly_detected": "是" in result.content}

def no_anomaly_report(state: State) -> dict:
    report = "未发现突刺，无需进一步分析。"
    return {
        "root_cause_report_markdown": report,
        "root_cause_report_html": markdown_to_html(report)
    }

def fetch_change_and_query(state: State) -> dict:
    if "start_time" not in state or "end_time" not in state:
        raise ValueError("缺少 start_time 或 end_time 参数")

    # 修复：使用正确的工具调用方式
    change_result = get_change_list.run({
        "start_time": state["start_time"],
        "end_time": state["end_time"]
    })
    query_result = get_query_list.run({
        "start_time": state["start_time"],
        "end_time": state["end_time"]
    })

    return {
        "change_list": change_result,
        "query_list": query_result
    }

def rga_analysis(state: State) -> dict:
    if "change_list" not in state or "query_list" not in state:
        raise ValueError("缺少变更列表或查询列表")

    merged_text = f"{state['change_list']}\n{state['query_list']}"

    # 修复：使用正确的工具调用方式
    rga_result = rga_search.run({"input_text": merged_text})
    return {"rga_result": rga_result}

def root_cause_analysis(state: State) -> dict:
    required_fields = ["monitoring_data", "change_list", "query_list", "rga_result"]
    for field in required_fields:
        if field not in state:
            raise ValueError(f"缺少必要字段: {field}")

    prompt = (
        f"请根据以下信息输出突刺分析和根因判断：\n"
        f"监控数据：{state['monitoring_data']}\n"
        f"变更清单：{state['change_list']}\n"
        f"查询清单：{state['query_list']}\n"
        f"RGA 结果：{state['rga_result']}\n"
        "请用清晰的 Markdown 格式输出分析内容（包括突刺判断、可能原因、建议）"
    )
    result = llm.invoke(prompt)
    report_md = result.content
    return {
        "root_cause_report_markdown": report_md,
        "root_cause_report_html": markdown_to_html(report_md)
    }

# ===== 构建 LangGraph =====
graph = StateGraph(State)

# 节点注册
graph.add_node("fetch_monitoring", fetch_monitoring_data)
graph.add_node("detect_anomaly", detect_anomaly)
graph.add_node("no_anomaly_report", no_anomaly_report)
graph.add_node("fetch_change_query", fetch_change_and_query)
graph.add_node("rga_analysis", rga_analysis)
graph.add_node("root_cause_analysis", root_cause_analysis)

# 流程定义
graph.set_entry_point("fetch_monitoring")
graph.add_edge("fetch_monitoring", "detect_anomaly")
graph.add_conditional_edges(
    "detect_anomaly",
    lambda state: "anomaly_detected" if state.get("anomaly_detected") else "no_anomaly",
    {
        "anomaly_detected": "fetch_change_query",
        "no_anomaly": "no_anomaly_report"
    }
)
graph.add_edge("no_anomaly_report", END)
graph.add_edge("fetch_change_query", "rga_analysis")
graph.add_edge("rga_analysis", "root_cause_analysis")
graph.add_edge("root_cause_analysis", END)

# 编译图
graph_app = graph.compile()

# 保存生成的图片
graph_png = graph_app.get_graph().draw_mermaid_png()
with open("plan.png", "wb") as f:
    f.write(graph_png)

# ===== 运行入口 =====
if __name__ == "__main__":
    # 初始状态只包含必需参数
    input_state = {
        "start_time": "2025-06-30 12:00",
        "end_time": "2025-06-30 13:00"
    }

    # 运行图
    try:
        # 使用 invoke 获取最终状态
        final_state = graph_app.invoke(input_state)

        print("\n最终状态:", json.dumps(final_state, indent=2, ensure_ascii=False))

        # 检查报告是否生成
        if "root_cause_report_markdown" in final_state:
            print("\n📄 Markdown 报告：")
            print(final_state["root_cause_report_markdown"])

            with open("root_cause_report.html", "w") as f:
                f.write(final_state["root_cause_report_html"])
            print("\n✅ HTML 报告已写入 root_cause_report.html")
        else:
            print("\n❌ 未生成报告")

    except Exception as e:
        print(f"\n❌ 运行出错: {str(e)}")
        import traceback

        traceback.print_exc()