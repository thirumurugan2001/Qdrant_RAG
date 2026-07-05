from rag_utils.embedding import get_embedding
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid

def setup_collection(client, collection_name, vector_size):
    try:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size, 
                distance=Distance.COSINE
            )
        )
        return True
    except Exception as e:
        print(f"Error in setting up collection: {str(e)}")
        return False
    
def ingest_chunks(client, collection_name, chunks):
    try :
        points = []
        for chunk in chunks:
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()), 
                    vector=get_embedding(chunk), 
                    payload={"text": chunk}  
                )
            )
        client.upsert(
            collection_name=collection_name,
            points=points
        )
        print(f"Ingested {len(points)} chunks into collection '{collection_name}'.")
        return True
    except Exception as e:
        print(f"Error in ingesting chunks: {str(e)}")
        return False