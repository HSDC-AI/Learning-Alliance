from langgraph.graph import END, StateGraph
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from typing import List, Dict, TypedDict, Annotated, Union, Optional
import operator
import json
import datetime
import os
import time
import re

from docs.S.LangChain学习记录.demo.getchat import get_chat


# ======================
# 1. 封装 MCP 工具客户端
# ======================
class MCPClient:
    @staticmethod
    def get_monitoring_data(start_time: str, end_time: str) -> str:
        """获取指定时间范围内的监控数据"""
        return f"监控数据（{start_time} 至 {end_time}）:\n- CPU峰值80%\n- 内存使用率90%\n- 网络流量突增"

    @staticmethod
    def get_change_list(start_time: str, end_time: str) -> str:
        """获取指定时间范围内的变更清单"""
        return f"变更清单（{start_time} 至 {end_time}）:\n1. 数据库配置更新\n2. 应用版本v2.3部署\n3. 网络策略调整"

    @staticmethod
    def get_query_list(start_time: str, end_time: str) -> str:
        """获取指定时间范围内的慢查询列表"""
        return f"慢查询列表（{start_time} 至 {end_time}）:\n1. SELECT * FROM large_table (耗时12s)\n2. UPDATE user_stats (耗时8s)"

    @staticmethod
    def rga_search(input_text: str) -> str:
        """使用RGA搜索引擎检索相关信息"""
        return f"RGA搜索结果:\n- 相关事件: 数据库维护窗口\n- 相关配置变更: 索引优化\n- 相关告警: 慢查询告警"

    @staticmethod
    def generate_report(report_content: str) -> str:
        """生成Markdown格式的报告文件"""
        # 确保报告目录存在
        os.makedirs("reports", exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/monitoring_report_{timestamp}.md"

        # 创建报告内容
        content = f"# 监控突刺分析报告\n\n{report_content}"

        # 保存到文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        return f"报告已生成: {filename}"

# ======================
# 2. 定义状态结构
# ======================
def merge_dicts(x: dict, y: dict) -> dict:
    """合并两个字典"""
    return {**x, **y}

class AgentState(TypedDict):
    messages: Annotated[
        List[Union[SystemMessage, HumanMessage, AIMessage, ToolMessage]],
        operator.add
    ]
    start_time: Optional[str]
    end_time: Optional[str]
    report_data: Annotated[Dict[str, str], merge_dicts]  # 使用自定义合并函数
    analysis_conclusion: Optional[str]  # 添加分析结论字段
    step_count: int  # 添加步数计数器
    pending_tool_calls: List[dict]  # 存储待处理的工具调用
    last_tool_result: Optional[str]  # 存储上一个工具的结果

# ======================
# 3. 工具调用函数 - 每次只调用一个工具
# ======================
def invoke_tool(state: AgentState) -> AgentState:
    """执行单个工具调用并返回结果"""
    messages = state["messages"]
    last_message = messages[-1]

    print(f"\n{'='*40}")
    print(f"⚙️ ACT节点: 执行工具调用... (步骤 {state.get('step_count', 0)})")
    print(f"最后消息类型: {type(last_message).__name__}")

    # 获取下一个工具调用（从待处理列表中取第一个）
    if not state["pending_tool_calls"]:
        print("⚠️ 警告: 没有待处理的工具调用")
        return state

    tool_call = state["pending_tool_calls"].pop(0)
    func_name = tool_call["function"]["name"]

    print(f"\n🛠️ 调用工具: {func_name}")

    # 安全解析参数
    try:
        args = json.loads(tool_call["function"]["arguments"])
        print(f"参数: {args}")
    except json.JSONDecodeError:
        print("⚠️ 参数解析失败")
        args = {}

    # 处理时间参数 - 如果未提供则使用状态中的时间
    if func_name in ["get_monitoring_data", "get_change_list", "get_query_list"]:
        if "start_time" not in args or not args["start_time"]:
            args["start_time"] = state.get("start_time", "")
        if "end_time" not in args or not args["end_time"]:
            args["end_time"] = state.get("end_time", "")

    # 调用对应的 MCP 工具
    if func_name == "get_monitoring_data":
        result = MCPClient.get_monitoring_data(**args)
        state["report_data"]["monitoring"] = result
    elif func_name == "get_change_list":
        result = MCPClient.get_change_list(**args)
        state["report_data"]["changes"] = result
    elif func_name == "get_query_list":
        result = MCPClient.get_query_list(**args)
        state["report_data"]["queries"] = result
    elif func_name == "rga_search":
        result = MCPClient.rga_search(**args)
        state["report_data"]["rga"] = result
    elif func_name == "generate_report":
        # 组合所有收集的数据作为报告内容
        report_content = "\n\n".join([
            "## 监控数据\n" + state["report_data"].get("monitoring", "无数据"),
            "## 变更清单\n" + state["report_data"].get("changes", "无数据"),
            "## 慢查询\n" + state["report_data"].get("queries", "无数据"),
            "## RGA分析\n" + state["report_data"].get("rga", "无数据"),
            "## 分析结论\n" + state.get("analysis_conclusion", "无分析结果")
        ])
        args["report_content"] = report_content
        result = MCPClient.generate_report(**args)
        state["report_data"]["report"] = result
    else:
        result = f"未知工具: {func_name}"

    print(f"工具结果: {result[:100]}{'...' if len(result) > 100 else ''}")

    # 添加工具响应消息
    tool_message = ToolMessage(
        content=result,
        tool_call_id=tool_call["id"]
    )

    # 保存上一个工具的结果
    state["last_tool_result"] = result

    print(f"{'='*40}\n")

    return {
        "messages": [tool_message],
        "report_data": state["report_data"],
        "analysis_conclusion": state.get("analysis_conclusion", ""),
        "step_count": state.get("step_count", 0) + 1,  # 增加步数计数
        "pending_tool_calls": state["pending_tool_calls"],  # 保留剩余的工具调用
        "last_tool_result": result
    }

# ======================
# 4. 初始化代理模型
# ======================
model = get_chat(model="gpt-4o")

# 定义工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_monitoring_data",
            "description": "获取指定时间范围内的监控数据",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {"type": "string", "description": "开始时间，格式 YYYY-MM-DD HH:MM"},
                    "end_time": {"type": "string", "description": "结束时间，格式 YYYY-MM-DD HH:MM"}
                },
                "required": ["start_time", "end_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_change_list",
            "description": "获取指定时间范围内的变更清单",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {"type": "string", "description": "开始时间，格式 YYYY-MM-DD HH:MM"},
                    "end_time": {"type": "string", "description": "结束时间，格式 YYYY-MM-DD HH:MM"}
                },
                "required": ["start_time", "end_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_query_list",
            "description": "获取指定时间范围内的慢查询列表",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {"type": "string", "description": "开始时间，格式 YYYY-MM-DD HH:MM"},
                    "end_time": {"type": "string", "description": "结束时间，格式 YYYY-MM-DD HH:MM"}
                },
                "required": ["start_time", "end_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rga_search",
            "description": "使用RGA搜索引擎检索相关信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_text": {"type": "string", "description": "搜索关键词"}
                },
                "required": ["input_text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_report",
            "description": "生成Markdown格式的报告文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "report_content": {"type": "string", "description": "报告内容"}
                },
                "required": ["report_content"]
            }
        }
    }
]

# 绑定工具到模型
model_with_tools = model.bind_tools(tools)

# ======================
# 5. 定义节点函数
# ======================
def think_node(state: AgentState) -> AgentState:
    """思考节点：决定下一步行动"""
    current_step = state.get("step_count", 0) + 1
    print(f"\n{'='*40}")
    print(f"🤔 THINK节点: 思考下一步行动... (步骤 {current_step})")
    print(f"当前消息数量: {len(state['messages'])}")

    # 打印上一个工具的结果（如果有）
    if "last_tool_result" in state and state["last_tool_result"]:
        print(f"上一个工具结果: {state['last_tool_result'][:100]}{'...' if len(state['last_tool_result']) > 100 else ''}")

    # 打印当前对话历史
    print("\n对话历史:")
    for i, msg in enumerate(state["messages"][-3:]):  # 只显示最后3条消息
        prefix = f"[{i+1}/{len(state['messages'])}] "
        if isinstance(msg, SystemMessage):
            print(f"{prefix}系统: {msg.content[:60]}{'...' if len(msg.content) > 60 else ''}")
        elif isinstance(msg, HumanMessage):
            print(f"{prefix}用户: {msg.content[:60]}{'...' if len(msg.content) > 60 else ''}")
        elif isinstance(msg, AIMessage):
            content = msg.content or "工具调用"
            print(f"{prefix}AI: {content[:60]}{'...' if len(content) > 60 else ''}")
        elif isinstance(msg, ToolMessage):
            print(f"{prefix}工具: {msg.content[:60]}{'...' if len(msg.content) > 60 else ''}")

    # 如果有待处理的工具调用，直接返回它们
    if state["pending_tool_calls"]:
        print(f"有 {len(state['pending_tool_calls'])} 个待处理的工具调用")
        return {
            "messages": [],  # 不添加新消息
            "analysis_conclusion": state.get("analysis_conclusion", ""),
            "step_count": current_step,  # 更新步数计数
            "pending_tool_calls": state["pending_tool_calls"],
            "last_tool_result": state.get("last_tool_result", None)
        }

    # 调用模型获取响应
    start_time = time.time()
    response = model_with_tools.invoke(state["messages"])
    elapsed = time.time() - start_time

    print(f"\n模型响应时间: {elapsed:.2f}秒")
    if response.content:
        print(f"AI回复: {response.content[:100]}{'...' if len(response.content) > 100 else ''}")

        # 检查是否有分析结论
        if "结论" in response.content or "分析" in response.content:
            state["analysis_conclusion"] = response.content

    # 提取工具调用
    tool_calls = []
    if hasattr(response, 'additional_kwargs') and "tool_calls" in response.additional_kwargs:
        tool_calls = response.additional_kwargs["tool_calls"]
        print(f"请求工具调用: {len(tool_calls)}个")
        for i, call in enumerate(tool_calls):
            print(f"  {i+1}. {call['function']['name']}")

    print(f"{'='*40}\n")

    return {
        "messages": [response],
        "analysis_conclusion": state.get("analysis_conclusion", ""),
        "step_count": current_step,  # 更新步数计数
        "pending_tool_calls": tool_calls,  # 存储所有工具调用
        "last_tool_result": state.get("last_tool_result", None)
    }

def act_node(state: AgentState) -> AgentState:
    """行动节点：执行单个工具调用"""
    return invoke_tool(state)

def should_continue(state: AgentState) -> str:
    """决策函数：判断是否继续循环"""
    last_message = state["messages"][-1] if state["messages"] else None
    current_step = state.get("step_count", 0)

    # 如果步数超过限制，强制结束
    if current_step > 20:
        print("⚠️ 决策: 超过最大步数限制(20)，强制结束")
        return "end"

    # 检查是否有待处理的工具调用
    if state["pending_tool_calls"]:
        print(f"🔧 决策: 有待处理的工具调用 ({len(state['pending_tool_calls'])}个) -> 继续执行行动")
        return "act"

    # 检查是否需要生成报告或声明任务完成
    if last_message and isinstance(last_message, AIMessage) and last_message.content:
        # 检查是否提到报告
        if "报告" in last_message.content or "generate_report" in last_message.content:
            print("📝 决策: 检测到报告相关指令 -> 继续思考")
            return "think"

        # 检查是否声明任务完成
        if "完成" in last_message.content or "结束" in last_message.content or "分析完毕" in last_message.content:
            print("✅ 决策: 检测到任务完成声明")
            return "end"

    # 默认返回思考节点
    print("➡️ 决策: 没有待处理的工具调用，继续思考")
    return "end"

# ======================
# 6. 构建 LangGraph 工作流
# ======================
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("think", think_node)
workflow.add_node("act", act_node)

# 设置入口点
workflow.set_entry_point("think")

# 添加条件边
workflow.add_conditional_edges(
    "think",
    should_continue,
    {
        "act": "act",  # 需要执行工具
        "end": END,    # 结束流程
        "think": "think"  # 继续思考
    }
)

# 添加普通边
workflow.add_edge("act", "think")

# 编译图
agent = workflow.compile()

# ======================
# 7. 运行代理的实用函数
# ======================
def run_analysis(start_time: str, end_time: str) -> str:
    """运行监控突刺分析并返回报告路径"""
    # 初始化状态
    state = {
        "messages": [
            SystemMessage(content="你是一个专业的监控分析专家，负责分析监控数据中的异常突刺。请每次只调用一个工具，然后根据结果决定下一步。"),
            HumanMessage(content=f"分析从 {start_time} 到 {end_time} 的监控数据，识别是否有突刺现象，并生成详细报告。")
        ],
        "start_time": start_time,
        "end_time": end_time,
        "report_data": {},
        "analysis_conclusion": "",
        "step_count": 0,  # 初始化步数计数
        "pending_tool_calls": [],  # 初始无待处理工具调用
        "last_tool_result": None  # 初始无工具结果
    }

    print(f"🔍 开始分析 {start_time} 到 {end_time} 的监控数据...")
    print(f"初始消息: {state['messages'][-1].content[:60]}...")

    # 运行代理
    final_state = None
    step = 1
    for output in agent.stream(state):
        for key, new_state in output.items():
            final_state = new_state
            print(f"\n🔄 步骤 {step} 完成 - 状态更新 (总步数: {final_state.get('step_count', 0)})")
            step += 1

            # 检查是否超过最大步数
            if final_state.get("step_count", 0) > 20:
                print("⚠️ 警告: 超过最大步数限制，强制终止")
                break

    if not final_state:
        print("❌ 错误: 未生成最终状态")
        return "报告生成失败，未生成最终状态"

    # 打印最终状态信息
    print("\n📊 最终状态信息:")
    print(f"总步数: {final_state.get('step_count', 0)}")
    print(f"消息数量: {len(final_state['messages'])}")
    print(f"报告数据键: {list(final_state.get('report_data', {}).keys())}")

    # 提取报告路径
    report_path = None

    print(final_state)
    # 1. 检查是否已生成报告
    if final_state.get("report_generated", False) and "report_data" in final_state and "report" in final_state["report_data"]:
        report_path = final_state["report_data"]["report"]
        # 移除前缀
        prefix = "报告已生成: "
        if isinstance(report_path, str) and report_path.startswith(prefix):
            report_path = report_path[len(prefix):]

    # 2. 如果报告路径未设置，尝试从消息中提取
    if not report_path:
        print("🔄 尝试从消息中提取报告路径...")
        last_message = final_state["messages"][-1] if final_state["messages"] else None
        if last_message and isinstance(last_message, AIMessage) and last_message.content:
            # 使用正则表达式匹配报告文件路径
            pattern = r'reports/monitoring_report_\d{8}_\d{6}\.md'
            match = re.search(pattern, last_message.content)
            if match:
                report_path = match.group(0)

    # 3. 如果仍没有报告路径，手动生成
    if not report_path:
        print("🔄 尝试手动生成报告...")
        # 组合所有收集的数据作为报告内容
        report_content = "\n\n".join([
            "## 监控数据\n" + final_state["report_data"].get("monitoring", "无数据"),
            "## 变更清单\n" + final_state["report_data"].get("changes", "无数据"),
            "## 慢查询\n" + final_state["report_data"].get("queries", "无数据"),
            "## RGA分析\n" + final_state["report_data"].get("rga", "无数据"),
            "## 分析结论\n" + final_state.get("analysis_conclusion", "无分析结果")
        ])

        # 生成报告并返回路径
        generated = MCPClient.generate_report(report_content)
        if "报告已生成: " in generated:
            report_path = generated.split("报告已生成: ")[1]
        else:
            report_path = generated

    return report_path

# ======================
# 8. 主程序
# ======================
if __name__ == "__main__":
    # 设置分析时间范围
    start_time = "2025-06-30 12:00"
    end_time = "2025-06-30 13:00"

    # 运行分析
    report_path = run_analysis(start_time, end_time)

    # 处理结果
    if report_path and os.path.exists(report_path):
        print(f"\n✅ 分析完成！报告已生成: {report_path}")
        print("\n📄 报告内容预览:")
        with open(report_path, 'r', encoding='utf-8') as f:
            print(f.read()[:500] + "...")  # 打印前500个字符作为预览
    else:
        print("\n❌ 报告生成失败")
        print(f"报告路径: {report_path}")

        # 打印工作目录和内容
        print("\n当前工作目录内容:")
        print(os.listdir('.'))

        # 检查reports目录是否存在
        if os.path.exists('reports'):
            print("\nreports目录内容:")
            print(os.listdir('reports'))