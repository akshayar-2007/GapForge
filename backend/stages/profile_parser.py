import json
from pypdf import PdfReader
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import os
from utils.retry import retry_on_rate_limit

from docx import Document as DocxDocument
def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF or DOCX depending on extension."""
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif file_path.lower().endswith(".docx"):
        doc = DocxDocument(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError(f"Unsupported file type: {file_path}. Please upload PDF or DOCX.")
class UserProfile(BaseModel):
    name: str
    technical_skills: list[str]
    soft_skills: list[str]
    past_projects: list[dict]
    languages: list[str]
    years_experience: float
    target_roles: list[str]
    
@retry_on_rate_limit(max_retries=2, base_delay=60)
def parse_profile_from_pdf(pdf_path: str) -> UserProfile:
    """Extract structured profile from resume PDF using Google Gemini."""
    
    # Configure Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-flash-lite-latest")
    
    # Extract text from PDF
    try:
        text = extract_text_from_file(pdf_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        raise
    
    # Call Gemini to parse resume
    prompt = f"""
Extract the following from this resume and return ONLY valid JSON (no markdown, no explanations):

{{
  "name": "Full Name",
  "technical_skills": ["Python", "Java", "React"],
  "soft_skills": ["Leadership", "Communication"],
  "past_projects": [
    {{"name": "Project Name", "description": "Brief description", "technologies": ["Tech1", "Tech2"]}}
  ],
  "languages": ["English", "Tamil"],
  "years_experience": 1.5,
  "target_roles": ["SDE", "Backend Engineer"]
}}

If any field is missing, use empty arrays [] or 0 for numbers.

Resume text:
---
{text}
---

IMPORTANT: Return ONLY the JSON object. No markdown, no backticks, no explanation.
"""
    
    response = model.generate_content(prompt)
    
    # Parse JSON from response
    response_text = response.text.strip()
    
    # Clean up any markdown formatting
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    
    response_text = response_text.strip()
    
    try:
        profile_dict = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response was: {response_text}")
        raise
    
    return UserProfile(**profile_dict)

def parse_profile_from_manual_input(data: dict) -> UserProfile:
    """Fallback: accept manual JSON input if no resume."""
    return UserProfile(**data)