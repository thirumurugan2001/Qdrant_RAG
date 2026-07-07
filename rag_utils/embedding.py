from dotenv import load_dotenv
from Config.loadConfig import load_config
import cohere
import os
load_dotenv()
config = load_config()

# Function to get the embedding of the text
def get_embedding(text):
    try:
        
        # Load the Cohere API key from environment variables and initialize the Cohere client
        token = os.getenv("COHERE_API_KEY")
        co = cohere.Client(token)  

        # Generate the embedding for the provided text using the specified model and input type from the configuration
        embedding = co.embed(
            model=config['cohere']['model'],
            input_type=config['cohere']['input_type'],
            texts=[text]
            ).embeddings[0] 
        return embedding
    except Exception as e:
        print("Error in getting embedding: ", str(e))
        return None