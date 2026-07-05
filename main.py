from fastapi import FastAPI
from rag_utils.model import RAG
from rag_utils.controller import ragController
app = FastAPI()

@app.post("/chatbot/about/")
async def rag(item: RAG):
    try:
        response = ragController(item.Question)
        return response
    except Exception as e:  
        return {
            "error": str(e),
            "statusCode": 500
        }