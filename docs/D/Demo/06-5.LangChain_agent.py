# 导入必要的库
import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()  # 加载环境变量

# 从环境变量中获取MiniMax API的配置信息
api_key = os.getenv('MINIMAX_API_KEY')
group_id = os.getenv('MINIMAX_GROUP_ID')
base_url = os.getenv('MINIMAX_BASE_URL')

# 初始化ChatOpenAI模型，配置MiniMax API
llm = ChatOpenAI(
    model="MiniMax-Text-01",
    openai_api_key=api_key,
    openai_api_base=f"{base_url}/v1",
    default_headers={"GroupId": group_id}
) 

# 导入网页加载器，用于从网页获取内容
from langchain_community.document_loaders import WebBaseLoader
from bs4 import SoupStrainer
# 配置网页加载器，指定要抓取的网页URL和HTML元素
loader = WebBaseLoader(
    web_paths=["https://www.gov.cn/xinwen/2020-06/01/content_5516649.htm"],  # 指定要抓取的网页URL
    bs_kwargs=dict(parse_only=SoupStrainer(id="UCAP-CONTENT"))  # 只获取指定ID的HTML元素内容
)

# 导入向量存储和文本分割器
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 加载文档
docs = loader.load()

# 配置文本分割器，将长文本分割成小块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    # 每个文本块的大小
    chunk_overlap=100   # 文本块之间的重叠部分
)

# 将文档分割成小块
documents = text_splitter.split_documents(docs)

print(len(documents))  # 打印分割后的文档块数量

# 导入MiniMax的嵌入模型
from langchain_community.embeddings import MiniMaxEmbeddings

# 初始化嵌入模型
embeddings = MiniMaxEmbeddings(
    minimax_api_key=api_key,
    minimax_group_id=group_id
)

# 使用FAISS创建向量存储
from langchain_community.vectorstores import FAISS
vector_store = FAISS.from_documents(documents, embeddings)

# 创建检索工具
from langchain.tools.retriever import create_retriever_tool
retriever = vector_store.as_retriever()

# 创建检索工具，用于搜索民法典相关信息
tool = create_retriever_tool(
    retriever,
    "CivilCodeRetriever",
    "搜索有关中华人民共和国和国民法典的信息。关于中华人民共和国和国民法典的任何问题，您必须使用此工具"
)

tools = [tool]  # 将工具添加到工具列表中

# 从LangChain Hub获取预构建的agent提示词模板
from langchain import hub
from langchain.agents import create_openai_functions_agent, AgentExecutor
# https://smith.langchain.com/hub/hwchase17/openai-functions-agent
prompt = hub.pull("hwchase17/openai-functions-agent")

# 创建智能体（agent）
agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# 创建智能体执行器
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 使用智能体回答问题
result = agent_executor.invoke({"input": "建设用地使用权是什么"})
print(result)  # 打印回答结果