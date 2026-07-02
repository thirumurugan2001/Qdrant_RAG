from fastapi import FastAPI
from model import *
from middleware import setup_cors
app = FastAPI()
setup_cors(app)

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