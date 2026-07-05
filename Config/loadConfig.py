import yaml

def load_config():
    with open(r"C:\Users\intel\OneDrive\Desktop\Studies\Qdrant_RAG\Config\config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config