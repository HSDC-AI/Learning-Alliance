import os
import requests
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

api_key = os.getenv('DEEPSEEK_API_KEY')
base_url = os.getenv('DEEPSEEK_BASE_URL')


# client = OpenAI(
#     api_key=api_key,
#     base_url=base_url
# )
# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "user", "content": "你是谁？"}
#     ]
# )
# print(response)

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    model="deepseek-reasoner", # deepseek-R1
    api_key=api_key,
    base_url=base_url
)
response = llm.invoke("你是谁？")
print(response)



# api_key = os.getenv('MINIMAX_API_KEY')
# group_id = os.getenv('MINIMAX_GROUP_ID')
# base_url = os.getenv('MINIMAX_BASE_URL')
# url = f"{base_url}/v1/text/chatcompletion_v2?GroupId={group_id}"

# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }
# data = {
#     "model": "MiniMax-Text-01", 
#     "messages": [
#         {"role": "system", "content": "你是一个AI接话小能手，你只需要将用户输入的句子补充完整。"},
#         {"role": "user", "content": "今天我"},
#     ],
#     "max_tokens": 20
# }
# response = requests.post(url, headers=headers, json=data)
# print(response.json()['choices'][0]['message']['content'])


# import os, openai
# import requests
# from dotenv import load_dotenv
# import json

# load_dotenv()

# api_key = os.getenv('MINIMAX_API_KEY')
# base_url = os.getenv('MINIMAX_BASE_URL_V1')

# client = OpenAI(
#     api_key=api_key,
#     base_url=base_url
# )
# response = client.chat.completions.create(
#     model="MiniMax-Text-01",
#     messages=[
#         {"role": "system", "content": "你是一个AI接话小能手，你只需要将用户输入的句子补充完整。"},
#         {"role": "user", "content": "今天我"},
#     ],
#     max_tokens=20
# )

# print(response)

