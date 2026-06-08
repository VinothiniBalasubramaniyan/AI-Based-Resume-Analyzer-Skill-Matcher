# AI Resume Analyzer
## AI-Powered Resume Analysis Using Text Processing and Model Generation

---

## SETUP INSTRUCTIONS

### Step 1 - Install Python libraries
Open terminal / command prompt and run:

```
pip install gradio PyPDF2 spacy nltk sentence-transformers
```

### Step 2 - Download spaCy model
```
python -m spacy download en_core_web_sm
```

### Step 3 - Run the app
```
python app.py
```

### Step 4 - Open browser
Go to: http://localhost:7860

---

## PROJECT STRUCTURE

```
ai_resume_analyzer/
│
├── app.py                    ← Main application (run this)
├── requirements.txt          ← All dependencies
│
└── modules/
    ├── extractor.py          ← PDF text extraction (PyPDF2)
    ├── preprocess.py         ← Text cleaning (spaCy)
    ├── wordnet_module.py     ← Word Sense Disambiguation (NLTK)
    ├── entity_extractor.py   ← Skill/Action/Attribute extraction
    ├── json_generator.py     ← JSON output generation
    ├── matcher.py            ← Sentence-BERT semantic matching
    └── scorer.py             ← Score calculation & classification
```

---

## FIXES IN THIS VERSION

1. Score and Match% are now consistent (no more double counting)
2. Skills database expanded to 100+ skills
3. Actions database uses fixed list (not word endings)
4. Attributes database uses fixed list (not word endings)
5. Better suggestions based on score range
6. JSON output includes score, result, and missing skills
7. Better UI with clear labels and instructions
