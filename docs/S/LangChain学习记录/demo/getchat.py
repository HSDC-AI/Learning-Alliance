from langchain_openai import ChatOpenAI

def get_chat(model):
    return ChatOpenAI(
        temperature=0,
        model=model,
        base_url="http://10.255.4.108:8080/v1",  # 根据你的实际API路径确认是否加 /v1
        api_key="sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452"  # 即使是假的，也要传
    )

def get_key(key):
    map = {
        "base_url": "http://10.255.4.108:8080/v1",
        "api_key": "sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452"
    }
    return map[key]