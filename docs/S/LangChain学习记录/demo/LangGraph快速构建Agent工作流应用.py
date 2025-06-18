import asyncio
import operator
from langchain_community.tools import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import create_react_agent
from docs.S.LangChain学习记录.demo.getchat import get_key, get_chat
from typing import Annotated, List, Tuple, TypedDict, Union, Literal
from pydantic import BaseModel, Field

# LANGSMITH_API_KEY = get_chat('LANGSMITH_API_KEY')

# 工具
tools = [TavilySearchResults(tavily_api_key=get_key("tavily_api_key"))]

# 模型
llm = get_chat("gpt-4o")

# 创建 agent
agent_executor = create_react_agent(llm, tools)

# response = agent_executor.invoke(
#     {
#         "messages": [("user", "世界首富有多少钱")]
#     }
# )
#
# print(response)

# 定义类 用于存储输入、计划、过去的步骤和响应
class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str

# 定义plan模型
class Plan(BaseModel):
    """未来要执行的计划"""
    steps: List[str] = Field(
        description="需要执行的不同步骤，应该按顺序排序"
    )

# 创建计划生成模版
planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """对于给定的目标，提出一个简单的逐步计划。这个计划应该包含独立的任务，如果正确执行将得出正确的答案。不要添加任何多余的步骤。最后一步的结果应该是最终答案。确保每一步都有所有必要的信息 - 不要跳过步骤。""",
        ),
        ("placeholder", "{messages}"),
    ]
)

planner = planner_prompt | llm.with_structured_output(Plan)

# response = planner.invoke(
#     {
#         "messages": [
#             ("user", "马云的家乡是哪")
#         ]
#     }
# )
#
# print(response)

# 定义响应模型
class Response(BaseModel):
    """用户响应"""
    response: str

# 定义要执行的行为
class Act(BaseModel):
    """要执行的行为"""
    action: Union[Response, Plan] = Field(
        description="要执行的行为。如果要回应用户，使用Response。如果需要进一步使用工具获取答案，使用Plan。"
    )

# 创建一个重新计划的提示词模版
replanner_prompt = ChatPromptTemplate.from_template(
    """
    对于给定的目标，提出一个简单的逐步计划。这个计划应该包含独立的任务，如果正确执行将得出正确的答案。不要添加任何多余的步骤。最后一步的结果应该是最终答案。确保每一步都有所有必要的信息 - 不要跳过步骤。
    
    你的目标是：
    {input}
    
    你的原计划是：
    {plan}
    
    你目前已完成的步骤是：
    {past_steps}
    
    相应地更新你的计划。如果不需要更多步骤并且可以返回给用户，那么就这样回应。如果需要，填写计划。只添加仍然需要完成的步骤。不要返回已完成的步骤作为计划的一部分。
    """
)

# 使用指定提示词创建一个重新计划生成器
replanner = replanner_prompt | llm.with_structured_output(Act)

# 定义主函数
async def main():
    # 定义执行步骤函数
    async def execute_step(state: PlanExecute):
        plan = state["plan"]
        plan_str = "\n".join(f"P{i + 1}. {step}" for i, step in enumerate(plan))
        task = plan[0]
        task_formatted = f"""
        对于以下计划
        {plan_str}\n\n 你的任务是执行第{1}步，{task}.
        """
        agent_response = await agent_executor.ainvoke(
            {"messages": [("user", task_formatted)]}
        )
        return {
            "past_steps": state["past_steps"] + [(task, agent_response["messages"][-1].content)]
        }

    # 定义生成计划函数
    async def plan_step(state: PlanExecute):
        plan = await planner.ainvoke(
            {"messages": [("user", state["input"])]}
        )
        return {"plan": plan.steps}

    # 定义重新生成计划步骤
    async def replan_step(state: PlanExecute):
        output = await replanner.ainvoke(state)
        if isinstance(output.action, Response):
            return {"response": output.action.response}
        else:
            return {"plan": output.action.steps}

    # 定义判断函数
    def should_end(state: PlanExecute) -> Literal["agent", "__end__"]:
        if "response" in state and state["response"]:
            return "__end__"
        else:
            return "agent"

    # 创建一个状态图
    workflow = StateGraph(PlanExecute)

    # 添加计划节点
    workflow.add_node("planner", plan_step)

    # 添加一个步骤节点
    workflow.add_node("agent", execute_step)

    # 添加重新计划生成节点
    workflow.add_node("replan", replan_step)

    # 添加开始和计划节点的边
    workflow.add_edge(START, "planner")

    # 添加计划和agent的边
    workflow.add_edge("planner", "agent")

    # 添加agent和重新计划节点的边
    workflow.add_edge("agent", "replan")

    # 添加条件变
    workflow.add_conditional_edges(
        "replan",
        should_end
    )

    # 编译状态图，生成可运行对象
    app = workflow.compile()

    # 保存生成的图片
    graph_png = app.get_graph().draw_mermaid_png()
    with open("plan.png", "wb") as f:
        f.write(graph_png)

    # 设置递归限制
    config = {"recursion_limit": 50}

    # 定义输入
    inputs = {"input": "xtransfer的创始人的家乡是哪？用中文回复"}

    # 执行
    async for event in app.astream(inputs, config=config):
        for k, v in event.items():
            if k != "__end__":
                print(v)

asyncio.run(main())

