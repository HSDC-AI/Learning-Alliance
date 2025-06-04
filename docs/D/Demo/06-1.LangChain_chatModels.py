import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,   # openAI的 system
    HumanMessage,    # openAI的 user 
    AIMessage        # openAI的 assistant 
)

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
message = [
    SystemMessage(content="你是一个AI助手，擅长回答用户的问题。你的名字叫Dian。当被问到你的名字时，你必须回答'我叫Dian'。再加上你要说的话"),
    HumanMessage(content="你是谁？")
]


# response = llm.invoke(message)
# print("Raw response:", response)
# print('--------------------------------')
# print("Response content:", response.content)





print('-----------------模版 ChatModels---------------')
# 使用prompt模版
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个AI助手，擅长回答用户的问题。你的名字叫Dian。当被问到你的名字时，你必须回答'我叫Dian'。再加上你要说的话"),
        ("user", "{input}")
    ]
)
print('-----------------prompt---------------')
print(prompt)


 # 这里可以把 prompt和llm 通过 "|" 连接起来 这就是所谓的chain 链

chain = prompt | llm 
response = chain.invoke({"input": "你是谁？"})
print('-----------------模版 ChatModels 输出---------------')
print(response)
