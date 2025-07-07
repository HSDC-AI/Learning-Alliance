from langgraph.graph import END, StateGraph
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from typing import List, Dict, TypedDict, Annotated, Union, Optional
import operator
import json
import datetime
import os
import time
import re
import asyncio

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
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/monitoring_report_{timestamp}.md"
        content = f"# 监控突刺分析报告\n\n{report_content}"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"报告已生成: {filename}"


# ======================
# 2. 定义状态结构
# ======================
def merge_dicts(x: dict, y: dict) -> dict:
    return {**x, **y}


class AgentState(TypedDict):
    messages: Annotated[
        List[Union[SystemMessage, HumanMessage, AIMessage, ToolMessage]],
        operator.add
    ]
    start_time: Optional[str]
    end_time: Optional[str]
    report_data: Annotated[Dict[str, str], merge_dicts]
    analysis_conclusion: Optional[str]
    step_count: int
    current_task: Optional[str]
    last_agent_result: Optional[str]


# ======================
# 3. 工具 Agent 封装
# ======================
class ToolAgent:
    def __init__(self, name: str, description: str, tool_func):
        self.name = name
        self.description = description
        self.tool_func = tool_func
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        # 定义工具Agent的状态
        class ToolAgentState(TypedDict):
            input_params: dict
            output_result: Optional[str]

        # 构建工具Agent的工作流
        workflow = StateGraph(ToolAgentState)

        # 添加节点
        workflow.add_node("execute_tool", self._execute_tool_node)
        workflow.add_node("return_result", self._return_result_node)

        # 设置边
        workflow.set_entry_point("execute_tool")
        workflow.add_edge("execute_tool", "return_result")
        workflow.add_edge("return_result", END)

        return workflow.compile()

    def _execute_tool_node(self, state: dict) -> dict:
        """执行工具函数"""
        print(f"🔧 {self.name} Agent: 正在执行工具...")
        result = self.tool_func(**state["input_params"])
        return {"output_result": result}

    def _return_result_node(self, state: dict) -> dict:
        """返回工具执行结果"""
        print(f"✅ {self.name} Agent: 任务完成")
        return state

    async def run(self, params: dict) -> str:
        """运行工具Agent并返回结果"""
        state = {"input_params": params}
        result = await self.workflow.ainvoke(state)
        return result["output_result"]


# ======================
# 4. 创建工具Agent实例
# ======================
monitoring_agent = ToolAgent(
    name="监控数据获取",
    description="从监控系统获取指定时间范围内的监控数据",
    tool_func=MCPClient.get_monitoring_data
)

change_agent = ToolAgent(
    name="变更清单获取",
    description="获取指定时间范围内的系统变更清单",
    tool_func=MCPClient.get_change_list
)

query_agent = ToolAgent(
    name="慢查询获取",
    description="获取数据库慢查询列表",
    tool_func=MCPClient.get_query_list
)

rga_agent = ToolAgent(
    name="RGA搜索",
    description="使用RGA搜索引擎检索相关信息",
    tool_func=MCPClient.rga_search
)

report_agent = ToolAgent(
    name="报告生成",
    description="生成分析报告文件",
    tool_func=MCPClient.generate_report
)

# 工具Agent映射
TOOL_AGENTS = {
    "get_monitoring_data": monitoring_agent,
    "get_change_list": change_agent,
    "get_query_list": query_agent,
    "rga_search": rga_agent,
    "generate_report": report_agent
}

# ======================
# 5. 协调Agent
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
# 6. 协调Agent工作流
# ======================
def think_node(state: AgentState) -> AgentState:
    """思考节点：决定下一步行动"""
    current_step = state.get("step_count", 0) + 1
    print(f"\n{'=' * 40}")
    print(f"🤔 协调Agent: 思考下一步行动... (步骤 {current_step})")

    # 如果有任务结果，添加到消息中
    if state.get("last_agent_result"):
        result_msg = f"工具Agent返回结果: {state['last_agent_result'][:100]}..."
        state["messages"].append(SystemMessage(content=result_msg))
        print(f"📥 收到工具Agent结果: {state['last_agent_result'][:100]}...")

    # 调用模型获取响应
    start_time = time.time()
    response = model_with_tools.invoke(state["messages"])
    elapsed = time.time() - start_time

    print(f"🔄 模型响应时间: {elapsed:.2f}秒")
    if response.content:
        print(f"💬 AI回复: {response.content[:100]}...")

        # 检查是否有分析结论
        if "结论" in response.content or "分析" in response.content:
            state["analysis_conclusion"] = response.content
            print("💡 更新分析结论")

    # 提取工具调用
    tool_calls = []
    if hasattr(response, 'additional_kwargs') and "tool_calls" in response.additional_kwargs:
        tool_calls = response.additional_kwargs["tool_calls"]
        print(f"🛠️ 请求工具调用: {len(tool_calls)}个")
        for i, call in enumerate(tool_calls):
            print(f"  {i + 1}. {call['function']['name']}")

    # 确定下一个任务
    next_task = "think"  # 默认继续思考
    if tool_calls:
        # 取第一个工具调用作为当前任务
        tool_call = tool_calls[0]
        state["current_task"] = tool_call["function"]["name"]
        next_task = "invoke_agent"
        print(f"📡 分配任务: {state['current_task']} -> 工具Agent")
    elif "生成报告" in response.content or "generate_report" in response.content:
        state["current_task"] = "generate_report"
        next_task = "invoke_agent"
        print("📄 分配任务: 生成报告 -> 工具Agent")
    else:
        print("🏁 没有进一步任务，结束流程")
        next_task = "end"

    print(f"{'=' * 40}\n")

    return {
        "messages": [response],
        "analysis_conclusion": state.get("analysis_conclusion", ""),
        "step_count": current_step,
        "current_task": state.get("current_task", None),
        "last_agent_result": None  # 重置结果
    }


async def invoke_agent_node(state: AgentState) -> AgentState:
    """调用工具Agent节点"""
    task_name = state["current_task"]
    print(f"\n{'=' * 40}")
    print(f"📡 协调Agent: 调用 {task_name} 工具Agent...")

    # 获取工具Agent
    agent = TOOL_AGENTS.get(task_name)
    if not agent:
        error_msg = f"⚠️ 错误: 找不到工具Agent: {task_name}"
        print(error_msg)
        return {
            "messages": [ToolMessage(content=error_msg)],
            "last_agent_result": error_msg
        }

    # 准备参数
    params = {}
    last_message = state["messages"][-1]

    # 从AI消息中提取参数
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        for call in last_message.tool_calls:
            if call["name"] == task_name:
                try:
                    params = json.loads(call["args"])
                except:
                    params = {}

    # 处理时间参数 - 如果未提供则使用状态中的时间
    if task_name in ["get_monitoring_data", "get_change_list", "get_query_list"]:
        if "start_time" not in params or not params["start_time"]:
            params["start_time"] = state.get("start_time", "")
        if "end_time" not in params or not params["end_time"]:
            params["end_time"] = state.get("end_time", "")

    # 特殊处理报告生成
    if task_name == "generate_report":
        # 组合所有收集的数据作为报告内容
        report_content = "\n\n".join([
            "## 监控数据\n" + state["report_data"].get("monitoring", "无数据"),
            "## 变更清单\n" + state["report_data"].get("changes", "无数据"),
            "## 慢查询\n" + state["report_data"].get("queries", "无数据"),
            "## RGA分析\n" + state["report_data"].get("rga", "无数据"),
            "## 分析结论\n" + state.get("analysis_conclusion", "无分析结果")
        ])
        params["report_content"] = report_content

    print(f"📤 发送参数: {params}")

    # 运行工具Agent
    start_time = time.time()
    result = await agent.run(params)
    elapsed = time.time() - start_time

    print(f"🔄 工具Agent执行时间: {elapsed:.2f}秒")
    print(f"📥 收到结果: {result[:100]}...")

    # 保存结果到报告数据
    if task_name != "generate_report":
        state["report_data"][task_name] = result
    else:
        state["report_data"]["report"] = result

    print(f"{'=' * 40}\n")

    return {
        "last_agent_result": result,
        "report_data": state["report_data"]
    }


def should_continue(state: AgentState) -> str:
    """决策函数：判断是否继续循环"""
    current_step = state.get("step_count", 0)

    # 如果步数超过限制，强制结束
    if current_step > 15:
        print("⚠️ 决策: 超过最大步数限制(15)，强制结束")
        return "end"

    # 检查是否有任务在执行
    if state.get("current_task"):
        return "invoke_agent"

    # 检查是否声明任务完成
    last_message = state["messages"][-1] if state["messages"] else None
    if last_message and isinstance(last_message, AIMessage) and last_message.content:
        if "完成" in last_message.content or "结束" in last_message.content or "分析完毕" in last_message.content:
            print("✅ 决策: 检测到任务完成声明")
            return "end"

    # 默认返回思考节点
    return "think"


# ======================
# 7. 构建协调Agent工作流
# ======================
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("think", think_node)
workflow.add_node("invoke_agent", invoke_agent_node)

# 设置入口点
workflow.set_entry_point("think")

# 添加条件边
workflow.add_conditional_edges(
    "think",
    should_continue,
    {
        "invoke_agent": "invoke_agent",
        "think": "think",
        "end": END
    }
)

# 添加普通边
workflow.add_edge("invoke_agent", "think")

# 编译图
coordinator = workflow.compile()


# ======================
# 8. 运行分析的实用函数
# ======================
async def run_analysis(start_time: str, end_time: str) -> str:
    """运行监控突刺分析并返回报告路径"""
    # 初始化状态
    state = {
        "messages": [
            SystemMessage(content="你是一个专业的监控分析协调员，负责将任务分配给专业工具Agent并整合结果。"),
            HumanMessage(content=f"分析从 {start_time} 到 {end_time} 的监控数据，识别是否有突刺现象，并生成详细报告。")
        ],
        "start_time": start_time,
        "end_time": end_time,
        "report_data": {},
        "analysis_conclusion": "",
        "step_count": 0,
        "current_task": None,
        "last_agent_result": None
    }

    print(f"🔍 开始分析 {start_time} 到 {end_time} 的监控数据...")
    print(f"初始消息: {state['messages'][-1].content[:60]}...")

    # 运行协调Agent
    final_state = None
    step = 1
    async for output in coordinator.astream(state):
        for key, new_state in output.items():
            final_state = new_state
            print(f"\n🔄 步骤 {step} 完成 - 状态更新 (总步数: {final_state.get('step_count', 0)})")
            step += 1

            # 检查是否超过最大步数
            if final_state.get("step_count", 0) > 15:
                print("⚠️ 警告: 超过最大步数限制，强制终止")
                break

    if not final_state:
        print("❌ 错误: 未生成最终状态")
        return "报告生成失败"

    # 提取报告路径
    report_path = final_state["report_data"].get("report", "")
    if "报告已生成: " in report_path:
        report_path = report_path.split("报告已生成: ")[1]

    return report_path


# ======================
# 9. 主程序
# ======================
async def main():
    # 设置分析时间范围
    start_time = "2025-06-30 12:00"
    end_time = "2025-06-30 13:00"

    # 运行分析
    report_path = await run_analysis(start_time, end_time)

    # 处理结果
    if report_path and os.path.exists(report_path):
        print(f"\n✅ 分析完成！报告已生成: {report_path}")
        print("\n📄 报告内容预览:")
        with open(report_path, 'r', encoding='utf-8') as f:
            print(f.read()[:500] + "...")
    else:
        print("\n❌ 报告生成失败")
        print(f"报告路径: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())