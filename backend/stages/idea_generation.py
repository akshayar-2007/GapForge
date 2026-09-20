import google.generativeai as genai
import os
import json
from typing import List, Dict
from utils.retry import retry_on_rate_limit
@retry_on_rate_limit(max_retries=2, base_delay=60)
def generate_ideas(skill_gaps: List[Dict], user_profile: Dict, company: str) -> List[Dict]:
    """
    Generate 5-7 project ideas that specifically target the identified skill gaps.
    Each idea focuses on closing 1-2 major gaps.
    """
    
    # Configure Gemini
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-flash-lite-latest")
    
    # Format gaps for the prompt
    top_gaps = skill_gaps[:3]  # Focus on top 3 gaps
    gap_text = "\n".join([
        f"- {gap['area']}: {', '.join(gap['missing_keywords'][:3])}"
        for gap in top_gaps
    ])
    
    prompt = f"""
You are a senior engineer who helps developers build resume-worthy projects.

A developer preparing for interviews at {company} has these skill gaps:
{gap_text}

Their existing skills: {', '.join(user_profile.get('technical_skills', [])[:5])}

Generate 5-7 PROJECT IDEAS that directly address these gaps. Each idea should:
1. Target 1-2 specific skill gaps
2. Be completable in 2-4 weeks
3. Result in a unique, portfolio-differentiating project
4. NOT be generic ("Build a to-do app")

For each idea, return JSON with:
{{
  "id": 1,
  "title": "Project name",
  "description": "2-3 sentences explaining what it does",
  "target_gaps": ["Gap area 1", "Gap area 2"],
  "tech_stack": ["Technology1", "Technology2"],
  "complexity": "medium",
  "timeline_weeks": 3,
  "why_unique": "Why this stands out from typical projects"
}}

Return ONLY a JSON array of 5-7 ideas. No markdown, no explanation.
"""
    
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    
    # Clean markdown if present
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    
    response_text = response_text.strip()
    
    try:
        ideas = json.loads(response_text)
        return ideas
    except json.JSONDecodeError as e:
        print(f"Error parsing ideas JSON: {e}")
        print(f"Response: {response_text}")
        return []