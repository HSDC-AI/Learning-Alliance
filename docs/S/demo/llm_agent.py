from langchain_community.tools import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

memory = MemorySaver()
model = ChatOpenAI(
    base_url="http://10.255.4.108:8080/v1",  # 根据你的实际API路径确认是否加 /v1
    api_key="sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452" # 即使是假的，也要传
)
search = TavilySearchResults(
    tavily_api_key="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",
    max_results=2
)
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)
config = {
    "configurable": {
        "thread_id": "abc123"
    }
}

for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="你好！ 我叫张爽，我生活在上海")]},
        config=config,
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="上海的天气怎么样?")]},
        config=config,
):
    print(chunk)
    print("----")