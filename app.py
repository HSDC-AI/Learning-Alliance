import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes
from fastapi import FastAPI

# 加载环境变量
load_dotenv()

# 从环境变量中获取MiniMax API的配置信息
api_key = os.getenv('MINIMAX_API_KEY')
group_id = os.getenv('MINIMAX_GROUP_ID')
base_url = os.getenv('MINIMAX_BASE_URL')

# 创建 FastAPI 应用
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple LangChain API server"
)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的AI助手。"),
    ("user", "{input}")
])

# 初始化ChatOpenAI模型，配置MiniMax API
model = ChatOpenAI(
    model="MiniMax-Text-01",
    openai_api_key=api_key,
    openai_api_base=f"{base_url}/v1",
    default_headers={"GroupId": group_id}
)

# 创建链
chain = prompt | model

# 添加路由
add_routes(
    app,
    chain,
    path="/chat"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 