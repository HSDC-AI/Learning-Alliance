from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.globals import set_verbose, set_debug
from langchain_community.tools import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import openai
openai.api_key = "sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452"
openai.base_url = "http://10.255.4.108:8080/v1"
# 打印调试日志
set_debug(True)
#不输出详细日志
set_verbose(False)
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o",
    base_url="http://10.255.4.108:8080/v1",  # 根据你的实际API路径确认是否加 /v1
    api_key="sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452"  # 即使是假的，也要传
)
tools = [TavilySearchResults(tavily_api_key="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", max_results=1)]
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一位得力的助手。",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
# 构建工具代理
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
response = agent_executor.invoke(
    {
        "input": "谁执导了2023年的电影《奥本海默》，他多少岁了？"
    }
)
print(response)