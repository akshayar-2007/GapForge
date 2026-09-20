import requests
import os
from typing import List, Dict

def check_github_saturation(project_title: str) -> Dict:
    """
    Check how many repos exist with similar keywords.
    Higher count = more saturated = less differentiated.
    """
    
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {github_token}"}
    
    # Search GitHub for similar repos
    query = f"{project_title} in:name language:python"
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=1"
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        
        total_count = data.get("total_count", 0)
        
        # Saturation levels
        if total_count < 50:
            saturation = "low"
            confidence = 0.9
        elif total_count < 200:
            saturation = "medium"
            confidence = 0.6
        else:
            saturation = "high"
            confidence = 0.3
        
        return {
            "saturation": saturation,
            "similar_repos": total_count,
            "confidence": confidence  # How unique/differentiated is this idea
        }
    
    except Exception as e:
        print(f"GitHub API error: {e}")
        # Default to medium saturation if API fails
        return {"saturation": "medium", "similar_repos": 0, "confidence": 0.5}

def filter_ideas(ideas: List[Dict], user_existing_projects: List[str]) -> List[Dict]:
    """
    Filter ideas by:
    1. GitHub saturation (reject oversaturated)
    2. Dedup against user's existing projects
    3. Score feasibility
    """
    
    filtered = []
    
    for idea in ideas:
        title = idea.get("title", "")
        
        # Check for overlap with user's existing projects
        is_duplicate = any(
            title.lower() in proj.lower() or proj.lower() in title.lower()
            for proj in user_existing_projects
        )
        
        if is_duplicate:
            idea["rejection_reason"] = "Too similar to your existing projects"
            idea["keep"] = False
            continue
        
        # Check GitHub saturation
        saturation_data = check_github_saturation(title)
        idea["saturation"] = saturation_data["saturation"]
        idea["similar_repos"] = saturation_data["similar_repos"]
        idea["confidence"] = saturation_data["confidence"]
        
        # Reject highly saturated ideas
        if saturation_data["saturation"] == "high":
            idea["rejection_reason"] = f"Too saturated ({saturation_data['similar_repos']} similar repos)"
            idea["keep"] = False
            continue
        
        idea["keep"] = True
        filtered.append(idea)
    
    return filtered