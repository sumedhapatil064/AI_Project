from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer

app = FastAPI(title="Semantic Product Search")
client = chromadb.Client()
collection = client.create_collection("products")
model = SentenceTransformer("all-MiniLM-L6-v2")

class Item(BaseModel):
    id: str
    title: str
    description: str

class IndexIn(BaseModel):
    items: List[Item]

class QueryIn(BaseModel):
    q: str
    top_k: int = 5

@app.post("/index")
def index(inp: IndexIn):
    docs = [f"{it.title}. {it.description}" for it in inp.items]
    emb = model.encode(docs).tolist()
    collection.add(ids=[it.id for it in inp.items], documents=docs, embeddings=emb)
    return {"indexed": len(inp.items)}

@app.post("/search")
def search(inp: QueryIn):
    q_emb = model.encode([inp.q]).tolist()
    res = collection.query(query_embeddings=q_emb, n_results=inp.top_k)
    return res
