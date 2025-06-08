from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from docs.S.LangChain学习记录.demo.getchat import get_chat

llm = get_chat("gpt-4o")

# 定义一个输出解析器
output_parser = StrOutputParser()

# 定义提示词
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个数据库专家"),
    ("user", "{input}")
])

# 构建链
chain = prompt | llm | output_parser

result = chain.invoke({"input": "帮我写一篇技术文档，100字左右"})

print(result)