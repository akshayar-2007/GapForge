import google.generativeai as genai
import os
import json
from typing import Dict
from utils.retry import retry_on_rate_limit

@retry_on_rate_limit(max_retries=2, base_delay=60)
def generate_deep_plan(selected_idea: Dict, user_profile: Dict, company: str) -> Dict:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-flash-lite-latest")

    prompt = f"""
You are a senior engineer creating a detailed execution plan for a student's resume project.

PROJECT: {selected_idea.get('title')}
DESCRIPTION: {selected_idea.get('description')}
TARGET GAPS: {', '.join(selected_idea.get('target_gaps', []))}
TECH STACK: {', '.join(selected_idea.get('tech_stack', []))}
TIMELINE: {selected_idea.get('timeline_weeks', 3)} weeks
TARGET COMPANY: {company}

Student's existing skills: {', '.join(user_profile.get('technical_skills', [])[:5])}

Return ONLY valid JSON:
{{
  "roadmap": [
    {{"week": 1, "title": "Foundation & Setup", "tasks": ["Task 1","Task 2"], "deliverable": "..."}}
  ],
  "tech_stack_justification": [
    {{"technology": "Tech name", "why": "1-2 sentence justification tied to {company}"}}
  ],
  "architecture_overview": "2-3 sentences",
  "resume_bullets": ["Bullet 1", "Bullet 2", "Bullet 3"],
  "interview_talking_points": ["Point 1", "Point 2"],
  "potential_challenges": [{{"challenge": "...", "mitigation": "..."}}],
  "stretch_goals": ["Goal 1", "Goal 2"]
}}

Match the roadmap to exactly {selected_idea.get('timeline_weeks', 3)} weeks.
Return ONLY the JSON object, no markdown, no backticks.
"""
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    response_text = response_text.strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing deep plan JSON: {e}")
        print(f"Response: {response_text}")
        return {
            "roadmap": [], "tech_stack_justification": [],
            "architecture_overview": "Error generating plan — please retry.",
            "resume_bullets": [], "interview_talking_points": [],
            "potential_challenges": [], "stretch_goals": [],
            "error": str(e)
        }