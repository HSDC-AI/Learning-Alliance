from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Simple API",
    description="A simple API for testing",
    version="1.0.0"
)

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: Item):
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 