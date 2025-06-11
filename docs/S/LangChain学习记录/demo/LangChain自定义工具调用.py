import asyncio

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool, StructuredTool, ToolException
from pydantic import BaseModel, Field

# @tool
# def multiply(a: int, b: int) -> int:
#     """计算两个数的积."""
#     return a * b
#
# print(multiply.name)
# print(multiply.description)
# print(multiply.args)
#
# class CalculatorInput(BaseModel):
#     a: int = Field(description="第一个数字")
#     b: int = Field(description="第二个数字")
#
# @tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
# def multiply(a: int, b: int) -> int:
#     """计算两个数的积."""
#     return a * b
#
# print(multiply.name)
# print(multiply.description)
# print(multiply.args)
# print(multiply.return_direct)
#
# def multiply(a: int, b: int) -> int:
#     """计算两个数的积."""
#     return a * b
#
# async def amultiply(a: int, b: int) -> int:
#     """计算两个数的积."""
#     return a * b
#
# async def main():
#     calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)
#     print(calculator.invoke({"a": 2, "b": 2}))
#     print(await calculator.ainvoke({"a": 2, "b": 2}))
#
# asyncio.run(main())

# 自定义参数

# class CalculatorInput(BaseModel):
#     a: int = Field(description="第一个数字")
#     b: int = Field(description="第二个数字")
#
# def multiply(a: int, b: int) -> int:
#     """获得两个数的积"""
#     return a * b
#
# async def async_add(a: int, b: int) -> int:
#     """获得两个数的和"""
#     return a + b
#
# async def main():
#     calculator = StructuredTool.from_function(
#         func=multiply,
#         name="Calculator",
#         description="计算两个数的积",
#         args_schema=CalculatorInput,
#         return_direct=True,
#         coroutine=async_add
#     )
#     print(calculator.invoke({"a": 2, "b": 3}))
#     print(await calculator.ainvoke({"a": 2, "b": 3}))
#     print(calculator.name)
#     print(calculator.description)
#     print(calculator.args)
#
# asyncio.run(main())

#错误处理工具

# def get_weather(city: str) -> int:
#     """获取指定城市的天气"""
#     raise ToolException(f"告警：没有获取到名为{city}城市")
#
# get_weather_tool = StructuredTool.from_function(
#     func=get_weather,
#     handle_tool_error=True,
# )
#
# print(get_weather_tool.invoke({"city": "上海"}))

# def _handle_error(error: ToolException) -> str:
#     return f"工具调用失败 `{error.args[0]}`"
#
# get_weather_tool = StructuredTool.from_function(
#     func=get_weather,
#     handle_tool_error="没找到这个城市",
# )
#
# print(get_weather_tool.invoke({"city": "北京"}))

# 集成维基百科

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
# tool = WikipediaQueryRun(api_wrapper=api_wrapper)
# print(tool.invoke({"query": "韦东奕"}))
# print(tool.name)
# print(tool.description)
# print(tool.args)
# print(tool.return_direct)

# 自定义默认工具

class WikiInputs(BaseModel):
    """维基百科工具输入"""
    query: str = Field(
        description="至少输入三个字符，才可以进行查询"
    )

tool = WikipediaQueryRun(
    name="wiki-tool",
    description="查询维基百科",
    args_schema=WikiInputs,
    api_wrapper=api_wrapper,
    return_direct=True
)

print(tool.run("韦东奕"))

print(f"Name: {tool.name}")
print(f"Description: {tool.description}")
print(f"args schema: {tool.args}")
print(f"returns directly?: {tool.return_direct}")