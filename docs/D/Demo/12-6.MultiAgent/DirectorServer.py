import uuid
from Director import graph

config = {
    "configurable": {
        "thread_id": str(uuid.uuid4())
    }
}
query = "给我讲一个笑话"
res = graph.invoke({"messages": [query]}, config=config)
# print(res)
print(res["messages"][-1].content)








