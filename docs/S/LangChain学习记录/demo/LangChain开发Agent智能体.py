import os
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_tavily import TavilySearch
from langchain_community.vectorstores import FAISS
from langchain_core.tools import create_retriever_tool
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from docs.S.LangChain学习记录.demo.getchat import get_key, get_chat
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.agents import AgentAction

from docs.S.demo.get_message_history import response

os.environ["USER_AGENT"] = "MyLangChainBot/1.0 (+https://yourdomain.com)"
from langchain_community.document_loaders import WebBaseLoader

search = TavilySearch(tavily_api_key=get_key("tavily_api_key"), max_results=2)

# print(search.invoke("上海的天气怎么样"))

loader = WebBaseLoader("https://www.thepaper.cn/newsdetail_forward_28688049")

docs = loader.load()

documents = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=20
).split_documents(docs)

# 文本向量化
vector = FAISS.from_documents(documents, OpenAIEmbeddings(
        base_url=get_key("base_url"),
        api_key=get_key("api_key")
))

retriever = vector.as_retriever()
#
# print(retriever.invoke("iphone16的价格")[0])

# 定义网页搜索工具
retriever_tool = create_retriever_tool(
    retriever,
    "web_search",
    "搜索网页",
)

tools = [retriever_tool, search]
#
model = get_chat('gpt-4')
# #
# response = model.invoke([HumanMessage(content="你好")])
# print(response)
#
# model_with_tools = model.bind_tools(tools)
#
# response = model_with_tools.invoke([HumanMessage(content="你是谁")])
#
# print(response.content)
# print(response.tool_calls)
#
# response = model_with_tools.invoke([HumanMessage(content="上海的天气")])
#
# print(response)
# print(response.tool_calls)

# 调用agent
# 使用官方推荐的方式构建 Agent
prompt = hub.pull("hwchase17/openai-functions-agent")

agent = create_openai_functions_agent(model, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)

# print(agent_executor.invoke({"input": "上海天气"}))

# print(agent_executor.invoke({"input": "张爽这个人怎么样"}))

# 增加记忆

# response = agent_executor.invoke({"input": "我是张爽", "chat_history": []})
#
# print(response)

# response = agent_executor.invoke(
#     {
#         "chat_history": [
#             HumanMessage(content="我是张爽"),
#             AIMessage(content="你好，张爽！有什么我可以帮助你的吗？")
#         ],
#         "input": "我的名字是什么？"
#     }
#
# )
#
# print(response)

# 自动追踪消息记忆

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

response = agent_with_chat_history.invoke(
    {"input": "我的名字是张爽"},
    config={"configurable": {"session_id": "abcd123"}}
)

print(response)

response = agent_with_chat_history.invoke(
    {"input": "我的名字叫什么"},
    config={"configurable": {"session_id": "abcd123"}}
)

print(response)