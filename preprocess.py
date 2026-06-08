# preprocess.py - Text Cleaning, Tokenization, Lemmatization using spaCy

import spacy
import re

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    """
    Clean and normalize text:
    - Remove URLs, emails, special characters
    - Lowercase
    - Tokenize
    - Remove stopwords
    - Lemmatize
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove phone numbers
    text = re.sub(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', '', text)
    
    # Remove special characters but keep letters, numbers, spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Process with spaCy
    doc = nlp(text.lower())
    
    # Keep meaningful tokens - remove stopwords, punctuation, short words
    tokens = [
        token.lemma_ 
        for token in doc 
        if not token.is_stop 
        and not token.is_punct 
        and len(token.text) > 2
        and token.is_alpha
    ]
    
    return " ".join(tokens)
