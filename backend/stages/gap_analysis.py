from typing import List, Dict
from stages.profile_parser import UserProfile
from stages.target_research import get_company_benchmark

def analyze_gaps(profile: UserProfile, company: str) -> List[Dict]:
    """Compare user skills against company benchmark."""
    benchmark = get_company_benchmark(company)
    
    user_skills_lower = [s.lower() for s in profile.technical_skills]
    gaps = []
    
    for depth_area in benchmark["depth_areas"]:
        area_name = depth_area["area"]
        keywords = depth_area.get("keywords", [])
        keywords_lower = [k.lower() for k in keywords]
        
        # Count keyword matches in user's skills
        matched_keywords = [
            k for k in keywords_lower 
            if any(k in s for s in user_skills_lower)
        ]
        coverage = len(matched_keywords) / len(keywords_lower) if keywords_lower else 0.0
        
        gap_obj = {
            "area": area_name,
            "weight": depth_area["weight"],
            "coverage": coverage,
            "missing_keywords": [k for k in keywords_lower if k not in matched_keywords],
            "confidence": 1 - coverage
        }
        
        gaps.append(gap_obj)
    
    return sorted(gaps, key=lambda x: x["weight"] * x["confidence"], reverse=True)