
# 导入必要的库
import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
load_dotenv()  # 加载环境变量


# 从环境变量中获取MiniMax API的配置信息
api_key = os.getenv('MINIMAX_API_KEY')
base_url = os.getenv('MINIMAX_BASE_URL_V1')

# 初始化ChatOpenAI模型，配置MiniMax API
llm = ChatOpenAI(
    model="MiniMax-Text-01",
    openai_api_key=api_key,
    openai_api_base=base_url,
) 

template = """你是一个专业的翻译专家。你的任务是：
1. 将用户提供的 {input_language} 文本翻译成 {output_language}
2. 保持原文的意思和语气
3. 只返回翻译结果，不要添加任何解释或额外内容

请将以下文本翻译成 {output_language}："""
human_message = "{text}"
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        ("human", human_message)
    ]
)

input = prompt.format_messages(
    input_language="中文",
    output_language="英文",
    text="我是谁？"
)
print(input)

result = llm.invoke(input)

print(result)
