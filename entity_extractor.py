# entity_extractor.py - Extract Skills, Actions, Attributes from Resume Text

# ============================================================
# LARGE SKILLS DATABASE - 100+ skills covered
# ============================================================
SKILLS_DB = [
    # --- Programming Languages ---
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "r", "go", "golang", "rust", "swift", "kotlin", "php", "ruby",
    "scala", "perl", "matlab", "bash", "shell", "dart", "lua",

    # --- Web Frontend ---
    "html", "css", "react", "angular", "vue", "vuejs", "reactjs",
    "nextjs", "nuxtjs", "bootstrap", "tailwind", "jquery", "sass",
    "webpack", "figma", "xml", "json",

    # --- Web Backend ---
    "nodejs", "flask", "django", "fastapi", "spring", "springboot",
    "express", "laravel", "asp.net", "rails", "graphql", "rest api",
    "microservices", "api",

    # --- Data Science & ML ---
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "data science", "data analysis", "data mining",
    "statistics", "mathematics", "linear algebra", "neural network",
    "artificial intelligence", "ai", "reinforcement learning",
    "transfer learning", "feature engineering", "model training",

    # --- ML Frameworks ---
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
    "xgboost", "lightgbm", "catboost", "hugging face", "transformers",
    "bert", "gpt", "sentence-bert", "spacy", "nltk", "opencv",
    "yolo", "fastai",

    # --- Data Tools ---
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "tableau", "power bi", "excel", "google sheets",
    "hadoop", "spark", "kafka", "airflow", "dbt",

    # --- Database ---
    "sql", "mysql", "postgresql", "sqlite", "oracle", "mongodb",
    "redis", "firebase", "cassandra", "dynamodb", "elasticsearch",
    "nosql", "database",

    # --- Cloud & DevOps ---
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "jenkins", "git", "github", "gitlab", "bitbucket", "linux",
    "unix", "terraform", "ansible", "ci/cd", "devops", "nginx",
    "apache", "heroku", "vercel", "netlify",

    # --- Mobile ---
    "android", "ios", "react native", "flutter", "xamarin",

    # --- Other Tech ---
    "iot", "embedded systems", "raspberry pi", "arduino",
    "blockchain", "cybersecurity", "networking", "cloud computing",
    "agile", "scrum", "jira", "unit testing", "selenium",
    "postman", "figma", "photoshop",
]

# ============================================================
# PROFESSIONAL ACTIONS DATABASE
# ============================================================
ACTIONS_DB = [
    "developed", "designed", "implemented", "built", "created",
    "managed", "led", "optimized", "deployed", "tested",
    "analyzed", "maintained", "automated", "integrated",
    "architected", "collaborated", "delivered", "improved",
    "enhanced", "reduced", "increased", "launched", "migrated",
    "monitored", "configured", "documented", "researched",
    "trained", "mentored", "presented", "coordinated",
    "debugged", "refactored", "scaled", "secured", "validated",
    "contributed", "published", "achieved", "handled", "operated",
]

# ============================================================
# PROFESSIONAL ATTRIBUTES DATABASE
# ============================================================
ATTRIBUTES_DB = [
    "proficient", "experienced", "skilled", "certified", "expert",
    "knowledgeable", "familiar", "trained", "specialized", "qualified",
    "enthusiastic", "motivated", "dedicated", "passionate", "creative",
    "analytical", "detail-oriented", "result-oriented", "self-motivated",
    "team player", "leadership", "communication", "problem-solving",
    "critical thinking", "fast learner", "adaptable", "innovative",
]

def extract_entities(text):
    """
    Extract Skills, Actions, and Attributes from preprocessed text.
    
    Args:
        text: preprocessed (cleaned + lemmatized) text string
        
    Returns:
        dict with keys: skills, actions, attributes
    """
    text_lower = text.lower()
    
    # Extract skills - check if skill phrase exists in text
    skills = []
    for skill in SKILLS_DB:
        # Use word boundary matching for short skills to avoid false matches
        if len(skill) <= 2:
            # For very short skills like "r", "c" match as whole word
            import re
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                skills.append(skill)
        else:
            if skill in text_lower:
                skills.append(skill)
    
    # Extract actions - match professional verbs
    actions = []
    for action in ACTIONS_DB:
        if action in text_lower:
            actions.append(action)
    
    # Extract attributes - match professional qualifiers
    attributes = []
    for attr in ATTRIBUTES_DB:
        if attr in text_lower:
            attributes.append(attr)
    
    return {
        "skills": list(set(skills)),
        "actions": list(set(actions)),
        "attributes": list(set(attributes))
    }

def get_missing_skills(resume_skills, jd_skills):
    """
    Find skills required in JD but missing from resume.
    """
    resume_set = set([s.lower() for s in resume_skills])
    jd_set = set([s.lower() for s in jd_skills])
    missing = jd_set - resume_set
    return list(missing)
