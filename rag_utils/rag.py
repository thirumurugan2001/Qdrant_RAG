from xmlrpc import client
from rag_utils.embedding import get_embedding
from ConnectChatBot import ConnectChatBot
from rag_utils.dbConnection import Dbconnection
from Config.loadConfig import load_config
config = load_config()
# Function to get the most relevant answer from the database
def rag(Question):
    try:
        conn=Dbconnection()
        embedding = get_embedding(Question)
        top_matches = client.query_points(
            collection_name=config["qdrant"]["collection_name"],
            query=embedding[0],

            limit=3)
        texts = []
        for hit in top_matches.points:
            texts.append(hit.payload["text"])

        context = "\n\n".join(texts)

        response = ConnectChatBot(Question,context)
        print(response)
        return {
            "statusCode":200,
            "status":False,
            "message":"No relevant information found in the database.",

        }
    except Exception as e:
        print(f"Error in rag function: {str(e)}")
        return {
                "Error":str(e),
                "statusCode":400,
                "message":"Error occurred while processing the request.",
                "Status":False
            }
