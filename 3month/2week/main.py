from fastapi import FastAPI, Path
from pydantic import BaseModel

# День 10: FastAPI. Первый сервер

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def read_root():
    return {"message": "Hello FastApi"}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item, "status": "created"}

@app.get("/items/{item_id}")
def read_item(item_id: int = Path(..., gt=0)):
    return {"item_id": item_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)