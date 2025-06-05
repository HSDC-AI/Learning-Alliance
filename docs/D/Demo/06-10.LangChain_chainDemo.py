# 导入必要的库
import os
import requests
from dotenv import load_dotenv
load_dotenv()  # 加载环境变量
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_experimental.utilities import PythonREPL
from langchain_core.output_parsers import StrOutputParser



# 从环境变量中获取MiniMax API的配置信息
minimax_api_key = os.getenv('MINIMAX_API_KEY')
minimax_base_url = os.getenv('MINIMAX_BASE_URL_V1')

llm = ChatOpenAI(
    model="MiniMax-Text-01",
    openai_api_key=minimax_api_key,
    openai_api_base=minimax_base_url,
    temperature=0
)

template = """
Write some python code to solve the problem:
Return only python code in Markdown format, e.g:
```python
....
```
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        ("user", "{input}")
    ]
)

def _sanitize_output(text: str):
    _, after = text.split("```python")
    return after.split("```")[0]


# chain = prompt | llm | StrOutputParser()
chain = prompt | llm | StrOutputParser() | _sanitize_output | PythonREPL().run
result = chain.invoke({"input": "whats 2 plus 2"})
print(result)












