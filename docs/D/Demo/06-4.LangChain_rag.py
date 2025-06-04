import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()

api_key = os.getenv('MINIMAX_API_KEY')
group_id = os.getenv('MINIMAX_GROUP_ID')
base_url = os.getenv('MINIMAX_BASE_URL')

llm = ChatOpenAI(
    model="MiniMax-Text-01",
    openai_api_key=api_key,
    openai_api_base=f"{base_url}/v1",
    default_headers={"GroupId": group_id}
) 

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


print('-----------------RAG开始---------------')
# 导入文档处理链和提示模板
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 创建提示模板，定义如何将检索到的文档和问题组合
prompt_doc = ChatPromptTemplate.from_messages([
   """
仅根据提供的上下文回答一下问题：
<context>
{context}
</context>
问题：{input}
   """
]
)

# 创建文档处理链，用于将检索到的文档和问题组合起来
document_chain = create_stuff_documents_chain(
    llm=llm,          # 使用之前配置的LLM模型
    prompt=prompt_doc, # 使用上面定义的提示模板
)

# 导入检索链
from langchain.chains import create_retrieval_chain

# 将向量存储转换为检索器
retruever = vector_store.as_retriever()
# 设置检索参数，每次检索最相关的3个文档
retruever.search_kwargs = {'k': 3}

input_query = "不动产登记，由不动产所在地的登记机构办理, 是那条条款"
test_docs = retruever.get_relevant_documents(input_query)
for i, doc in enumerate(test_docs):
    print(f"\n文档 {i+1}:")
    print(doc.page_content[:200])
# 输出查询到的文献更信息

# 创建RAG链，将检索器和文档处理链组合起来
rag_chain = create_retrieval_chain(
    retriever=retruever,           # 检索器，用于从向量存储中检索相关文档
    combine_docs_chain=document_chain  # 文档处理链，用于处理检索到的文档
)

# 使用RAG链回答问题
response = rag_chain.invoke({
    # "input": "建设用地使用权是什么？"  # 示例问题1
    # "input": "第二百零七条"           # 示例问题2
    # "input": "什么叫不动产？"         # 示例问题3
    "input": input_query  # 当前问题
})
# print(response) 
print("回答的内容：",response['answer']) 





