from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder

prompt_template = PromptTemplate.from_template(
    "给我讲一个关于{content}的{adjective}笑话"
)

result = prompt_template.format(adjective="完整", content="猫")

print(result)

# 创建聊天消息提示词模版

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个人工智能助手，你的名字是{name}"),
        ("human", "你好"),
        ("assistant", "我很好，谢谢！"),
        ("human", "{user_input}")
    ]
)

messages = chat_prompt.format_messages(name="zs", user_input="你的名字是什么")

print(messages)

# 另一种消息格式

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "你是一个乐于助人的助手，可以入色内容，使其看起来更简单易读。"
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}")
    ]
)

messages = chat_template.format_messages(text="我最近为了学习头疼")

print(messages)

# MessagesPlaceholder
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个人工智能助手"),
    MessagesPlaceholder("msgs"),
    ("placeholder", "{msgs}")
])

result = prompt_template.invoke({
    "msgs": [HumanMessage(content="你好！")]
})

print(result)