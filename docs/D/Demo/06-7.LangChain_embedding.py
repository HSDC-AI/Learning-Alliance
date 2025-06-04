# 导入必要的库
import os
import requests
from dotenv import load_dotenv
from langchain_community.embeddings import MiniMaxEmbeddings
from langchain_openai import OpenAIEmbeddings
load_dotenv()  # 加载环境变量


# 从环境变量中获取MiniMax API的配置信息
minimax_api_key = os.getenv('MINIMAX_API_KEY')
minimax_group_id = os.getenv('MINIMAX_GROUP_ID')
text = "大模型是什么？"
embedding = MiniMaxEmbeddings(
    minimax_api_key=minimax_api_key,
    minimax_group_id=minimax_group_id
)
doc_result = embedding.embed_documents([text])
print(doc_result[0][:5])

query_result = embedding.embed_query(text)
print(query_result[:5])

