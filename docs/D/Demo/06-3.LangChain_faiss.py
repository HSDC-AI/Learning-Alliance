import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv('MINIMAX_API_KEY')
group_id = os.getenv('MINIMAX_GROUP_ID')
base_url = os.getenv('MINIMAX_BASE_URL')

print('-----------------向量存储Embedding---------------')
from langchain_community.document_loaders import WebBaseLoader
from bs4 import SoupStrainer
# 使用WebBaseLoader加载网页内容
loader = WebBaseLoader(
    web_paths=["https://www.gov.cn/xinwen/2020-06/01/content_5516649.htm"],  # 指定要抓取的网页URL
    bs_kwargs=dict(parse_only=SoupStrainer(id="UCAP-CONTENT"))  # 只获取指定ID的HTML元素内容
)

# 导入FAISS向量存储和文本分割器
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 加载文档
docs = loader.load()
print("原始文档内容预览:")
print(docs[0].page_content[:500])  # 打印更多内容来检查

# 调整文本分割器，使用更大的块大小
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    # 增加块大小
    chunk_overlap=100   # 增加重叠
)

# 将文档分割成小块
documents = text_splitter.split_documents(docs)
print("\n分割后的文档块数量:", len(documents))

# 导入MiniMax的嵌入模型
from langchain_community.embeddings import MiniMaxEmbeddings

# 初始化嵌入模型
embeddings = MiniMaxEmbeddings(
    minimax_api_key=api_key,
    minimax_group_id=group_id
)
# 使用FAISS创建向量存储
# 将文档转换为向量并存储，便于后续的相似度搜索
print('-----------------存储向量数据FAISS---------------')
vector_store = FAISS.from_documents(documents, embeddings)

