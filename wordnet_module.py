# wordnet_module.py - Word Sense Disambiguation using NLTK WordNet

import nltk
from nltk.corpus import wordnet as wn

# Download required NLTK data
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4')

def get_word_sense(word):
    """
    Get the most common definition of a word using WordNet.
    This is Word Sense Disambiguation (WSD).
    """
    synsets = wn.synsets(word)
    if synsets:
        # Return first (most common) synset definition
        return synsets[0].definition()
    return "No definition found"

def get_synonyms(word):
    """
    Get synonyms of a word using WordNet.
    Used to expand skill matching beyond exact terms.
    """
    synonyms = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonym = lemma.name().replace('_', ' ').lower()
            synonyms.add(synonym)
    return list(synonyms)

def simplified_lesk(word, context_sentence):
    """
    Simplified Lesk Algorithm for Word Sense Disambiguation.
    Finds the best synset for a word given its context.
    """
    best_sense = None
    max_overlap = 0
    context = set(context_sentence.lower().split())
    
    for synset in wn.synsets(word):
        # Get definition and examples as signature
        signature = set(synset.definition().lower().split())
        for example in synset.examples():
            signature.update(example.lower().split())
        
        # Count overlap between context and signature
        overlap = len(context & signature)
        
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = synset
    
    if best_sense:
        return best_sense.definition()
    return get_word_sense(word)
