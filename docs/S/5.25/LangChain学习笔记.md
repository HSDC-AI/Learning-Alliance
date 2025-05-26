# LangChain快速入门

## LangChain的定义

LangChain 是一个开源的开发框架,，皆在帮助开发者快速构建基友大模型(LLM)的应用程序，它通过模块化设计简化了与大模型交互的复杂性,支持灵活集成外部工具和数据源，使开发者能够高效实现复杂的AI应用逻辑。

![image-20250525182647438](/Users/xt03337/Documents/知识库/Learning-Alliance/docs/S/图片/image-20250525182647438.png)

LangChain框架由几个部分组成，包括：

- LangChain库：Python和JavaScript库。包括接口和集成多种组件的运行基础，以及现成的链和代理的实现。
- LangChain模版：LangChain官方提供一些AI任务模版。
- LangServe：基于FastApi可以将LangChain定义链，发布称为REST API。
- LangSmith：开发平台，是个云服务，支持LangChain Debug、任务监控。

LangChain库（Libraries）：

LangChain库本身由几个不同的包组成：

- Langchain-core：基础抽象的LangChain表达语言。
- langchain-community：第三方继承。
  - 合作伙伴包（例如langchain-openai，langchain-anthropic等）：一些集成已进一步拆分为仅依赖于langchain-core的轻量级包。
- langchain：构建应用程序认知架构的链、代理和检索策略。

LangChain任务处理流程

![image-20250525190108913](/Users/xt03337/Documents/知识库/Learning-Alliance/docs/S/图片/image-20250525190108913.png)

如上图，LangChain提供一套提示词模版管理工具，负责处理提示词，然后传递给大模型处理，最后处理大模型返回的结果。

LangChain对大模型的封装主要包括LLM和Chat Model两种类型：

- LLM-问答模型，模型接收一个文本输入，然后返回一个文本结果。
- Chat Model-对话模型，接收一组对话消息，然后返沪对话消息，类似聊天信息一样。

## 核心概念

1. LLMs

   LangChain封装的基础模型，模型接收一个文本输入，然后返回一个文本结果。

2. Chat Models（聊天模型）

   聊天类型，与LLMs不同，这些模型转为对话场景而设计，模型可以接收一组对话消息，然后染灰对话消息，类似聊天消息一样。

3. 消息（Message）

   指的是聊天模型的消息内容，消息类型包括HumanMessage、ALMessgae、SystemMessage、FunctionMessage和ToolMessage等多种类型的消息。

4. 提示（prompts）

   LangChain封装了一组专门用于提示词（prompts）管理的工具类，方便我们格式化提示词内容。

5. 输出解析器（Output Parers）

   如上图介绍，LangChain接收大模型返回的文本内容之后，可以使用专门的输出解析器对文本内容进行格式化，例如解析Json、python对象。

6. Retrievers

   为方便我们将私有数据导入到大模型，提高模型回答问题的质量，LangChain封装了检索框架，方便我们加载文档、切割、存储和检索文档数据。

7. 向量存储（Vector stores）

   为支持私有数据的语义相似搜索，langchain支持多种向量数据库。

8. Agents

   智能体，通常指以大模型为决策引擎，根据用户输入的任务，自动调用外部系统、硬件设备共同完成用户任务，是一种以大模型为核心的应用设计模式。

## 核心功能

（1）模块集成（Models）

- 作用：统一几口对接多种大模型（如OpenAI GPT、Anthropic、Hugging Face等），避免厂商锁定。
- 示例：通过ChatOpenAI或CharAnthropic类快速切换不同模型，实现对话、文本生成等任务。

（2）模块化组件（Components）

- 提示模块（Prompts）：标准化提示词管理，支持变量注入和动态生成（如Few-shot Learning）
- 文档加载器（Document Loaders）：支持PDF、网页、数据库等数据源的加载与预处理。
- 文档分割器（Text Splitters）：将长文本切分以适应模型输入限制。
- 向量存储（Vector Stores）：集成FAISS、Chroma等工具，实现文本向量化与相似性检索。

（3）链式调用（Chains）

- 作用：将多个步骤组合成可重复的流程，处理复杂任务。
- 典型链：RetrievalQA（检索+生成）、SequentialChain（顺序执行多个模型调用）。
- 场景：构建问答系统时，先检索知识库，在生成回答。

（4）记忆机制（Memory）

- 作用：维护对话历史或上下文状态，支持多轮交互。
- 实现方式：通过ConversationBufferMemory或ConversationSummaryMemory存储和管理历史信息。

（5）代理与工具（Agents & Tools）

- 代理（Agents）：让LLM动态选择调用工具，实现智能决策（如“使用搜索API查询天气，再用计算器转化单位”）。
- 工具（Tools）：预置搜索引擎、Python REPL、API调用等工具，支持自定义扩展。

（6）数据增强（RAG）

- 作用：将外部数据（如文档、数据库）与LLM结合提升生成内容的准确性和相关性。
- 流程：加载数据->向量化->检索相关片段->注入提示词->生成最终回答。

## 典型应用场景

- 智能问答系统：结合RAG处理领域知识库。
- 对话机器人：支持多轮会话、个性化记忆。
- 文档分析：自动总结长文本，提取关键信息。
- 自动化流程：通过代理调用工具执行代码、发送邮件等操作。
- 代码生成：根据需要描述生成并验证代码片段。

## 快速入门

### 安装LangChain

```python
pip install langchain
```

### 初始化模型

在使用langchain之前，需要导入LangChain X OpenAI集成包，并设置API密钥作为环境变量或直接传递给OpenAI LLM类。

首先，获取OpenAI的api密钥，可以通过创建账户并访问链接获取，然后将API密钥设置为环境变量：

```
export OPENAI_API_KEY = ""
from langchain_openai import ChatOpenAI
llm = ChatOpenAI()
```

### 输出转化

LLM的输出通常是一条消息，为了更方便处理结果，可以将消息转化为字符串。

```python
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()
```

### 相关代码

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo"
)

# 定义一个输出解析器
output_parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages(
    ("system", "你是一名数据库专家")
    ("user", "{input}")
)

chain = prompt | llm | output_parser

result = chain.invoke({"input": "帮我写一篇技术文档，100字左右"})

print(result)
```

# LangChain提示词工程应用实践

## Prompt templates（提示词模版）

语言模型以文本作为输入 - 这个文本通常被称为提示词（prompt）。在开发过程中，对于提示词通常不能直接硬编码，不利于提示词管理，而是通过提示词模版进行维护，类似开发过程中遇到的短信模版、邮件模版等等。

![image-20250525190108913](/Users/xt03337/Documents/知识库/Learning-Alliance/docs/S/图片/image-20250525190108913.png)

## 什么是提示词模版？

提示词模版本质上跟平时大家使用的邮件、短信模版某游什么区别，就是一个字符串模版，模版可以包含一组模版参数，通过模版参数可以替换模版对应的参数。

一个提示词模版可以包含以下内容：

- 发给大语言模型（LLM）的指令。
- 一组问答示例，以提醒AI以什么格式返回请求。
- 发给语言模型的问题。

## 创建一个提示词模版（prompt template）

可以使用PromptTemplate类创建简单的提示词。提示词模版可以内嵌任意数量的模版参数，然后通过参数值格式化模版内容。

```python
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "给我讲一个关于{content}的{adjective}笑话"
)
result = prompt_template.format(adjective="冷", content="狗")
print(result)
```

## 聊天消息提示词模版(chat prompt template)

聊天模型（Chat Model）以聊天消息列表作为输入，这个聊天消息列表的消息内容也可以通过提示词模版进行管理。这些聊天消息与原始字符串不同，因为每个消息都与“角色”相关联。

例如，在OpenAI的Chat Completion API中，OpenAi的聊天模型，给不同的聊天消息定义了三种角色类型分别是助手(assistant)、人类 (human)、系统 (system)角色：

- 助手(assistant)消息指的是当前消息是AI回答的内容。
- 人类 (human)消息指的是你发给AI的内容。
- 系统 (system)消息通常是用来给AI身份进行描述。

```python
from langchain_core.prompts import ChatPromptTemplate
from transformers.models.llama4.processing_llama4 import chat_template

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个人工智能助手，你的名字是{name}。"),
        ("human", "你好"),
        ("ai", "我很好，谢谢！"),
        ("human", "{user_input}"),
    ]
)

messages = chat_template.format_messages(name="Bob", user_input="你的名字叫什么?")
print(messages)
```

另一种消息格式例子： 

```python
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "你是一个乐于助人的助手，可以入色内容，使其看起来更简单易读。"
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}")
    ]
)

message = chat_template.format_messages(text="我最近为了学习头疼")
print(message)
```

通常我们不会直接使用format_messages函数格式化提示词模版内容，而是交给LangChain框架自动处理。

## MessagesPlaceholder

这个提示模版负责在特定位置添加消息列表，在上面ChatPromptTemplate中，我们看到了如何格式化两条消息，每条消息都是一个字符串。但是我们希望用户传入一个消息列表，我们将其插入到特定的位置，该怎么办？这就是使用MessagesPlaceholder的方式。

```python
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


prompt_template = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})
```

这将生成两条消息，第一条是系统消息，第二条是我们传入的HumanMessage。如果我们传入了5条消息，那么总共会生成6条消息(系统消息加上传入的5条消息)。这对于将一系列消息插入到特定位置非常有用。另一种实现相同效果的替代方式是，不直接使用MessagesPlaceholder类，而是：

```python
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assistant"),
    ("placeholder", "{msgs}")
])

prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})
```

## 提示词追加示例（Few-shot prompt templates）

提示词中包含交互样本的作用是为了帮助模型更好的理解用户的意图，从而更好的回答问题或执行任务。小样本提示模版是指使用一组少量的示例来指导模型处理新的输入。这些实例可以用来训练模型，以便模型可以更好的理解和回答类似的问题。

## 使用示例选择器

### 将示例提供给ExampleSelector

这里重用前一部分中的示例集和提示词模版。但是，不会将示例直接提供给提示词追加示例对象，把全部示例插入到提示词中，而是将它们提供给一个ExampleSelector对象，插入部分示例。

这里我们使用SemanticSimilarityExampleSelector类。该类根据与输入的相似性选择小样本示例。它使用嵌入模型计算输入和小样本示例之间的相关性，然后使用向量数据库执行相似搜索，获取跟输入相似的示例。

- 提示：这里涉及向量计算、向量数据库，在AI领域这两个主要用于数据相似度搜索。