# app.py - AI Resume Analyzer - Main Application
# FIXED VERSION: Score consistency, expanded skills, better suggestions

import gradio as gr
import sys
import os

# Add modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.extractor import extract_text
from modules.preprocess import preprocess
from modules.wordnet_module import get_word_sense, simplified_lesk
from modules.entity_extractor import extract_entities, get_missing_skills
from modules.json_generator import generate_json
from modules.matcher import match_resume_jd
from modules.scorer import calculate_score, classify, get_suggestions

# ============================================================
# MAIN ANALYSIS FUNCTION
# ============================================================

def analyze(resume_file, job_description):
    """
    Main analysis pipeline:
    Step 1: Extract text from PDF
    Step 2: Preprocess text (clean, tokenize, lemmatize)
    Step 3: WordNet WSD (demo)
    Step 4: Entity extraction (skills, actions, attributes)
    Step 5: JSON generation
    Step 6: Semantic matching (Sentence-BERT)
    Step 7: Score calculation
    Step 8: Classification
    Step 9: Missing skills & suggestions
    """

    # ---- Input Validation ----
    if resume_file is None:
        return "❌ Error", "Please upload a resume PDF", "", "", "", ""

    if not job_description or job_description.strip() == "":
        return "❌ Error", "Please enter a job description", "", "", "", ""

    try:
        # ---- STEP 1: Extract Text from PDF ----
        raw_text = extract_text(resume_file.name)

        if not raw_text or "Error" in raw_text:
            return "❌ Error", "Could not read PDF. Try another file.", "", "", "", ""

        # ---- STEP 2: Preprocess ----
        clean_resume = preprocess(raw_text)
        clean_jd = preprocess(job_description)

        # ---- STEP 3: WordNet WSD (demonstration) ----
        # Applied to key words in the resume for disambiguation
        sample_word = clean_resume.split()[0] if clean_resume.split() else "develop"
        wsd_result = simplified_lesk(sample_word, clean_resume)

        # ---- STEP 4: Entity Extraction ----
        resume_entities = extract_entities(clean_resume)
        jd_entities = extract_entities(clean_jd)

        # ---- STEP 5: Missing Skills ----
        missing = get_missing_skills(
            resume_entities["skills"],
            jd_entities["skills"]
        )

        # ---- STEP 6: Semantic Matching (Sentence-BERT) ----
        similarity = match_resume_jd(clean_resume, clean_jd)

        # ---- STEP 7: Score Calculation ----
        # Score = 70% semantic similarity + 30% skill overlap
        score = calculate_score(
            similarity,
            resume_entities["skills"],
            jd_entities["skills"]
        )

        # ---- STEP 8: Classification ----
        result = classify(score)

        # ---- STEP 9: Suggestions ----
        suggestions_list = get_suggestions(score, missing, resume_entities["skills"])
        suggestions_text = "\n".join([f"• {s}" for s in suggestions_list])

        # ---- STEP 10: JSON Output ----
        json_output = generate_json(
            resume_entities,
            score=score,
            result=result,
            missing_skills=missing
        )

        # ---- Format Outputs ----
        score_display = f"{score}/100  |  Semantic Match: {round(similarity * 100, 2)}%"
        skills_display = ", ".join(resume_entities["skills"]) if resume_entities["skills"] else "No skills detected"
        missing_display = ", ".join(missing) if missing else "✅ No missing skills — great match!"

        return (
            score_display,
            result,
            skills_display,
            missing_display,
            suggestions_text,
            json_output
        )

    except Exception as e:
        return f"❌ Error: {str(e)}", "", "", "", "", ""


# ============================================================
# GRADIO INTERFACE
# ============================================================

with gr.Blocks(
    theme=gr.themes.Soft(),
    title="AI Resume Analyzer"
) as app:

    # Title
    gr.Markdown("""
    ### AI-Powered Resume Analysis Using Text Processing and Transformer-Based Model Matching
    """)

    gr.Markdown("---")

    # Input Section
    with gr.Row():
        with gr.Column(scale=1):
            resume_input = gr.File(
                label="📄 Upload Resume (PDF)",
                file_types=[".pdf"]
            )
        with gr.Column(scale=1):
            jd_input = gr.Textbox(
                label="💼 Enter Job Description",
                lines=10,
                placeholder="Paste the job description here...\n\nExample:\nWe are looking for a Python developer with experience in Machine Learning, TensorFlow, SQL, Docker, and AWS..."
            )

    # Analyze Button
    analyze_btn = gr.Button(
        "🔍 Analyze Resume",
        variant="primary",
        size="lg"
    )

    gr.Markdown("---")
    gr.Markdown("## 📊 Analysis Results")

    # Output Section - Row 1
    with gr.Row():
        score_out = gr.Textbox(
            label="🎯 Match Score",
            interactive=False
        )
        result_out = gr.Textbox(
            label="📋 Result / Classification",
            interactive=False
        )

    # Output Section - Row 2
    with gr.Row():
        skills_out = gr.Textbox(
            label="✅ Skills Found in Resume",
            interactive=False,
            lines=3
        )
        missing_out = gr.Textbox(
            label="❌ Missing Skills",
            interactive=False,
            lines=3
        )

    # Suggestions
    suggestions_out = gr.Textbox(
        label="💡 Improvement Suggestions",
        interactive=False,
        lines=5
    )

    # JSON Output
    json_out = gr.Textbox(
        label="🗂️ JSON Output (Structured Data)",
        interactive=False,
        lines=15
    )

    # Connect button to function
    analyze_btn.click(
        fn=analyze,
        inputs=[resume_input, jd_input],
        outputs=[
            score_out,
            result_out,
            skills_out,
            missing_out,
            suggestions_out,
            json_out
        ]
    )

    gr.Markdown("---")
    gr.Markdown("""
    ### 📌 How It Works
    1. **Resume Parser** — Extracts text from PDF using PyPDF2
    2. **NLP Preprocessing** — Cleaning, Tokenization, Lemmatization using spaCy
    3. **WordNet WSD** — Word Sense Disambiguation using NLTK WordNet
    4. **Skill Extraction** — Extracts Skills, Actions, Attributes from text
    5. **Semantic Matching** — Sentence-BERT Transformer model computes similarity
    6. **Scoring Engine** — 70% semantic + 30% skill overlap = Final Score
    7. **Classification** — Recommended / Good / Average / Bad
    """)


# ============================================================
# LAUNCH APP
# ============================================================

if __name__ == "__main__":
    app.launch(
        share=False,
        show_error=True,
        server_port=7861        
    )