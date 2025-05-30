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
import os
from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个人工智能助手，你的名字是{name}。"),
        ("human", "你好"),
        ("ai", "我很好，谢谢！"),
        ("human", "{user_input}"),
    ]
)

messages = chat_prompt.format_messages(name="Bob", user_input="你的名字叫什么?")
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

# LangChain工作流编排

## LCEL介绍

LCEL(LangChain Expression Language)是一个强大的工作流编排工具，可以从基本组件构建复杂任务链条（chain），并支持诸如流式处理、并行处理和日志记录等开箱即用的功能。

LCEL从第一天就被设计为支持将原型投入生产，无需更改代码，从最简单的“提示+LLM”链到最复杂的链（我们已经看到有人成功地在生产中运行了包含数百步的LCEL链）。以下是使用LCEL的几大亮点：

- 一流的流式支持：当使用LCEL构建链是，将获得可能的最佳时间到第一个标记（直到输出的第一块内容出现所经过的时间）。对于某些链，这意味着我们直接从LLM流式传输标记到流式输出解析器，将以与LLM提供程序输出原始标记的速率相同的速度获取解析的增量输出块。
- 异步支持：使用LCEL构建的任何链都可以使用同步API以及异步API进行调用。这使得可以在原型和生产中使用相同的代码，具有出色的性能，并且能够在同一服务器中处理许多并发请求。
- 优化的并行执行：每当LCEL链具有可以并行执行的步骤时，会自动执行，无论是在同步接口还是异步接口中，以获取可能的最小延迟。
- 重试和回退：为LCEL链的任何部分配置重试和回退。这使链在规模上更可靠的好办法。目前正在努力为重试/回退添加流式支持，这样就可以获得额外的可靠性而无需任何延迟成本。
- 访问中间结果：对于更复杂的链，访问中间步骤的结果通常非常有用，即使在生成最终输出之前。这可以用于让最终用户知道正在发生的事情，甚至只是用于调用链。可以流式传输中间结果，并且在每个LangServe服务器上都可以使用。
- 输入和输出模式：输入和输出模式为每个LCEL链提供了从链的结构推断出的Pydantic和JSONSchema模式。这可用于验证输入输出，并且是LangServe的一个组成部分。

## Ruable interface

为了尽可能简化创建自定义链的过程，实现了一个Runable的协议，许多LangChain的组件都实现了Runable协议，包括聊天模型、LLMs、输出解析器、检索器、提示模版等等。此外，还有一些有用的基本组件可用于处理可运行对象。这是一个标准接口，可以轻松定义自定义链，并以标准方式调用。标准接口包括：

- stream：返回响应的数据块。
- invoke：输入调用链(同步调用）。
- batch：输入列表调用链（批量调用）。

还有相应的异步方法，应该与asyncio一起使用await语法以实现并发：

- astream：异步返回响应的数据块。
- ainvoke：异步输入调用链。
- abatch：异步输入列表调用链。
- astream_log：异步返回中间步骤，以及最终响应。
- astream_events：beta流式传输链中发生的事件。

输入类型和输出类型因组件而异：

| 组件       | 输入类型                         | 输出类型     |
| ---------- | -------------------------------- | ------------ |
| 提示       | 字典                             | 提示值       |
| 聊天模型   | 单个字符串、聊天信息列表或提示值 | 聊天消息     |
| LLM        | 单个字符串、聊天信息列表或提示值 | 字符串       |
| 输出解析器 | LLM或聊天模型的输出              | 取决于解析器 |
| 检索器     | 单个字符串                       | 文档列表     |
| 工具       | 单个字符串活字典，取决于工具     | 取决于工具   |

所有可运行对象都公开输入和输出模式以检查输入和输出：

- input_schema:从可运行对象机构自动生成的输入Pydantic模型
- output_schema:从可运行对象机构自动生成的输出Pydantic模型

流式运行对于使基于LLM的应用程序对最终用户具有响应性至关重要。重要的LangChain原语，如聊天模型、输出解析器、提示模版、检索器和代理都实现了LangChain Runnable接口。该接口提供了两种通用的流式内容方法：

1. 同步stream和异步astream：流式传输链中的最终输出的默认实现。
2. 异步astream_events和异步astream_log：这些方法提供了一种从链中流式传输中间步骤和最终输出的方式。

## Stream

所有的Runnable对象都实现了一个名为stream的同步方法和一个名为astream的异步变体。这些方法皆在以块的形式流式传输最终输出，尽快返回每个块。只有在程序中的所有步骤都知道如何处理输入时，才能进行流式传输；即，逐个处理输入块，并产生相应的输出块。这种处理的复杂性可以有所不同，从简单的任务，如发出LLM生成的令牌，到更具挑战性的任务，如在整个JSON完成前流式传输JSON结果的部分。开始探索流式传输的最佳方法从LLM应用程序中最重要的组件开始-LLM本身！

### LLM和聊天模型

大型语言模型与其聊天变体是基于LLM的应用程序的主要瓶颈。大型语言模型可能需要几秒红才能对查询生成完整的响应。这比应用程序对最终用户具有响应性的约200-300毫秒的阀值要慢的多。使应用程序具有更高的响应性的关键策略是显示中间进度；即，逐个令牌流式传输模型的输出。我们将展示使用聊天模型流式传输的示例。以下选项中选择一个：

从同步stream API开始：

```python
chunks = []
for chunk in model.stream(”天空是什么颜色的):
    chunks.append(chunk)
    print(chunk.content, end="|", flush=True)
```

或者使用异步astream API

```python
chunks = []
async for chunk in model.stream(”天空是什么颜色的):
    chunks.append(chunk)
    print(chunk.content, end="|", flush=True)
```

得到一个称为AIMessageChunk的响应体，该块表示AIMessage的一部分。消息块是可叠加的

可以简单的将它们相加获得到目前为止的响应状态

```
AIMessageChunk(content="", id='')
```

### Chain（链）

几乎所有的LLM应用程序都涉及不止一步的操作，而不仅仅是调用语言模型。使用LangChain表达式语言（LCEL）构建一个简单的链，该链结合了一个提示、模型和解析器，并验证流式传输是否正常工作。将使用StrOutPutParser来解析模型的输出。这是一个简单的解析器，从AIMessageChunk中提取content字段，给出模型返回的token。

LCEL 是一种声明式的方式，通过将不同的 LangChain 原语链接在一起来指定一个“程序”。使用 LCEL 创建的链可以自动实现 stream 和 astream，从而实现对最终输出的流式传输。事实上，使用 LCEL 创建的链实现了整个标准 Runnable 接口。

```python
#astream_chain.py
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template("给我讲一个关于{topic}的笑话")
parser = StrOutputParser()
chain = prompt | model | parser
async for chunk in chain.astream({"topic": "鹦鹉"}):
    print(chunk, end="|", flush=True)
```

```
|一个|人|去|宠|物|店|买|鹦|鹉|。|店|员|说|：“|这|只|鹦|鹉|会|说|话|。”|
|买|回|家|后|，|那|人|发|现|鹦|鹉|只|会|说|一|句|话|：“|我|是|鹦|鹉|。”|
|那|人|就|去|找|店|员|，|说|：“|你|不|是|说|这|只|鹦|鹉|会|说|话|吗|？|它|只|会|说|‘|我|是|鹦|鹉|’|。”|
|店|员|回|答|：“|它|确|实|会|说|话|，|你|想|它|怎|么|可能|知|道|自|己|是|鹦|鹉|呢|？”||
```

请注意，即使我们在上面的链条末尾使用了parser，我们仍然可以获得流式输出。parser会对每个流式块进行操作。许多LCEL基元也支持这种转换式的流式传递，这在构建应用程序时非常方便。

自定义函数可以被设计为返回生成器，这样就能够操作流。

某些可运行实体，如提示模板和聊天模型，无法处理单个块，而是聚合所有先前的步骤。这些可运行实体可以中断流处理。

LangChain表达语言允许您将链的构建与使用模式（例如同步/异步、批处理/流式等）分开。如果这与您构建的内容无关，您也可以依赖于标准的命令式编程方法，通过在每个组件上调用invoke、batch或stream，将结果分配给变量，然后根据需要在下游使用它们。

### 使用输入流

如果您想要在输出生成时从中流式传输JSON，该怎么办呢？

如果您依赖json.loads来解析部分JSON，那么解析将失败，因为部分JSON不会是有效的JSON。

您可能会束手无策，声称无法流式传输JSON。

事实证明，有一种方法可以做到这一点——解析器需要在输入流上操作，并尝试将部分JSON“自动完成”为有效状态。

让我们看看这样一个解析器的运行，以了解这意味着什么。

```
model = ChatOpenAI(model="gpt-4")
parser = StrOutputParser()
chain = (
        model | JsonOutputParser()
    # 由于Langchain旧版本中的一个错误，JsonOutputParser未能从某些模型中流式传输结果
)
async def async_stream():
    async for text in chain.astream(
            "以JSON 格式输出法国、西班牙和日本的国家及其人口列表。"
            '使用一个带有“countries”外部键的字典，其中包含国家列表。'
            "每个国家都应该有键`name`和`population`"
    ):
        print(text, flush=True)
```

```
{}
{'countries': []}
{'countries': [{}]}
{'countries': [{'name': ''}]}
{'countries': [{'name': 'France'}]}
{'countries': [{'name': 'France', 'population': 670}]}
{'countries': [{'name': 'France', 'population': 670810}]}
{'countries': [{'name': 'France', 'population': 67081000}]}
{'countries': [{'name': 'France', 'population': 67081000}, {}]}
{'countries': [{'name': 'France', 'population': 67081000}, {'name': ''}]}
{'countries': [{'name': 'France', 'population': 67081000}, {'name': 'Spain'}]}
{'countries': [{'name': 'France', 'population': 67081000}, {'name': 'Spain', 'population': 467}]}
{'countries': [{'name': 'France', 'population': 67081000}, {'name': 'Spain', 'population': 467330}]}
{'countries': [{'name': 'France', 'population': 67081000}, {'name': 'Spain', 'population': 46733038}]}
{'countries': [{'name': 'France', 'population': 67081000}, {'name': 'Spain', 'population': 46733038}, {}]}
{'countries': [{'name': 'France', 'population': 67081000}, {'name': 'Spain', 'population': 46733038}, {'name': ''}]}
{'countries': [{'name': 'France', 'population': 67081000}, {'name': 'Spain', 'population': 46733038}, {'name': 'Japan'}]}
{'countries': [{'name': 'France', 'population': 67081000}, {'name': 'Spain', 'population': 46733038}, {'name': 'Japan', 'population': 126}]}
{'countries': [{'name': 'France', 'population': 67081000}, {'name': 'Spain', 'population': 46733038}, {'name': 'Japan', 'population': 126300}]}
{'countries': [{'name': 'France', 'population': 67081000}, {'name': 'Spain', 'population': 46733038}, {'name': 'Japan', 'population': 126300000}]}
```

## Stream events(事件流)

现在我们已经了解了stream和astream的工作原理，让我们进入事件流的世界。

事件流是一个beta API。这个API可能会根据反馈略微更改。

本指南演示了V2 API，并且需要 langchain-core >= 0.2。对于与旧版本 LangChain 兼容的V1 API，请参阅这里。

```
import langchain_core
langchain_core.__version__
```

为了使astream_events API正常工作：

- 在代码中尽可能使用async（例如，异步工具等）

- 如果定义自定义函数/可运行项，请传播回调

- 在没有 LCEL 的情况下使用可运行项时，请确保在LLMs上调用.astream()而不是.ainvoke以强制LLM流式传输令牌

#### 事件参考

下面是一个参考表，显示各种可运行对象可能发出的一些事件。

当流式传输正确实现时，对于可运行项的输入直到输入流完全消耗后才会知道。这意味着inputs通常仅包括end事件，而不包括start事件。包括`end`事件，而不包括`start`事件。

| 事件                | 名称         | 块                             | 输入                                          | 输出                                            |
| ------------------- | ------------ | ------------------------------ | --------------------------------------------- | ----------------------------------------------- |
| on_chat_model_start | [模型名称]   |                                | {"messages": [[SystemMessage, HumanMessage]]} |                                                 |
| on_chat_model_end   | [模型名称]   |                                | {"messages": [[SystemMessage, HumanMessage]]} | AIMessageChunk(content="hello world")           |
| on_llm_start        | [模型名称]   |                                | {'input': 'hello'}                            |                                                 |
| on_llm_stream       | [模型名称]   | 'Hello'                        |                                               |                                                 |
| on_llm_end          | [模型名称]   |                                | 'Hello human!'                                |                                                 |
| on_chain_start      | format_docs  |                                |                                               |                                                 |
| on_chain_stream     | format_docs  | "hello world!, goodbye world!" |                                               |                                                 |
| on_chain_end        | format_docs  |                                | [Document(...)]                               | "hello world!, goodbye world!"                  |
| on_tool_start       | some_tool    |                                | {"x": 1, "y": "2"}                            |                                                 |
| on_tool_end         | some_tool    |                                |                                               | {"x": 1, "y": "2"}                              |
| on_retriever_start  | [检索器名称] |                                | {"query": "hello"}                            |                                                 |
| on_retriever_end    | [检索器名称] |                                | {"query": "hello"}                            | [Document(...), ..]                             |
| on_prompt_start     | [模板名称]   |                                | {"question": "hello"}                         |                                                 |
| on_prompt_end       | [模板名称]   |                                | {"question": "hello"}                         | ChatPromptValue(messages: [SystemMessage, ...]) |

#### 聊天模型

让我们首先看一下聊天模型产生的事件。

```python
#astream_event.py
events = []
async for event in model.astream_events("hello", version="v2"):
    events.append(event)
```

```python
/home/eugene/src/langchain/libs/core/langchain_core/_api/beta_decorator.py:87: LangChainBetaWarning: This API is in beta and may change in the future.
  warn_beta(
```

嘿，API中那个有趣的version="v2"参数是什么意思？😾 这是一个beta API，我们几乎肯定会对其进行一些更改（事实上，我们已经做了！） 这个版本参数将允许我们最小化对您代码的破坏性更改。 简而言之，我们现在让您感到烦恼，这样以后就不必再烦恼了。 v2仅适用于 langchain-core>=0.2.0。

让我们看一下一些开始事件和一些结束事件。

```python
events[:3]
```

```python
[{'event': 'on_chat_model_start',
  'data': {'input': 'hello'},
  'name': 'ChatAnthropic',
  'tags': [],
  'run_id': 'a81e4c0f-fc36-4d33-93bc-1ac25b9bb2c3',
  'metadata': {}},
 {'event': 'on_chat_model_stream',
  'data': {'chunk': AIMessageChunk(content='Hello', id='run-a81e4c0f-fc36-4d33-93bc-1ac25b9bb2c3')},
  'run_id': 'a81e4c0f-fc36-4d33-93bc-1ac25b9bb2c3',
  'name': 'ChatAnthropic',
  'tags': [],
  'metadata': {}},
 {'event': 'on_chat_model_stream',
  'data': {'chunk': AIMessageChunk(content='!', id='run-a81e4c0f-fc36-4d33-93bc-1ac25b9bb2c3')},
  'run_id': 'a81e4c0f-fc36-4d33-93bc-1ac25b9bb2c3',
  'name': 'ChatAnthropic',
  'tags': [],
  'metadata': {}}]
```

```python
events[-2:]
```

```python
[{'event': 'on_chat_model_stream',
  'data': {'chunk': AIMessageChunk(content='?', id='run-a81e4c0f-fc36-4d33-93bc-1ac25b9bb2c3')},
  'run_id': 'a81e4c0f-fc36-4d33-93bc-1ac25b9bb2c3',
  'name': 'ChatAnthropic',
  'tags': [],
  'metadata': {}},
  {'event': 'on_chat_model_end',
  'data': {'output': AIMessageChunk(content='Hello! How can I assist you today?', id='run-a81e4c0f-fc36-4d33-93bc-1ac25b9bb2c3')},
  'run_id': 'a81e4c0f-fc36-4d33-93bc-1ac25b9bb2c3',
  'name': 'ChatAnthropic',
  'tags': [],
  'metadata': {}}]
```

# LangChain服务部署与链路监控

## LangServe服务部署

### 概述

LangServe帮助开发者将 LangChain 可运行和链部署为 REST API。

该库集成了 FastAPI 并使用 pydantic 进行数据验证。

Pydantic 是一个在 Python中用于数据验证和解析的第三方库，现在是Python中使用广泛的数据验证库。

- 它利用声明式的方式定义数据模型和Python 类型提示的强大功能来执行数据验证和序列化，使您的代码更可靠、更可读、更简洁且更易于调试。

- 它还可以从模型生成 JSON 架构，提供了自动生成文档等功能，从而轻松与其他工具集成。

此外，它提供了一个客户端，可用于调用部署在服务器上的可运行对象。JavaScript 客户端可在 LangChain.js 中找到。

### 特性

- 从 LangChain 对象自动推断输入和输出模式，并在每次 API 调用中执行，提供丰富的错误信息。

- 带有 JSONSchema 和 Swagger 的 API 文档页面（插入示例链接）。

- 高效的 /invoke、/batch 和 /stream 端点，支持单个服务器上的多个并发请求。

- /stream_log 端点，用于流式传输链/代理的所有（或部分）中间步骤。

- 新功能 自 0.0.40 版本起，支持 /stream_events，使流式传输更加简便，无需解析 /stream_log 的输出。

- 使用经过严格测试的开源 Python 库构建，如 FastAPI、Pydantic、uvloop 和 asyncio。

- 使用客户端 SDK 调用 LangServe 服务器，就像本地运行可运行对象一样（或直接调用 HTTP API）。

### 限制

- 目前不支持服务器发起的事件的客户端回调。

- 当使用 Pydantic V2 时，将不会生成 OpenAPI 文档。FastAPI 支持混合使用 pydantic v1 和 v2 命名空间。更多细节请参见下面的章节。
