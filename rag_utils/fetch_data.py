from pypdf import PdfReader
PDF_PATH = "hr_policy_detailed_5_pages.pdf"

def load_pdf() -> str:
    try:
        reader = PdfReader(PDF_PATH)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        print(f"Loaded PDF text successfully. Length: {len(text)} characters.")
        return text
    except Exception as e:
        print(f"Error in load_pdf: {str(e)}")
        return None
