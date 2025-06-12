# 导入必要的库
import os  # 用于操作系统相关功能，这里主要用于获取环境变量
import requests  # 用于发送HTTP请求（本例未直接用到，但常用于数据抓取）
from dotenv import load_dotenv  # 用于加载.env文件中的环境变量

load_dotenv()  # 加载.env文件中的环境变量到系统环境中，便于后续通过os.getenv获取

# 联网搜索相关的LangChain工具
from langchain_community.tools.tavily_search import TavilySearchResults  # Tavily搜索API封装
from langchain_community.document_loaders import WebBaseLoader  # 用于加载网页内容
from langchain_text_splitters import RecursiveCharacterTextSplitter  # 用于将长文本分割成小块
from langchain_community.vectorstores import FAISS  # FAISS向量数据库，用于高效相似度检索
from langchain_community.embeddings import MiniMaxEmbeddings  # MiniMax嵌入模型，将文本转为向量
from langchain_core.prompts import ChatPromptTemplate  # 用于构建对话提示词模板
from langchain_openai import ChatOpenAI  # OpenAI兼容的LLM接口，这里用于MiniMax
from langchain.agents import AgentExecutor, initialize_agent, AgentType  # Agent相关工具

# ================== 环境变量配置 ==================
# 从环境变量中获取MiniMax API的配置信息，需提前在.env文件中配置
minimax_api_key = os.getenv('MINIMAX_API_KEY')  # MiniMax API密钥
minimax_group_id = os.getenv('MINIMAX_GROUP_ID')  # MiniMax分组ID
minimax_base_url = os.getenv('MINIMAX_BASE_URL_V1')  # MiniMax API基础URL

# ================== 联网搜索工具 ==================
# 初始化Tavily搜索工具，支持联网搜索
search = TavilySearchResults(
    tavily_api_key="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",  # Tavily测试API Key（仅测试用）
    max_results=2  # 最多返回2条搜索结果
)
# # 示例：调用搜索工具
# result = search.invoke("今天是几点？")
# print(result)

# ================== 网页加载与文本分割 ==================
# 加载指定网页内容，作为知识库的原始数据
loader = WebBaseLoader("https://www.thepaper.cn/newsdetail_forward_28688049")  # 指定要抓取的网页URL
docs = loader.load()  # 加载网页内容，返回文档对象列表

# 将长文档切分为更小的片段，便于后续向量化和检索
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 每个片段最大500字符
    chunk_overlap=50  # 相邻片段重叠50字符，保证上下文连续性
)

docs_splitter = text_splitter.split_documents(docs)  # 对文档进行切分，返回片段列表
print(len(docs_splitter))  # 打印切分后片段数量，便于调试

# ================== 向量化与向量数据库 ==================
# 初始化MiniMax嵌入模型，用于将文本转为向量表示
embeddings = MiniMaxEmbeddings(
    api_key=minimax_api_key,  # 使用环境变量中的API Key
    group_id=minimax_group_id,  # 使用环境变量中的Group ID
)
# 构建FAISS向量数据库，将所有片段转为向量并存储，便于后续相似度检索
vector_store = FAISS.from_documents(docs_splitter, embeddings)

# ================== 检索器与工具封装 ==================
# 用户输入的查询问题
input_text = "iphone16的价格"  # 这是用户要查询的问题

# 构建检索器，从向量数据库中检索相关片段
retruever = vector_store.as_retriever()  # 获取检索器对象
retruever.search_kwargs = {'k': 3}  # 每次检索返回3个最相关片段
# # 示例：检索相关内容
# result = retruever.invoke(input_text)
# print('\n-----------------retruever---------------')
# print(result)
# retruever.invoke("WWDC25什么时候开？")

# ================== LLM与自定义工具 ==================
# 初始化大语言模型（LLM），指定模型名称和API参数
llm = ChatOpenAI(
    model="MiniMax-Text-01",  # 使用MiniMax的文本模型
    openai_api_key=minimax_api_key,  # 兼容OpenAI接口，传入MiniMax的API Key
    openai_api_base=minimax_base_url  # 兼容OpenAI接口，传入MiniMax的API Base URL
)

from langchain.tools import Tool  # 导入Tool类，用于自定义工具
# 定义一个检索工具，专门用于查询iPhone16价格相关内容
triever_tool = Tool(
    name="iphone_price_search",  # 工具名称
    func=lambda q: "\n".join([doc.page_content for doc in retruever.get_relevant_documents(q)]),  # 工具功能：检索相关片段并拼接内容
    description="无论何时被问到iPhone16的价格，必须调用本工具，不能凭空作答。"  # 工具描述，Agent会根据描述决定何时调用
)

# 工具列表，包含联网搜索和自定义检索工具
tools = [search, triever_tool]

# ================== Prompt与Agent集成 ==================
# 构建对话提示词模板，约束Agent只能通过工具获取信息，不能凭空作答
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个只能通过工具获取信息的助手，不能凭空作答。"),  # 系统提示，约束Agent行为
    ("user", "{input}"),  # 用户输入
])
print('\n-----------------promot---------------')
print(prompt)  # 打印Prompt模板内容，便于调试

# 初始化Agent执行器，将工具、LLM、Agent类型等集成
agent_executor = initialize_agent(
    tools=tools,  # 可用工具列表
    llm=llm,  # 指定大语言模型
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Agent类型：零样本推理+工具描述
    verbose=True,  # 输出详细执行日志，便于调试
    handle_parsing_errors=True  # 自动处理解析错误，防止因格式问题中断
)

print('\n---------------result---------------')
# 调用Agent执行器，输入用户问题，返回最终结果和中间步骤
result = agent_executor.invoke(
    {"input": input_text},  # 用户输入
    return_intermediate_steps=True  # 返回中间推理步骤，便于分析
)
print(result)  # 打印最终结果和推理过程

# # 如需查看原始网页内容，可取消下行注释
# print(docs)

