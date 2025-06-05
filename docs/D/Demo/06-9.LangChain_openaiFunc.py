# 导入必要的库
import os
import requests
from dotenv import load_dotenv
load_dotenv()  # 加载环境变量
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.utils.function_calling import convert_to_openai_function
from pydantic import BaseModel, Field
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser



# 从环境变量中获取MiniMax API的配置信息
minimax_api_key = os.getenv('MINIMAX_API_KEY')
minimax_base_url = os.getenv('MINIMAX_BASE_URL_V1')

class Joke(BaseModel):
    problem: str = Field(description="设置笑话的问题")
    answer: str = Field(description="笑话的答案")

openai_function = convert_to_openai_function(Joke)
print("\nopenai_function:")
print(openai_function)
llm = ChatOpenAI(
    model="MiniMax-Text-01",
    openai_api_key=minimax_api_key,
    openai_api_base=minimax_base_url,
    temperature=0
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个乐于助人的助手"),
        ("user", "{input}")
    ]
)

parser = JsonOutputFunctionsParser()

chain = prompt | llm.bind(functions=[openai_function]) | parser

result = chain.invoke({"input": "给我讲一个笑话"})

print(result)







