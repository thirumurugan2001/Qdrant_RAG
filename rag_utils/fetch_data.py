from pypdf import PdfReader
from Config.loadConfig import load_config
config = load_config()

def load_pdf() -> str:
    try:
        reader = PdfReader(config['document']['pdf_path'])
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        print(f"Loaded PDF text successfully. Length: {len(text)} characters.")
        return text
    except Exception as e:
        print(f"Error in load_pdf: {str(e)}")
        return None
