import base64
import httpx
from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser, XMLOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from docs.S.LangChain学习记录.demo.getchat import get_chat

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"

image_url2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Morning_in_China_Snow_Town.jpg/1280px-Morning_in_China_Snow_Town.jpg"

model = get_chat("gpt-4o")

# image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
#
# image_data2 = base64.b64encode(httpx.get(image_url2).content).decode("utf-8")

# message = HumanMessage(
#     content=[
#         {"type": "text", "text": "用中文描述这张图片"},
#         {
#             "type": "image_url",
#             "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
#         }
#     ]
# )

# response = model.invoke([message])
#
# print(response.content)

# message = HumanMessage(
#     content=[
#         {"type": "text", "text": "用中文描述这张图片"},
#         {
#             "type": "image_url",
#             "image_url": {"url": image_url},
#         }
#     ]
# )
#
# response = model.invoke([message])
#
# print(response.content)

# 传入多张图片

# message = HumanMessage(
#     content=[
#         {"type": "text", "text": "这两张图片是一样的吗"},
#         {
#             "type": "image_url",
#             "image_url": {"url": image_url},
#         },
#         {
#             "type": "image_url",
#             "image_url": {"url": image_url2},
#         }
#     ],
# )
#
# response = model.invoke([message])
#
# print(response.content)

# @tool
# def weather_tool(weather: Literal["晴朗的", "多云的", "多雨的", "下雪的"]) -> None:
#     """描述图片中的天气情况：晴朗、多云、多雨或下雪"""
#     pass
#
# model_with_tools = model.bind_tools([weather_tool])
#
# message = HumanMessage(
#     content=[
#         {"type": "text", "text": "用中文描述这两张图片的天气"},
#         {"type": "image_url", "image_url": {"url": image_url}},
#         {"type": "image_url", "image_url": {"url": image_url2}},
#     ]
# )
#
# response = model_with_tools.invoke([message])
#
# print(response.tool_calls)

# 自定义输出
#
# class Joke(BaseModel):
#     setup: str = Field(description="设置笑话问题")
#     punchile: str = Field(description="回答笑话问题")
#
# parser = JsonOutputParser(pydantic_object=Joke)
#
# prompt = PromptTemplate(
#     template="回答用户问题。\n{format_instructions}\{query}\n",
#     input_variables=["query"],
#     partial_variables={"format_instructions": parser.get_format_instructions()}
# )
#
# chain = prompt | model | parser
#
# response = chain.invoke({"query": "给我讲一个笑话"})
#
# print(response)

# 流式处理
#
# for s in chain.stream({"query": "给我讲一个笑话"}):
#     print(s)

# xml输出

parser = XMLOutputParser()
parser = XMLOutputParser(tags=["movies", "actor", "film", "name", "genre"])
prompt = PromptTemplate(
    template="回答用户问题\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = prompt | model

response = chain.invoke({"query": "生成周星驰的简化电影作品列表，按照最新的时间降序"})

xml_output = parser.parse(response.content)

print(xml_output)