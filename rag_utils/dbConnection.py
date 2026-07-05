
from qdrant_client import QdrantClient
from Config.loadConfig import load_config
config = load_config()

def Dbconnection():
    try:
        client = QdrantClient(host=config["qdrant"]["host"], port=config["qdrant"]["port"])
        print("Connected to Qdrant successfully.")
        return client
    except Exception as e:
        print(f"Error in Dbconnection: {str(e)}")
        return {
            "Error": str(e),
            "statusCode": 500,
            "message": "Error occurred while connecting to the database.",
            "Status": False
        }