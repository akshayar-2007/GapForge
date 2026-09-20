from typing import List, Dict

def rank_ideas(filtered_ideas: List[Dict], skill_gaps: List[Dict]) -> List[Dict]:
    """Rank ideas by how well they close skill gaps + uniqueness."""
    gap_importance = {gap["area"]: gap["weight"] for gap in skill_gaps}

    for idea in filtered_ideas:
        if not idea.get("keep", True):
            continue
        target_gaps = idea.get("target_gaps", [])
        gap_score = sum(gap_importance.get(gap, 0) for gap in target_gaps)
        idea["rank_score"] = (gap_score * 0.6) + (idea.get("confidence", 0.5) * 0.4)

    ranked = sorted(
        [i for i in filtered_ideas if i.get("keep")],
        key=lambda x: x.get("rank_score", 0),
        reverse=True
    )
    for i, idea in enumerate(ranked):
        idea["rank"] = i + 1
    return ranked


def create_shortlist(ideas: List[Dict], top_n: int = 5) -> Dict:
    kept = [i for i in ideas if i.get("keep")]
    rejected = [i for i in ideas if not i.get("keep")]
    return {
        "shortlist": kept[:top_n],
        "rejected_count": len(rejected),
        "rejection_reasons": [
            {"title": r.get("title"), "reason": r.get("rejection_reason")}
            for r in rejected
        ]
    }