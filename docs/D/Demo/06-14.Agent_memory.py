import os
from dotenv import load_dotenv 

load_dotenv()
minimax_api_key = os.getenv('MINIMAX_API_KEY')  
minimax_group_id = os.getenv('MINIMAX_GROUP_ID')  
minimax_base_url = os.getenv('MINIMAX_BASE_URL_V1') 

from langchain_openai import ChatOpenAI
from langchain.chains.conversation.base import ConversationChain


llm = ChatOpenAI(
    model="MiniMax-Text-01",
    openai_api_key=minimax_api_key,
    openai_api_base=minimax_base_url
)

conv_chain = ConversationChain(llm=llm)
print(conv_chain.prompt.template)




print("\n---------------conversationBufferMemory-----------------")

from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)
memory.chat_memory.add_user_message("你是谁")
memory.chat_memory.add_ai_message("你好，我是langchain")
memory.chat_memory.add_user_message("很好，以后我问你你就这么回答")
memory.chat_memory.add_ai_message("好的我记住了，以后你问我是谁，我就回答：我是langchain")

conversation = ConversationChain(llm=llm, memory=memory)

print(conversation.prompt)
result = conversation.invoke({"input": "你是谁？"})
print("\n---------------result-----------------")
print(result)


print("\n---------------LLMChain-----------------")

from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
template = """
你可以与人类对话。
当前对话:{chat_history}
人类的问题：{question}
回复：
"""
prompt = PromptTemplate(
    input_variables=["chat_history", "question"], 
    template=template
    )
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
    )
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
    )

# res=chain.invoke({"question": "你是langchain"})
# print("\n---------------res-----------------")
# print(res["text"])

# res=chain.invoke({"question": "我的名字是Dian"})
# print("\n---------------res-----------------")
# print(res["text"])

# res=chain.invoke({"question": "我的名字是什么?"})
# print("\n---------------res-----------------")
# print(res["text"])


print("\n---------------向量存储库记忆-----------------")

import faiss
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import MiniMaxEmbeddings



# 初始化向量存储相关组件
embedding_siza = 1536 # embedding 向量的维度大小
index = faiss.IndexFlatL2(embedding_siza)  # 创建FAISS索引，使用欧氏距离（L2范数）来衡量向量间的相似度，支持高效的相似内容检索
# index = faiss.IndexFlatIP(embedding_siza)  # 创建基于内积的扁平向量索引    余弦相似度 计算向量相似度
embedding_fn = MiniMaxEmbeddings(
    minimax_api_key=minimax_api_key,
    minimax_group_id=minimax_group_id
).embed_query # 定义用于生成向量的embedding函数
# print("\n---------------向量的维度大小-----------------")
# print(len(embedding_fn))  # 输出应该是 1536  这里可以输出 向量维度的大小
vectorstore = FAISS(embedding_fn, index, InMemoryDocstore({}), {})  # 构建FAISS向量存储对象

# 获取向量检索器，用于后续的相似度检索
retriever = vectorstore.as_retriever()

# 初始化向量存储记忆对象
memory = VectorStoreRetrieverMemory(
    retriever=retriever
)

# 向记忆中保存多轮对话的上下文信息
memory.save_context({"Human": "我最喜欢的食物是披萨"}, {"AI": "很高兴知道"})
memory.save_context({"Human": "我最喜欢的水果是菠萝"}, {"AI": "好的，我知道了"})
memory.save_context({"Human": "我最喜欢的动物是猫咪"}, {"AI": "好的，我知道了"})

# 定义对话模板，history变量用于插入检索到的相关历史片段
_DEFAULT_TEMPLATE = """
以下是人类和人工智能之间的友好对话。人工智能很健谈，并从其上下文中提供了许多具体细节。如果人工智能不知道问题的答案，它就会如实说它不知道。
之前对话的相关片段: {history}
(如果不相关，则无需使用这些信息)
当前对话:
Human: {input}
AI:
"""
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=_DEFAULT_TEMPLATE
)

# 构建带有向量记忆的对话链
conversation_with_summary = ConversationChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

# 进行一次对话，模型会自动检索相关历史信息并生成回答
result = conversation_with_summary.predict(input="我最喜欢什么？")
print("\n---------------result-----------------")
print(result)






















