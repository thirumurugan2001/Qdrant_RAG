from fastapi import FastAPI
from model import *
from ragPiplinne import middleware
app = FastAPI()

@app.post("/chatbot/about/")
async def rag(item: RAG):
    try:
        response = middleware(item.Question)
        return response
    except Exception as e:
        return {
            "error": str(e),
            "statusCode": 500
        }