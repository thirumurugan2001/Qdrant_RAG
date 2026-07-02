from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid

def setup_collection(client, collection_name, vector_size):
    
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size, 
            distance=Distance.COSINE
        )
    )
    
def ingest_chunks(client, collection_name, chunks, embeddings):

    points = []
    for chunk, vector in zip(chunks, embeddings):

       points.append(
           PointStruct(
               id=str(uuid.uuid4()), 
               vector=vector, 
               payload={"text": chunk}  
           )
       )
    
    client.upsert(
        collection_name=collection_name,
        points=points
    )


# Function to connect to SingleStore
def dbconnection():
    try :
        conn = s2.connect( 
            host = os.getenv("DB_HOST"), 
            port = os.getenv("PORT"), 
            user =os.getenv("DB_USER"), 
            password = os.getenv("DB_PASSWORD") , 
            database =  os.getenv("DB_NAME")
        )
        print("Connected to SingleStore")
        return conn
    except Exception as e:
        print("Error in connecting to SingleStore: ", str(e))
        return None
    