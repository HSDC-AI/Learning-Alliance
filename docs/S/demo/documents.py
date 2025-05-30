from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

base_url = "http://10.255.4.108:8080/v1"
model_name = "text-embedding-3-large"
api_key = "sk-3BEJwQPhsyVSzDW2C963Af69A6Bf4b608810Dd78E2Bb4452"

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]
#
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=OpenAIEmbeddings(
        model=model_name,
        openai_api_key=api_key,
        base_url=base_url
    )
)
# print(vectorstore.similarity_search("cat"))
# # 打分
# print(vectorstore.similarity_search_with_score("cat"))

# 嵌入式查询相似度
embedding = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=api_key,
    base_url=base_url
).embed_query("cat")

print(vectorstore.similarity_search_by_vector(embedding))