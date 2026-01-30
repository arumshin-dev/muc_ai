from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="MUC AI Backend")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    message: str


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None


# 샘플 데이터
items = [
    {"id": 1, "name": "Item 1", "description": "First item"},
    {"id": 2, "name": "Item 2", "description": "Second item"},
    {"id": 3, "name": "Item 3", "description": "Third item"},
]


@app.get("/")
async def root():
    return {"message": "Welcome to MUC AI Backend"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "healthy", "message": "Backend is running"}


@app.get("/api/items", response_model=list[Item])
async def get_items():
    return items


@app.get("/api/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"id": item_id, "name": "Not found", "description": None}


@app.post("/api/items", response_model=Item)
async def create_item(item: Item):
    items.append(item.dict())
    return item
