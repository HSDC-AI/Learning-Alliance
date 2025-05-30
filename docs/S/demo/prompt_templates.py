from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from docs.S.demo.get_message_history import with_message_history

model = ChatOpenAI(
    base_url="http://10.255.4.108:8080/v1",  # 根据你的实际API路径确认是否加 /v1
    api_key="sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452" # 即使是假的，也要传
)
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model

response = chain.invoke(
    {
        "messages": [
            HumanMessage(content="hi! I'm bob")
        ]
    }
)

with_message_history = RunnableWithMessageHistory(chain, get_session_history)

config = {
    "configurable": {
        "session_id": "abc123"
    }
}

response = with_message_history.invoke(
    [HumanMessage(content="hi! I'm zs")],
    config=config,
)
print(response.content)