from langgraph.graph import END, StateGraph
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from typing import List, Dict, TypedDict, Annotated, Union, Optional
import operator
import json
import datetime
import os
import time
import uuid
import asyncio

from docs.S.LangChain学习记录.demo.getchat import get_chat


# ======================
# 1. 定义 Agent 基础类
# ======================
class BaseAgent:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """子类必须实现此方法来构建工作流"""
        raise NotImplementedError("Subclasses must implement this method")

    async def run(self, state: dict) -> dict:
        """运行Agent工作流"""
        return await self.workflow.ainvoke(state)


# ======================
# 2. 工具 Agent 实现
# ======================
class MonitoringDataAgent(BaseAgent):
    """从监控系统获取指定时间范围内的监控数据"""

    def __init__(self):
        super().__init__("监控数据获取", "从监控系统获取指定时间范围内的监控数据")

    @staticmethod
    def get_monitoring_data(start_time: str, end_time: str) -> str:
        """获取监控数据的具体实现"""
        return f"监控数据（{start_time} 至 {end_time}）:\n- CPU峰值80%\n- 内存使用率90%\n- 网络流量突增"

    def _build_workflow(self):
        # 定义状态
        class ToolAgentState(TypedDict):
            input_params: dict
            output_result: Optional[str]

        # 构建工作流
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
        print(f"🔧 {self.name}: 正在执行...")
        params = state["input_params"]
        result = self.get_monitoring_data(
            start_time=params.get("start_time", ""),
            end_time=params.get("end_time", "")
        )
        return {"output_result": result}

    def _return_result_node(self, state: dict) -> dict:
        """返回工具执行结果"""
        print(f"✅ {self.name}: 任务完成")
        return state


class ChangeListAgent(BaseAgent):
    """获取指定时间范围内的系统变更清单"""

    def __init__(self):
        super().__init__("变更清单获取", "获取指定时间范围内的系统变更清单")

    @staticmethod
    def get_change_list(start_time: str, end_time: str) -> str:
        """获取变更清单的具体实现"""
        return f"变更清单（{start_time} 至 {end_time}）:\n1. 数据库配置更新\n2. 应用版本v2.3部署\n3. 网络策略调整"

    def _build_workflow(self):
        # 定义状态
        class ToolAgentState(TypedDict):
            input_params: dict
            output_result: Optional[str]

        # 构建工作流
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
        print(f"🔧 {self.name}: 正在执行...")
        params = state["input_params"]
        result = self.get_change_list(
            start_time=params.get("start_time", ""),
            end_time=params.get("end_time", "")
        )
        return {"output_result": result}

    def _return_result_node(self, state: dict) -> dict:
        """返回工具执行结果"""
        print(f"✅ {self.name}: 任务完成")
        return state


class QueryListAgent(BaseAgent):
    """获取数据库慢查询列表"""

    def __init__(self):
        super().__init__("慢查询获取", "获取数据库慢查询列表")

    @staticmethod
    def get_query_list(start_time: str, end_time: str) -> str:
        """获取慢查询列表的具体实现"""
        return f"慢查询列表（{start_time} 至 {end_time}）:\n1. SELECT * FROM large_table (耗时12s)\n2. UPDATE user_stats (耗时8s)"

    def _build_workflow(self):
        # 定义状态
        class ToolAgentState(TypedDict):
            input_params: dict
            output_result: Optional[str]

        # 构建工作流
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
        print(f"🔧 {self.name}: 正在执行...")
        params = state["input_params"]
        result = self.get_query_list(
            start_time=params.get("start_time", ""),
            end_time=params.get("end_time", "")
        )
        return {"output_result": result}

    def _return_result_node(self, state: dict):
        """返回工具执行结果"""
        print(f"✅ {self.name}: 任务完成")
        return state


class RGASearchAgent(BaseAgent):
    """使用RGA搜索引擎检索相关信息"""

    def __init__(self):
        super().__init__("RGA搜索", "使用RGA搜索引擎检索相关信息")

    @staticmethod
    def rga_search(input_text: str) -> str:
        """RGA搜索的具体实现"""
        return f"RGA搜索结果:\n- 相关事件: 数据库维护窗口\n- 相关配置变更: 索引优化\n- 相关告警: 慢查询告警"

    def _build_workflow(self):
        # 定义状态
        class ToolAgentState(TypedDict):
            input_params: dict
            output_result: Optional[str]

        # 构建工作流
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
        print(f"🔧 {self.name}: 正在执行...")
        params = state["input_params"]
        result = self.rga_search(
            input_text=params.get("input_text", "")
        )
        return {"output_result": result}

    def _return_result_node(self, state: dict) -> dict:
        """返回工具执行结果"""
        print(f"✅ {self.name}: 任务完成")
        return state


class ReportAgent(BaseAgent):
    """生成分析报告文件"""

    def __init__(self):
        super().__init__("报告生成", "生成Markdown格式的报告文件")

    @staticmethod
    def generate_report(report_content: str) -> str:
        """生成报告的具体实现"""
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/monitoring_report_{timestamp}.md"
        content = f"# 监控突刺分析报告\n\n{report_content}"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"报告已生成: {filename}"

    def _build_workflow(self):
        # 定义状态
        class ToolAgentState(TypedDict):
            input_params: dict
            output_result: Optional[str]

        # 构建工作流
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
        print(f"🔧 {self.name}: 正在执行...")
        params = state["input_params"]
        result = self.generate_report(
            report_content=params.get("report_content", "")
        )
        return {"output_result": result}

    def _return_result_node(self, state: dict) -> dict:
        """返回工具执行结果"""
        print(f"✅ {self.name}: 任务完成")
        return state


# ======================
# 3. 定义状态结构
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
    collected_data: Dict[str, str]  # 收集所有工具返回的数据
    analysis_result: Optional[str]  # 最终分析结论
    current_step: int
    last_task: Optional[str]  # 最后执行的任务名称
    task_history: List[Dict]  # 任务执行历史
    is_completed: bool  # 任务是否完成
    pending_tool_calls: List[Dict]  # 待处理的工具调用


# ======================
# 4. 创建 Agent 实例
# ======================
monitoring_agent = MonitoringDataAgent()
change_agent = ChangeListAgent()
query_agent = QueryListAgent()
rga_agent = RGASearchAgent()
report_agent = ReportAgent()

# Agent 映射
AGENTS = {
    "get_monitoring_data": monitoring_agent,
    "get_change_list": change_agent,
    "get_query_list": query_agent,
    "rga_search": rga_agent,
    "generate_report": report_agent
}

# ======================
# 5. 协调 Agent
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
# 6. 协调 Agent 工作流节点
# ======================
async def task_planner(state: AgentState) -> AgentState:
    """任务规划节点：让大模型决定下一步行动"""
    print(f"\n{'=' * 40}")
    print(f"🧠 协调Agent: 规划下一步任务 (步骤 {state['current_step']})")

    # 准备上下文消息 - 只保留最近的完整交互轮次
    context_messages = state['messages'][-4:] if len(state['messages']) > 4 else state['messages']

    # 添加系统提示
    context_messages = [
                           SystemMessage(
                               content="你是一个专业的监控分析协调员，负责将任务分配给专业工具Agent并整合结果。每次只能调用一个工具。"),
                           SystemMessage(
                               content=f"当前任务: 分析从 {state['start_time']} 到 {state['end_time']} 的监控数据突刺"),
                           SystemMessage(content="可用工具列表:\n" + "\n".join(
                               [f"- {name}: {AGENTS[name].description}" for name in AGENTS]
                           )),
                           SystemMessage(content="已收集数据:\n" + (
                               "\n".join([f"- {k}: {v[:50]}..." for k, v in state['collected_data'].items()])
                               if state['collected_data'] else "无"
                           ))
                       ] + context_messages

    # 调用模型获取计划
    print("🔄 调用大模型进行任务规划...")
    response = model_with_tools.invoke(context_messages)

    # 提取工具调用
    tool_calls = []
    if hasattr(response, 'additional_kwargs') and "tool_calls" in response.additional_kwargs:
        tool_calls = response.additional_kwargs["tool_calls"]
        print(f"📋 模型规划任务: {len(tool_calls)}个")
        for i, call in enumerate(tool_calls):
            print(f"  {i + 1}. {call['function']['name']}")

    # 确定下一步任务
    next_task = None
    if tool_calls:
        # 只处理第一个工具调用
        tool_call = tool_calls[0]
        next_task = tool_call["function"]["name"]

        # 记录任务历史
        state["task_history"].append({
            "step": state["current_step"],
            "task": next_task,
            "params": tool_call["function"].get("arguments", {}),
            "tool_call_id": tool_call.get("id", f"call_{uuid.uuid4().hex[:30]}")  # 记录工具调用ID
        })

        # 存储其他待处理的工具调用
        pending_tool_calls = tool_calls[1:] if len(tool_calls) > 1 else []
        if pending_tool_calls:
            print(f"⚠️ 注意: 暂存 {len(pending_tool_calls)} 个待处理工具调用")

        print(f"📡 分配任务: {next_task} -> {AGENTS[next_task].name}")
    else:
        print("🏁 没有规划新任务，检查是否需要结束")
        pending_tool_calls = []

    print(f"{'=' * 40}\n")

    # 更新状态
    new_state = {
        "messages": [response],
        "last_task": next_task,
        "current_step": state["current_step"] + 1,
        "pending_tool_calls": pending_tool_calls
    }

    # 保留其他状态
    for key in ["start_time", "end_time", "collected_data", "analysis_result", "task_history", "is_completed"]:
        if key in state:
            new_state[key] = state[key]

    return new_state


async def task_executor(state: AgentState) -> AgentState:
    """任务执行节点：调用指定的Agent"""
    task_name = state["last_task"]
    if not task_name:
        print("⚠️ 无任务可执行")
        return state

    print(f"\n{'=' * 40}")
    print(f"⚙️ 协调Agent: 执行 {task_name} 任务")

    # 获取工具Agent
    agent = AGENTS.get(task_name)
    if not agent:
        error_msg = f"错误: 找不到工具Agent: {task_name}"
        print(error_msg)
        return {
            "messages": [AIMessage(content=error_msg)],
            "is_completed": True
        }

    # 准备参数 - 从任务历史中获取
    task_info = state["task_history"][-1]
    params = task_info["params"]

    # 如果是字符串形式的JSON，转换为字典
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except json.JSONDecodeError:
            params = {}

    # 特殊处理时间参数
    if task_name in ["get_monitoring_data", "get_change_list", "get_query_list"]:
        if "start_time" not in params:
            params["start_time"] = state["start_time"]
        if "end_time" not in params:
            params["end_time"] = state["end_time"]

    # 特殊处理报告生成
    if task_name == "generate_report":
        # 组合所有收集的数据作为报告内容
        # 确保所有部分都是字符串
        monitoring_data = state["collected_data"].get("get_monitoring_data", "无数据") or "无数据"
        change_list = state["collected_data"].get("get_change_list", "无数据") or "无数据"
        query_list = state["collected_data"].get("get_query_list", "无数据") or "无数据"
        rga_search = state["collected_data"].get("rga_search", "无数据") or "无数据"
        analysis_result = state.get("analysis_result", "无分析结果") or "无分析结果"

        report_content = "\n\n".join([
            f"## 监控数据\n{monitoring_data}",
            f"## 变更清单\n{change_list}",
            f"## 慢查询\n{query_list}",
            f"## RGA分析\n{rga_search}",
            f"## 分析结论\n{analysis_result}"
        ])
        params["report_content"] = report_content

    print(f"📤 执行参数: {params}")

    # 运行工具Agent
    print(f"🔄 调用 {task_name} Agent...")
    result = await agent.run({"input_params": params})
    agent_result = result.get("output_result", "无结果")

    # 保存结果
    updated_data = state["collected_data"].copy()
    if task_name != "generate_report":
        updated_data[task_name] = agent_result
        print(f"📥 收集数据: {agent_result[:100]}...")
    else:
        updated_data["report"] = agent_result
        print(f"📄 报告生成: {agent_result}")

    print(f"{'=' * 40}\n")

    # 创建工具响应消息 - 使用正确的tool_call_id
    tool_call_id = task_info.get("tool_call_id", f"call_{uuid.uuid4().hex[:30]}")
    tool_response = ToolMessage(
        content=agent_result[:2000],  # 限制内容长度
        name=task_name,
        tool_call_id=tool_call_id
    )

    # 更新状态
    new_state = {
        "collected_data": updated_data,
        "messages": [tool_response]
    }

    # 保留其他状态
    for key in ["start_time", "end_time", "analysis_result", "current_step", "last_task", "task_history",
                "is_completed", "pending_tool_calls"]:
        if key in state:
            new_state[key] = state[key]

    return new_state


def task_reviewer(state: AgentState) -> str:
    """任务评审节点：决定是否继续"""
    print(f"\n{'=' * 40}")
    print(f"🔍 协调Agent: 评审任务状态 (步骤 {state['current_step']})")

    # 检查是否有待处理的工具调用
    if state.get("pending_tool_calls") and len(state["pending_tool_calls"]) > 0:
        print(f"⚠️ 检测到 {len(state['pending_tool_calls'])} 个待处理工具调用")
        return "plan"  # 继续规划新任务

    # 检查是否生成报告
    if "report" in state["collected_data"]:
        print("✅ 检测到报告已生成")
        return "end"

    # 检查步数限制
    if state["current_step"] > 10:
        print("⚠️ 达到最大步数限制(10)")
        return "end"

    # 检查是否设置了完成标志
    if state.get("is_completed", False):
        print("✅ 检测到任务完成标志")
        return "end"

    # 检查模型是否表示任务完成
    last_message = state["messages"][-1] if state["messages"] else None
    if last_message and isinstance(last_message, AIMessage) and last_message.content:
        if "完成" in last_message.content or "结束" in last_message.content or "分析完毕" in last_message.content:
            print("✅ 模型指示任务完成")
            return "end"

    # 检查是否需要生成最终分析
    if state["current_step"] > 5 and not state.get("analysis_result"):
        print("📊 收集足够数据，准备生成分析结论")
        return "analyze"

    print("🔄 需要继续执行任务")
    print(f"{'=' * 40}\n")
    return "plan"


async def analysis_generator(state: AgentState) -> AgentState:
    """分析生成节点：创建最终分析结论"""
    print(f"\n{'=' * 40}")
    print(f"💡 协调Agent: 生成分析结论")

    # 准备分析提示
    collected_data_summary = "\n".join(
        [f"### {key}\n{value[:500]}{'...' if len(value) > 500 else ''}"
         for key, value in state["collected_data"].items()]
    )

    prompt = f"""
    基于以下数据，分析从 {state['start_time']} 到 {state['end_time']} 的监控突刺原因：

    {collected_data_summary}

    请给出专业的分析结论，包括：
    1. 可能的原因
    2. 责任方
    3. 改进建议
    """

    # 调用模型生成分析
    print("🔄 调用大模型生成分析结论...")
    response = model.invoke([
        SystemMessage(content="你是一个专业的监控数据分析师"),
        HumanMessage(content=prompt[:4000])  # 限制提示长度
    ])

    analysis = response.content
    print(f"📝 分析结论: {analysis[:200]}...")

    print(f"{'=' * 40}\n")

    # 更新状态
    new_state = {
        "analysis_result": analysis,
        "messages": [response]
    }

    # 保留其他状态
    for key in ["start_time", "end_time", "collected_data", "current_step", "last_task", "task_history", "is_completed",
                "pending_tool_calls"]:
        if key in state:
            new_state[key] = state[key]

    return new_state


# ======================
# 7. 构建优化的工作流
# ======================
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("plan", task_planner)  # 任务规划
workflow.add_node("execute", task_executor)  # 任务执行
workflow.add_node("review", lambda state: state)  # 评审节点（仅用于路由）
workflow.add_node("analyze", analysis_generator)  # 分析生成

# 设置入口点
workflow.set_entry_point("plan")

# 添加边
workflow.add_edge("plan", "execute")
workflow.add_edge("execute", "review")
workflow.add_edge("analyze", "plan")  # 生成分析后继续规划

# 添加条件边
workflow.add_conditional_edges(
    "review",
    task_reviewer,
    {
        "plan": "plan",  # 继续规划新任务
        "analyze": "analyze",  # 生成分析结论
        "end": END  # 结束流程
    }
)

# 编译图
coordinator = workflow.compile()


# ======================
# 8. 运行分析的实用函数
# ======================
async def run_analysis(start_time: str, end_time: str) -> str:
    """运行监控突刺分析并返回报告路径"""
    # 初始化状态
    state = AgentState(
        messages=[
            SystemMessage(
                content="你是一个专业的监控分析协调员，负责将任务分配给专业工具Agent并整合结果。每次只能调用一个工具。"),
            HumanMessage(content=f"分析从 {start_time} 到 {end_time} 的监控数据，识别突刺现象")
        ],
        start_time=start_time,
        end_time=end_time,
        collected_data={},
        analysis_result=None,
        current_step=1,
        last_task=None,
        task_history=[],
        is_completed=False,
        pending_tool_calls=[]
    )

    print(f"🔍 开始分析 {start_time} 到 {end_time} 的监控数据...")
    print(f"初始步骤: {state['current_step']}")

    # 运行协调Agent
    step_counter = 1
    async for output in coordinator.astream(state):
        for key, new_state in output.items():
            # 合并状态更新
            state.update(new_state)
            print(f"🔄 步骤 {step_counter} 完成 - 当前步骤 {state['current_step']}")
            step_counter += 1

            # 检查是否完成
            if state.get("is_completed", False):
                print("✅ 任务完成标志已设置")
                break

            # 检查是否超过最大步数
            if state["current_step"] > 10:
                print("⚠️ 达到最大步数限制(10)")
                break

    # 提取报告路径
    report_path = state["collected_data"].get("report", "")
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
    print("🚀 开始监控突刺分析流程")
    report_path = await run_analysis(start_time, end_time)

    # 处理结果
    if report_path and os.path.exists(report_path):
        print(f"\n✅ 分析完成！报告已生成: {report_path}")
        print("\n📄 报告内容预览:")
        with open(report_path, 'r', encoding='utf-8') as f:
            print(f.read()[:500] + "...")
    elif report_path:
        print(f"\n⚠️ 报告路径无效: {report_path}")
    else:
        print("\n❌ 报告生成失败")


if __name__ == "__main__":
    asyncio.run(main())