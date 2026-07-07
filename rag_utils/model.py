from pydantic import BaseModel

# Define a Pydantic model for RAG (Retrieval-Augmented Generation) with a single field for the question
class RAG(BaseModel): 
    Question: str