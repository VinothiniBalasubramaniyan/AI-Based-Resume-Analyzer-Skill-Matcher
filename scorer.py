# scorer.py - Calculate Final Match Score and Classification
# FIXED: Score and Match% are now consistent

def calculate_score(similarity, resume_skills, jd_skills):
    """
    Calculate final match score combining:
    - 70% Semantic similarity (Sentence-BERT cosine similarity)
    - 30% Skill overlap (entity matching)
    
    Args:
        similarity: float 0-1 from Sentence-BERT cosine similarity
        resume_skills: list of skills extracted from resume
        jd_skills: list of skills extracted from job description
        
    Returns:
        int: final score 0-100
    """
    # Semantic similarity score (70% weight)
    semantic_score = similarity * 70
    
    # Skill overlap score (30% weight)
    if len(jd_skills) > 0:
        matched = set([s.lower() for s in resume_skills]) & \
                  set([s.lower() for s in jd_skills])
        skill_overlap_ratio = len(matched) / len(jd_skills)
        skill_score = skill_overlap_ratio * 30
    else:
        # No skills in JD — give partial skill score based on resume skills
        skill_score = min(15, len(resume_skills) * 2)
    
    # Total score
    total = semantic_score + skill_score
    total = max(0, min(100, total))  # Clamp between 0-100
    
    return round(total)


def classify(score):
    """
    Classify match score into categories.
    
    Args:
        score: int 0-100
        
    Returns:
        str: classification label with emoji
    """
    if score >= 75:
        return "✅ RECOMMENDED"
    elif score >= 55:
        return "👍 GOOD"
    elif score >= 35:
        return "⚠️ AVERAGE"
    else:
        return "🔴 BAD"


def get_suggestions(score, missing_skills, resume_skills):
    """
    Generate improvement suggestions based on score and missing skills.
    
    Args:
        score: int match score
        missing_skills: list of skills missing from resume
        resume_skills: list of skills found in resume
        
    Returns:
        list of suggestion strings
    """
    suggestions = []
    
    # Add missing skills suggestion
    if missing_skills:
        suggestions.append(
            f"Add these missing skills to your resume: {', '.join(missing_skills)}"
        )
    
    # Score-based suggestions
    if score < 35:
        suggestions.append(
            "Your resume needs significant improvement. "
            "Tailor your resume specifically for this job description."
        )
        suggestions.append(
            "Add more relevant technical skills and project experience."
        )
        suggestions.append(
            "Include measurable achievements (e.g., 'Improved performance by 30%')."
        )
    elif score < 55:
        suggestions.append(
            "Improve resume with more relevant keywords from the job description."
        )
        suggestions.append(
            "Add more project descriptions that match the job requirements."
        )
    elif score < 75:
        suggestions.append(
            "Good match! Add a few more specific skills to strengthen your profile."
        )
        suggestions.append(
            "Highlight relevant achievements and quantify your impact."
        )
    else:
        suggestions.append(
            "Excellent match! Your resume is well-aligned with this job."
        )
        suggestions.append(
            "Prepare for technical interview questions related to your listed skills."
        )
    
    # General suggestions
    if len(resume_skills) < 5:
        suggestions.append(
            "Add more technical skills to your resume skills section."
        )
    
    return suggestions
