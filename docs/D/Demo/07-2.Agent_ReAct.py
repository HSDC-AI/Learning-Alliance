import os
from dotenv import load_dotenv 

load_dotenv()
minimax_api_key = os.getenv('MINIMAX_API_KEY')  
minimax_group_id = os.getenv('MINIMAX_GROUP_ID')  
minimax_base_url = os.getenv('MINIMAX_BASE_URL_V1') 

import calendar
from langchain.tools import Tool,tool
from datetime import date
from dateutil.parser import parse
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import BaseOutputParser
from langchain.schema import OutputParserException
# 自定义工具
@tool("weekday")
def weekday(date_str: str) -> str:
    """cover date to weekday name"""
    d=parse(date_str)
    return calendar.day_name[d.weekday()]


tools = [weekday]

print("\n ------------tools:------------")
print(tools)


class StopAtFinalAnswerParser(BaseOutputParser):
    def parse(self, text: str):
        # 如果输出中有 Final Answer，直接返回，不再继续
        if "Final Answer:" in text:
            print("\n ------------Final Answer find:------------")
            # 你可以自定义返回格式
            answer = text.split("Final Answer:")[-1].strip()
            return {"output": answer}
        # 否则抛出异常，让 agent 继续
        raise OutputParserException("No final answer found.")


prompt_template = """
你是一个智能AI助手，可以调用如下工具：

{tools}

请严格按照以下格式思考和作答：

Question: {input}
Thought: 你需要怎么做（简短说明）
Action: 要调用的工具名，必须是[{tool_names}]中的一个
Action Input: 工具的输入参数
Observation: 工具返回的结果
Thought: 我已经知道最终答案了
Final Answer: 问题的最终答案

不要输出多余内容，不要重复，不要解释，只输出上述格式内容。
Observation 后，只能输出一次 Thought: 我已经知道最终答案了 和 Final Answer:，然后立即结束，不要再输出任何内容。
After you output Final Answer, STOP. Do not output anything else. Do not repeat the process.

开始！

Question: {input}
{agent_scratchpad}
"""
prompt = PromptTemplate(
    input_variables=["input", "tools", "tool_names"],
    template=prompt_template,
)
print("\n ------------prompt:------------")
print(prompt.template)


llm = ChatOpenAI(
    model="MiniMax-Text-01",
    openai_api_key=minimax_api_key,
    openai_api_base=minimax_base_url
)

from langchain.agents import create_react_agent
agent = create_react_agent(
    llm,
    tools,
    prompt,
    
    
)

from langchain.agents import AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True,
    output_parser=StopAtFinalAnswerParser()
)
print("\n ------------agent_executor:------------")
# agent_executor.invoke({"input": "周杰伦的生日是哪天  是星期几？"})
for i in range(2):  # 最多循环5次
    result = agent_executor.invoke({"input": "周杰伦的生日是哪天  是星期几？"})
    if "Final Answer" in str(result):
        break







