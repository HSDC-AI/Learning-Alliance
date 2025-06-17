from langchain_openai import ChatOpenAI

def get_chat(model):
    return ChatOpenAI(
        temperature=0,
        model=model,
        base_url="http://10.255.4.108:8080/v1",
        api_key="sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452"
    )

def get_key(key):
    map = {
        "base_url": "http://10.255.4.108:8080/v1",
        "api_key": "sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452",
        "tavily_api_key": "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",
        "LANGSMITH_API_KEY": "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"
    }
    return map[key]