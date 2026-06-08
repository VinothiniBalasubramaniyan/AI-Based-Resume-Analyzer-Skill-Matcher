from sentence_transformers import SentenceTransformer, util

print("Loading Sentence-BERT model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("Model loaded successfully!")

def split_chunks(text, chunk_size=200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks

def match_resume_jd(resume_text, jd_text):
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    # Split long text into chunks
    resume_chunks = split_chunks(resume_text)
    jd_chunks = split_chunks(jd_text)

    # Encode all chunks
    resume_embeddings = model.encode(resume_chunks, convert_to_tensor=True)
    jd_embeddings = model.encode(jd_chunks, convert_to_tensor=True)

    # Take best similarity across all chunk combinations
    best_score = 0.0
    for r_emb in resume_embeddings:
        for j_emb in jd_embeddings:
            score = util.cos_sim(r_emb, j_emb).item()
            if score > best_score:
                best_score = score

    return max(0.0, min(1.0, best_score))