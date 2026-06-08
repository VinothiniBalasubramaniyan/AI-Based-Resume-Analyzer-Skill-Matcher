# json_generator.py - Generate Structured JSON Output

import json
from datetime import datetime

def generate_json(entities, score=None, result=None, missing_skills=None):
    """
    Generate a structured JSON output from extracted entities.
    
    Args:
        entities: dict with skills, actions, attributes
        score: match score (optional)
        result: classification result (optional)
        missing_skills: list of missing skills (optional)
        
    Returns:
        formatted JSON string
    """
    output = {
        "resume_analysis": {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "extracted_entities": {
                "skills": entities.get("skills", []),
                "actions": entities.get("actions", []),
                "attributes": entities.get("attributes", [])
            },
            "skill_count": len(entities.get("skills", [])),
            "action_count": len(entities.get("actions", [])),
        }
    }
    
    # Add score and result if provided
    if score is not None:
        output["resume_analysis"]["match_score"] = f"{score}/100"
    
    if result is not None:
        output["resume_analysis"]["classification"] = result
        
    if missing_skills is not None:
        output["resume_analysis"]["missing_skills"] = missing_skills
    
    return json.dumps(output, indent=4)
