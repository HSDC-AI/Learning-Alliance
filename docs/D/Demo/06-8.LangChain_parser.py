# 导入必要的库
import os
import requests
from dotenv import load_dotenv
load_dotenv()  # 加载环境变量
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser



# 从环境变量中获取MiniMax API的配置信息
minimax_api_key = os.getenv('MINIMAX_API_KEY')
minimax_base_url = os.getenv('MINIMAX_BASE_URL_V1')

deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
deepseek_base_url = os.getenv('DEEPSEEK_BASE_URL')


def translate_text(text):
    # 创建一个新的翻译模板
    translate_template = "将以下文本翻译成中文：{text}"
    translate_prompt = PromptTemplate.from_template(translate_template)
    # 创建翻译链
    translate_chain = translate_prompt | llm | StrOutputParser()
    # 执行翻译
    translated_result = translate_chain.invoke({"text": text})
    return translated_result



# llm = ChatOpenAI(
#     model="deepseek-reasoner",
#     openai_api_key=deepseek_api_key,
#     openai_api_base=deepseek_base_url
# )
llm = ChatOpenAI(
    model="MiniMax-Text-01",
    openai_api_key=minimax_api_key,
    openai_api_base=minimax_base_url
)

print("---------------Json/Str解析器-----------------")
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "你是一个专业的翻译专家。你的任务是："),
#         ("human", "{text}")
#     ]
# )
# # output_parser = JsonOutputParser()
# output_parser = StrOutputParser()


# chain = prompt| llm | output_parser

# result = chain.invoke({"text": "你好。用json的形式回复我"})
# print(result)


print("---------------时间解析器-----------------")
# from langchain.output_parsers import DatetimeOutputParser

# datetime_parser = DatetimeOutputParser()

# template = "回答用户的问题：{question} {format_instructions}"
# prompt = PromptTemplate.from_template(
#     template,
#     partial_variables={"format_instructions": datetime_parser.get_format_instructions()}
# )
# print("\nprompt:")
# print(prompt)
# print("\ntranslate_text:")
# print(translate_text(prompt))
# print("format_instructions:")
# print(datetime_parser.get_format_instructions())

# chain = prompt | llm | datetime_parser

# result = chain.invoke({"question": "中国奥运会是什么时候？"})
# print(result)


print("---------------CSV解析器-----------------")

from langchain.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()

template = "生成5个列表{text} \n\n{format_instructions}"

prompt = PromptTemplate.from_template(
    template,
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

print("\nprompt:")
print(prompt)
print("\ntranslate_text:")
print(translate_text(prompt))

chain = prompt | llm | parser
result = chain.invoke({"text": "生成5个列表"})
print("\n结果:")
print(result)

    
    
    
    
    