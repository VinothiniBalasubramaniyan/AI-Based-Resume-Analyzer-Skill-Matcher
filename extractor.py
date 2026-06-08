# extractor.py - Extract text from PDF (Digital + Scanned)

from PyPDF2 import PdfReader

def extract_text(file_path):
    """
    Extract text from PDF file.
    Supports digital PDFs using PyPDF2.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if not text.strip():
            return "Could not extract text from this PDF."
        
        return text.strip()
    
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
