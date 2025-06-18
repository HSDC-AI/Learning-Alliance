
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(
#             model="claude-3-5-sonnet-20241022",
#             openai_api_key=os.getenv("OPENAI_API_KEY"),
#             base_url="https://globalai.vip/v1"
#         )

# llm.invoke("你好")

import http.client
import json

# conn = http.client.HTTPSConnection("globalai.vip")
# payload = json.dumps({
#    "model": "claude-3-7-sonnet-20250219",
#    "messages": [
#       {
#          "role": "system",
#          "content": "You are a helpful assistant."
#       },
#       {
#          "role": "user",
#          "content": "你是谁!"
#       }
#    ]
# })
# headers = {
#    'Accept': 'application/json',
#    'Authorization': os.getenv("ANTHROPIC_API_KEY"),
#    'Content-Type': 'application/json',
#    'Host': 'globalai.vip',
#    'Connection': 'keep-alive'
# }
# conn.request("POST", "/v1/chat/completions", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))

llm = ChatOpenAI(
            model="claude-3-7-sonnet-20250219",
            openai_api_key=os.getenv("ANTHROPIC_API_KEY"),  # 这里用你的 Anthropic Key
            base_url="https://globalai.vip/v1"
        )
response = llm.invoke("你是谁!")
print(response)