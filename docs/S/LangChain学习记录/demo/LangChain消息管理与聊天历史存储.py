from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnablePassthrough
from docs.S.LangChain学习记录.demo.getchat import get_chat
from langchain_core.runnables import ConfigurableFieldSpec

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You're an assistant who's good at {ability}."
#         ),
#         MessagesPlaceholder(variable_name="history"),
#         ("human", "{input}")
#     ]
# )

model = get_chat("gpt-4o")

#runnable = prompt | model
#store = {}

# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]
#
# with_message_history = RunnableWithMessageHistory(
#     runnable,
#     get_session_history,
#     input_messages_key="input",
#     history_messages_key="history",
# )
#
# response = with_message_history.invoke(
#     {"ability": "math", "input": "欧式距离是什么意思？"},
#     config={"configurable": {"session_id": "abc123"}}
# )
#
# print(response)
#
# response = with_message_history.invoke(
#     {"ability": "math", "input": "我刚刚问了什么"},
#     config={"configurable": {"session_id": "abc123"}}
# )
#
# print(response)
#
# response = with_message_history.invoke(
#     {"ability": "math", "input": "我刚刚问了什么"},
#     config={"configurable": {"session_id": "abc124"}}
# )
#
# print(response)

# 配置唯一键

# def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
#     if (user_id, conversation_id)not in store:
#         store[(user_id, conversation_id)] = ChatMessageHistory()
#     return store[(user_id, conversation_id)]
#
# with_message_history = RunnableWithMessageHistory(
#     runnable,
#     get_session_history,
#     input_messages_key="input",
#     history_messages_key="history",
#     history_factory_config=[
#         ConfigurableFieldSpec(
#             id="user_id",
#             annotation=str,
#             name="User ID",
#             description="用户唯一标识",
#             default="",
#             is_shared=True
#         ),
#         ConfigurableFieldSpec(
#             id="conversation_id",
#             annotation=str,
#             name="Conversation ID",
#             description="对话唯一标识",
#             default="",
#             is_shared=True
#         )
#     ]
# )
#
# response = with_message_history.invoke(
# {"ability": "math", "input": "欧式距离是什么意思？"},
#     config={"configurable": {"user_id": "abc123", "conversation_id": "abc123"}}
# )
#
# print(response)
#
# response = with_message_history.invoke(
# {"ability": "math", "input": "我刚刚问了什么？"},
#     config={"configurable": {"user_id": "abc123", "conversation_id": "abc124"}}
# )
#
# print(response)
#
# def get_messages_history(session_id: str) -> BaseChatMessageHistory:
#     return RedisChatMessageHistory(session_id, url="")
#
# with_message_history = RunnableWithMessageHistory(
#     runnable,
#     get_messages_history,
#     input_messages_key="input",
#     history_messages_key="history",
# )
#
# response = with_message_history.invoke(
#     {"ability": "math", "input": "我刚刚问了什么？"},
#     config={"configurable": {"session_id": "abc124"}}
# )
#
# print(response)

# 修改聊天消息

temp_chat_history = ChatMessageHistory()
temp_chat_history.add_user_message("我叫zs，你好")
temp_chat_history.add_ai_message("你好")
temp_chat_history.add_user_message("我今天头很疼")
temp_chat_history.add_ai_message("你今天身体怎么样")
temp_chat_history.add_user_message("我下午在上班")
temp_chat_history.add_ai_message("你下午在干什么")
# print(temp_chat_history.messages)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个乐于助人的助手。尽力回答所有问题。提供的聊天历史包含你和用户聊的所有事实"
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]
)

chain = prompt | model

chat_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: temp_chat_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# response = chat_with_message_history.invoke(
#     {"input": "我今天身体怎么样？"},
#     config={"configurable": {"session_id": "unused"}}
# )
#
# print(response)

# 裁剪消息

# def trim_messages(chain_input):
#     stored_messages = temp_chat_history.messages
#     if len(stored_messages) <= 2:
#         return False
#     temp_chat_history.clear()
#     for message in stored_messages[2:]:
#         temp_chat_history.add_message(message)
#     return True
#
# chat_with_trimming = (
#     RunnablePassthrough.assign(messages_trimmed=trim_messages) | chat_with_message_history
# )
#
# response = chat_with_trimming.invoke(
#     {"input": "我下午在干什么? "},
#     config={"configurable": {"session_id": "unused"}}
# )
#
# print(response)
# print(temp_chat_history.messages)
#
# response = chat_with_trimming.invoke(
#     {"input": "我叫什么名字？"},
#     config={"configurable": {"session_id": "unused"}}
# )
#
# print(response)
#
# print(temp_chat_history.messages)

# 总结记忆

def summarize_messages(chain_input):
    stored_messages = temp_chat_history.messages
    if len(stored_messages) == 0:
        return False
    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            (
                "user",
                "将上述所有的聊天信息进行总结，包含多个具体细节。"
            )
        ]
    )
    summarization_chain = summarization_prompt | model
    summary_message = summarization_chain.invoke({"chat_history": stored_messages})
    temp_chat_history.clear()
    temp_chat_history.add_message(summary_message)
    return True

chain_with_summarization = (
    RunnablePassthrough.assign(messages_summarized=summarize_messages)  | chat_with_message_history
)

response = chain_with_summarization.invoke(
    {"input": "我下午在干什么？"},
    config={"configurable": {"session_id": "unused"}}
)

print(response)
print(temp_chat_history.messages)

response = chain_with_summarization.invoke(
    {"input": "我下午不想上班还能干什么？"},
    config={"configurable": {"session_id": "unused"}}
)

print(response)
print(temp_chat_history.messages)