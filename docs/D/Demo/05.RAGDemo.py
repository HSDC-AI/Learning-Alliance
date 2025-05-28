import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('MINIMAX_API_KEY')
group_id = os.getenv('MINIMAX_GROUP_ID')
base_url = os.getenv('MINIMAX_BASE_URL')

url = f"{base_url}/v1/embeddings?GroupId={group_id}"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_embedding(texts, model="embedding-embedding-001"):
    data = {
        "model": model,
        "type": "query",
        "texts": texts
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    print(result)  # 打印原始返回，便于调试
    return [item["embedding"] for item in result.get("data", [])]

text_query = ["大模型", "AI"]
res = get_embedding(text_query)
# print(res)


