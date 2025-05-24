import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.getenv('MINIMAX_API_KEY')
group_id = os.getenv('MINIMAX_GROUP_ID')
base_url = os.getenv('MINIMAX_BASE_URL')
url = f"{base_url}/v1/text/chatcompletion_v2?GroupId={group_id}"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def sum_number(items):
    return sum(items)

data = {
    "model": "MiniMax-Text-01",
    "messages": [
        {"role": "system", "content": "你是一个AI接话小能手"},
        {"role": "user", "content": "我爸爸50岁 我25岁  我们的年龄相乘是多少岁"},
    ],
    "max_tokens": 256,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "sum_number",
                "description": "计算两个数的和",
                "parameters": {
                    "type": "object",
                    "parameters": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    }
                }
            }
        },
    ]
}

# 第一次请求，获取 function_call
response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result)

# 解析 function_call
choice = result['choices'][0]
finish_reason = choice['finish_reason']
message = choice['message']

tool_call = message['tool_calls'][0] if 'tool_calls' in message and message['tool_calls'] else None
function = tool_call["function"] if tool_call else None

if finish_reason == 'tool_calls' and function:
    function_call = function["name"]
    if function_call == "sum_number":
        arguments = json.loads(function["arguments"])
        function_result = sum_number(arguments["items"])
        tool_call_id = tool_call["id"]
        # 追加 assistant 的 tool_call 消息
        data["messages"].append(message)
        # 追加 tool 的返回
        data["messages"].append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": str(function_result)
        })
        # 再次请求，获得最终回复
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        print(result)
    else:
        print("没有 function_call，直接回复：", message.get('content', ''))
        exit()
else:
    print("没有 function_call，直接回复：", message.get('content', ''))

