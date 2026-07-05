from fastapi import FastAPI
from model import *
from ragPiplinne import middleware
app = FastAPI()

@app.post("/chatbot/about/")
async def rag(item: RAG):
    try:
        response = middleware(item.Question)
        # Step 5 - Querying the collection  
        # question = input("\nEnter your question about the document: ")
        # query_vector = get_embedding([question], config["ollama"]["embedding_model"])

        # top_matches = client.query_points(
        #     collection_name=config["qdrant"]["collection_name"],
        #     query=query_vector[0],
        #     limit=3)
        
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