from xmlrpc import client
from rag_utils.embedding import get_embedding
from ConnectChatBot import ConnectChatBot
from rag_utils.dbConnection import Dbconnection
from Config.loadConfig import load_config
config = load_config()

# Function to get the most relevant answer from the database
def rag(Question):
    try:
        client=Dbconnection()
        embedding = get_embedding(Question)
        top_matches = client.query_points(collection_name=config["qdrant"]["collection_name"],query=embedding[0],limit=2)
        texts = []
        for hit in top_matches.points:
            texts.append(hit.payload["text"])
        context = "\n".join(texts)
        response = ConnectChatBot(Question,context)
        if response is None:
            return {
                "statusCode":200,
                "status":False,
                "message":"No relevant information found in the database.",
            }
        return {
            "statusCode":200,
            "status":True,
            "message":"Relevant information found.",
            "response":response
        }
    except Exception as e:
        print(f"Error in rag function: {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400,
                "message":"Error occurred while processing the request.",
                "Status":False
            }
