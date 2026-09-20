from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph, END

from stages.profile_parser import parse_profile_from_pdf, UserProfile
from stages.target_research import get_company_benchmark
from stages.gap_analysis import analyze_gaps
from stages.idea_generation import generate_ideas
from stages.filtering import filter_ideas
from stages.shortlist import rank_ideas, create_shortlist
from stages.deep_plan import generate_deep_plan


class AgentState(TypedDict):
    resume_path: Optional[str]
    manual_profile_data: Optional[Dict]
    target_company: str
    user_profile: Optional[Dict]
    target_benchmark: Optional[Dict]
    skill_gaps: Optional[List[Dict]]
    candidate_ideas: Optional[List[Dict]]
    filtered_ideas: Optional[List[Dict]]
    shortlist_result: Optional[Dict]
    user_feedback: Optional[str]
    iteration: int
    selected_idea_index: Optional[int]
    deep_plan: Optional[Dict]


# ---------- Nodes ----------

def node_parse_profile(state: AgentState) -> AgentState:
    if state.get("resume_path"):
        profile = parse_profile_from_pdf(state["resume_path"])
    else:
        from stages.profile_parser import parse_profile_from_manual_input
        profile = parse_profile_from_manual_input(state["manual_profile_data"])
    state["user_profile"] = profile.dict()
    return state

def node_target_research(state: AgentState) -> AgentState:
    state["target_benchmark"] = get_company_benchmark(state["target_company"])
    return state

def node_gap_analysis(state: AgentState) -> AgentState:
    profile_obj = UserProfile(**state["user_profile"])
    state["skill_gaps"] = analyze_gaps(profile_obj, state["target_company"])
    return state

def node_idea_generation(state: AgentState) -> AgentState:
    feedback = state.get("user_feedback")
    gaps = state["skill_gaps"]
    if feedback:
        gaps = gaps + [{"area": f"USER FEEDBACK: {feedback}", "weight": 0.5,
                         "missing_keywords": [], "coverage": 0, "confidence": 1.0}]
    ideas = generate_ideas(gaps, state["user_profile"], state["target_company"])
    state["candidate_ideas"] = ideas
    state["iteration"] = state.get("iteration", 0) + 1
    state["user_feedback"] = None  # consumed
    return state

def node_filtering(state: AgentState) -> AgentState:
    existing = [p.get("name", "") for p in state["user_profile"].get("past_projects", [])]
    state["filtered_ideas"] = filter_ideas(state["candidate_ideas"], existing)
    return state

def node_shortlist(state: AgentState) -> AgentState:
    ranked = rank_ideas(state["filtered_ideas"], state["skill_gaps"])
    state["shortlist_result"] = create_shortlist(ranked, top_n=5)
    return state

def node_deep_plan(state: AgentState) -> AgentState:
    shortlist = state["shortlist_result"]["shortlist"]
    idx = state.get("selected_idea_index", 0)
    selected = shortlist[idx]
    state["deep_plan"] = generate_deep_plan(selected, state["user_profile"], state["target_company"])
    return state


def route_after_shortlist(state: AgentState) -> str:
    if state.get("user_feedback"):
        return "loop_back"
    if state.get("selected_idea_index") is not None:
        return "finalize"
    return "wait"


# ---------- Graph 1: full pipeline, used by /api/start ----------

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("parse_profile", node_parse_profile)
    graph.add_node("target_research", node_target_research)
    graph.add_node("gap_analysis", node_gap_analysis)
    graph.add_node("idea_generation", node_idea_generation)
    graph.add_node("filtering", node_filtering)
    graph.add_node("shortlist", node_shortlist)
    graph.add_node("deep_plan", node_deep_plan)

    graph.set_entry_point("parse_profile")
    graph.add_edge("parse_profile", "target_research")
    graph.add_edge("target_research", "gap_analysis")
    graph.add_edge("gap_analysis", "idea_generation")
    graph.add_edge("idea_generation", "filtering")
    graph.add_edge("filtering", "shortlist")
    graph.add_conditional_edges(
        "shortlist", route_after_shortlist,
        {"loop_back": "idea_generation", "finalize": "deep_plan", "wait": END}
    )
    graph.add_edge("deep_plan", END)
    return graph.compile()


# ---------- Graph 2: loop-only, used by /api/feedback and /api/select ----------

def build_loop_subgraph():
    graph = StateGraph(AgentState)
    graph.add_node("idea_generation", node_idea_generation)
    graph.add_node("filtering", node_filtering)
    graph.add_node("shortlist", node_shortlist)
    graph.add_node("deep_plan", node_deep_plan)

    graph.set_entry_point("idea_generation")
    graph.add_edge("idea_generation", "filtering")
    graph.add_edge("filtering", "shortlist")
    graph.add_conditional_edges(
        "shortlist", route_after_shortlist,
        {"loop_back": "idea_generation", "finalize": "deep_plan", "wait": END}
    )
    graph.add_edge("deep_plan", END)
    return graph.compile()


agent_graph = build_graph()
loop_graph = build_loop_subgraph()