from qdrant_client import QdrantClient
from rag_utils.dbConnection import Dbconnection
from rag_utils.fetch_data import load_pdf
from rag_utils.preprocessing import preprocess
from rag_utils.chunking import chunk_text
from rag_utils.vectorstore import  setup_collection, ingest_chunks
from rag_utils.embedding import get_embedding
from Config.loadConfig import load_config
config = load_config()
    

def Create_rag_pipeline():
    try:
        text = load_pdf()
        if text is None:
            return {
                "Error": "Failed to load PDF.",
                "statusCode": 500,
                "message": "Error occurred while loading the PDF.",
                "Status": False
            }
        
        cleaned_text = preprocess(text)
        if cleaned_text is None:
            return {
                "Error": "Failed to preprocess text.",
                "statusCode": 500,
                "message": "Error occurred while preprocessing the text.",
                "Status": False
            }
        
        chunks = chunk_text(cleaned_text)
        if not chunks:
            return {
                "Error": "Failed to chunk text.",
                "statusCode": 500,
                "message": "Error occurred while chunking the text.",
                "Status": False
            }
        
        client = Dbconnection()
        if client is None:
            return {
                "Error": "Failed to connect to Qdrant.",
                "statusCode": 500,
                "message": "Error occurred while connecting to Qdrant.",
                "Status": False
            }
        
        if not setup_collection(client, config["qdrant"]["collection_name"],config["qdrant"]["vector_size"]):
            return {
                "Error": "Failed to set up Qdrant collection.",
                "statusCode": 500,
                "message": "Error occurred while setting up the Qdrant collection.",
                "Status": False
            }
        
        if not ingest_chunks(client, config["qdrant"]["collection_name"],chunks):
            return {
                "Error": "Failed to ingest chunks into Qdrant.",
                "statusCode": 500,
                "message": "Error occurred while ingesting chunks into Qdrant.",
                "Status": False
            }
        print("RAG pipeline created successfully.")
    
    except Exception as e:
        print(f"Error in Create_rag_pipeline: {str(e)}")
        return {
            "Error": str(e),
            "statusCode": 500,
            "message": "Error occurred while creating the RAG pipeline.",
            "Status": False
        }

if __name__ == "__main__":
    result = Create_rag_pipeline()
    if result is not None and "Error" in result:
        print(f"Pipeline creation failed: {result['Error']}")
    else:
        print("Pipeline created successfully.")     
