import asyncio

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy.util import await_only
from docs.S.LangChain学习记录.demo.getchat import get_chat

model = get_chat("gpt-4o")

chunks = []
# for chunk in model.stream("海是什么颜色"):
#     chunks.append(chunk)
#     print(chunk.content, end="|", flush=True)
#
# async def test():
#     async for chunk in model.astream("海是什么颜色"):
#         chunks.append(chunk)
#         print(chunk.content, end="|", flush=True)
#
# asyncio.run(test())

# prompt = ChatPromptTemplate.from_template("给我讲一个关于{topic}的笑话")
# parser = StrOutputParser()
# chain = prompt | model | parser
# async def main():
#     async for chunk in chain.astream({"topic": "计算机"}):
#         print(chunk, end="|", flush=True)
# asyncio.run(main())

# parser = StrOutputParser()
# chain = (
#     model | JsonOutputParser()
# )
# async def main():
#     async for text in chain.astream(
#         "以JSON 格式输出法国、西班牙和日本的国家及其人口列表。"
#         '使用一个带有“countries”外部键的字典，其中包含国家列表。'
#         "每个国家都应该有键`name`和`population`"
#     ):
#         print(text)
# asyncio.run(main())

events = []
async def main():
    async for event in model.astream_events("hello", version="v2"):
        events.append(event)
    print(events[-2:])
asyncio.run(main())