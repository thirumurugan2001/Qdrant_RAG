from fastapi import FastAPI
from model import *
from ragPiplinne import middleware
app = FastAPI()

@app.post("/chatbot/about/")
async def rag(item: RAG):
    try:
        response = middleware(item.Question)

        
        
        # texts = []
        # for hit in top_matches.points:
        #     print(f"\n--- Retrieved Chunk (Score: {hit.score:.4f}) ---\n")
        #     texts.append(hit.payload["text"])
        #     print(hit.payload["text"])

        # context = "\n\n".join(texts)

        # # Step 6 - Generate answer by asking Ollama
        # answer = ask_ollama(question, context, config)
        # print("\n--- Answer ---\n")
        # print(answer)
        return response
    except Exception as e:
        return {
            "error": str(e),
            "statusCode": 500
        }