from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    base_url="http://10.255.4.108:8080/v1",  # 根据你的实际API路径确认是否加 /v1
    api_key="sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452" # 即使是假的，也要传
)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(model, get_session_history)

config = {
    "configurable": {
        "session_id": "abc2"
    }
}

response = with_message_history.invoke(
    [HumanMessage(content="Hi my name is zs")],
    config=config
)

print(response.content)


response = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)

print(response.content)

config = {
    "configurable": {
        "session_id": "abc3"
    }
}

response = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)

print(response.content)

config = {
    "configurable": {
        "session_id": "abc2"
    }
}

response = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)

print(response.content)