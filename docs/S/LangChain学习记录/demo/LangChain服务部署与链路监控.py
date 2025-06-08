from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.globals import set_verbose, set_debug
from langchain_community.tools import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from docs.S.LangChain学习记录.demo.getchat import get_chat
# 打印调试日志
set_debug(True)
#不输出详细日志
set_verbose(False)

llm = get_chat("gpt-4o")
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