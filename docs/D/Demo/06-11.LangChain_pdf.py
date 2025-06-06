# 导入必要的库
import os
import requests
from dotenv import load_dotenv
load_dotenv()  # 加载环境变量
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import MiniMaxEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

# 从环境变量中获取MiniMax API的配置信息
minimax_api_key = os.getenv('MINIMAX_API_KEY')
minimax_group_id = os.getenv('MINIMAX_GROUP_ID')
minimax_base_url = os.getenv('MINIMAX_BASE_URL_V1')


loader = PyPDFLoader(file_path="../Assets/单向散列函数是如何保证信息的完整性.pdf")

docs = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs_splitter = text_splitter.split_documents(docs)
print(len(docs_splitter))


embeddings = MiniMaxEmbeddings(
    minimax_api_key=minimax_api_key,
    minimax_group_id=minimax_group_id
)

vector_store = FAISS.from_documents(docs_splitter, embeddings)



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
retriever = vector_store.as_retriever()
retriever.search_kwargs = {'k': 3}

llm = ChatOpenAI(
    model="MiniMax-Text-01",
    openai_api_key=minimax_api_key,
    openai_api_base=minimax_base_url
)

document_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=prompt_doc
)

rag_chain = create_retrieval_chain(
    retriever=retriever,
    combine_docs_chain=document_chain
)

response = rag_chain.invoke({
    "input": "单向散列函数是如何保证信息的完整性？"
})

print(response['answer'])










# print(docs)

