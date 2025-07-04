import os
from dotenv import load_dotenv 

load_dotenv()
minimax_api_key = os.getenv('MINIMAX_API_KEY')  
minimax_group_id = os.getenv('MINIMAX_GROUP_ID')  
minimax_base_url = os.getenv('MINIMAX_BASE_URL_V1') 

LANGSMITH_API_KEY = os.getenv('LANGSMITH_API_KEY') 
LANGSMITH_ENDPOINT = os.getenv('LANGSMITH_ENDPOINT') 

os.environ['LANGSMITH_TRACING'] = "true"
os.environ['LANGSMITH_PROJECT'] = "test-001"




from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts.chat import HumanMessagePromptTemplate

llm = ChatOpenAI(
    model="MiniMax-Text-01",
    openai_api_key=minimax_api_key,
    openai_api_base=minimax_base_url
)

prompt_template = """
我的名字是{name}
请根据我的名字，帮我想一段有吸引力的自我介绍的句子
"""

prompt = ChatPromptTemplate.from_messages(
    [
        HumanMessagePromptTemplate.from_template(prompt_template)
    ]
)

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"name": "张三"})
print(result)




















