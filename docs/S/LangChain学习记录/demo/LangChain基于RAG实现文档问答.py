import os
import tempfile
import streamlit as st
from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks.streamlit.streamlit_callback_handler import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import create_retriever_tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from streamlit import sidebar

def get_chat(model):
    return ChatOpenAI(
        temperature=0,
        model=model,
        base_url="http://10.255.4.108:8080/v1",
        api_key="sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452"
    )

def get_key(key):
    map = {
        "base_url": "http://10.255.4.108:8080/v1",
        "api_key": "sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452"
    }
    return map[key]

# 设置应用标题和布局
st.set_page_config(page_title="知识问答", layout="wide")
# 设置应用标题
st.title("知识问答")

# 文件上传
uploaded_files = st.sidebar.file_uploader(
    label="上传txt文件", type=["txt"], accept_multiple_files=True
)

if not uploaded_files:
    st.info("请先上传文档")
    st.stop()
else:
    # 检索器
    # @st.cache_resource(ttl="1h")
    def configure_retriever(upload_files):
        docs = []
        temp_dir = tempfile.TemporaryDirectory(dir="/Users/xt03337/Documents/xt/")
        for file in upload_files:
            temp_filepath = os.path.join(temp_dir.name, file.name)
            with open(temp_filepath, "wb") as f:
                f.write(file.getvalue())
            loader = TextLoader(temp_filepath, encoding="utf-8")
            docs.extend(loader.load())

        # 文档分割
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
        splits = text_splitter.split_documents(docs)

        # 文档向量化
        embeddings = OpenAIEmbeddings(
            base_url=get_key("base_url"),
            api_key=get_key("api_key"),
        )
        vectordb = Chroma.from_documents(splits, embeddings)
        retriever = vectordb.as_retriever()
        return retriever

    # 配置检索器
    retriever = configure_retriever(uploaded_files)

    # 如果session_state中没有消息记录/清理记录按钮初始化消息
    if "messages" not in st.session_state or sidebar.button("清空聊天记录"):
        st.session_state.messages = [{"role": "assistant", "content": "你好，我是知识问答助手"}]

    #加载聊天记录
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # 创建检索工具
    tool = create_retriever_tool(
        retriever,
        "文档检索",
        "用于检索用户提出的问题，并基于检索内容进行回复"
    )

    tools = [tool]

    # 历史聊天记录
    msgs = StreamlitChatMessageHistory()
    # 对话消息环缓存到内存
    memory = ConversationBufferMemory(
        chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
    )

    # 创建agent
    # 指令模版
    instructions = """您是一个设计用于查询文档来回答问题的代理。
    您可以使用文档检索工具，并基于检索内容来回答问题
    您可能不查询文档就知道答案，但是您仍然应该查询文档来获得答案。
    如果您从文档中找不到任何信息用于回答问题，则只需返回“抱歉，这个问题我还不知道。”作为答案。
    """

    # 提示模版
    base_prompt_template = """
    {instructions}
    
    TOOLS:
    ------
    
    You have access to the following tools:
    
    {tools}
    
    To use a tool, please use the following format:
    
    •```
    Thought: Do I need to use a tool? Yes
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    •```
    
    When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
    
    •```
    Thought: Do I need to use a tool? No
    Final Answer: [your response here]
    •```
    
    Begin!
    
    Previous conversation history:
    {chat_history}
    
    New input: {input}
    {agent_scratchpad}"""

    base_prompt = PromptTemplate.from_template(base_prompt_template)

    prompt = base_prompt.partial(instructions=instructions)

    llm = get_chat('gpt-4o')

    # 创建recat agent
    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=False, handle_parsing_errors="未检索到任何相似内容")

    # 创建聊天输入框
    user_query = st.chat_input(placeholder="来说出你的问题")

    if user_query:
        # 将消息添加到session_state
        st.session_state.messages.append({"role": "user", "content": user_query})
        # 显示用户消息
        st.chat_message("user").write(user_query)

        with st.chat_message("assistant"):
            # 创建会掉处理器
            st_cb = StreamlitCallbackHandler(st.container())
            # 将agent执行日志回掉显示在container
            config = {"callback": st_cb}
            # 执行agent获取相应
            response = agent_executor.invoke({"input": user_query}, config=config)
            # 添加相应消息到session_state
            st.session_state.messages.append({"role": "assistant", "content": response["output"]})
            # 显示相应
            st.write(response["output"])
