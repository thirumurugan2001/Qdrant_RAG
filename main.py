from fastapi import FastAPI
from rag_utils.model import RAG
from rag_utils.controller import ragController
app = FastAPI()

# Define a POST endpoint for the chatbot that accepts a question and returns a response based on the RAG process
@app.post("/chatbot/about/")
async def rag(item: RAG):
    try:
        # Call the ragController function with the provided question and return the response
        response = ragController(item.Question)
        return response
    except Exception as e:  
        return {
            "error": str(e),
            "statusCode": 500
        }