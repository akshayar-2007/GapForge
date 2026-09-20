from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from dotenv import load_dotenv
from pydantic import BaseModel
from agent import agent_graph, loop_graph, AgentState

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

sessions: dict[str, AgentState] = {}


@app.post("/api/start")
async def start_pipeline(target_company: str = "default", resume: UploadFile = File(...)):
    """Runs the full graph: Stages 1-6, then pauses at 'wait'."""
    try:
        os.makedirs("./temp_resumes", exist_ok=True)
        temp_path = f"./temp_resumes/{resume.filename}"
        with open(temp_path, "wb") as f:
            f.write(await resume.read())

        initial_state: AgentState = {
            "resume_path": temp_path,
            "manual_profile_data": None,
            "target_company": target_company,
            "user_profile": None,
            "target_benchmark": None,
            "skill_gaps": None,
            "candidate_ideas": None,
            "filtered_ideas": None,
            "shortlist_result": None,
            "user_feedback": None,
            "iteration": 0,
            "selected_idea_index": None,
            "deep_plan": None,
        }

        result_state = agent_graph.invoke(initial_state)

        session_id = str(uuid.uuid4())
        sessions[session_id] = result_state

        return {
            "status": "success",
            "session_id": session_id,
            "user_profile": result_state["user_profile"],
            "skill_gaps": result_state["skill_gaps"][:5],
            "shortlist": result_state["shortlist_result"]["shortlist"],
            "iteration": result_state["iteration"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class ManualProfileInput(BaseModel):
    target_company: str = "default"
    name: str
    technical_skills: list[str]
    soft_skills: list[str] = []
    past_projects: list[dict] = []
    languages: list[str] = []
    years_experience: float = 0.0
    target_roles: list[str] = []


@app.post("/api/start-manual")
async def start_pipeline_manual(payload: ManualProfileInput):
    """Same pipeline as /api/start, but for users without a resume."""
    try:
        initial_state: AgentState = {
            "resume_path": None,
            "manual_profile_data": payload.dict(exclude={"target_company"}),
            "target_company": payload.target_company,
            "user_profile": None,
            "target_benchmark": None,
            "skill_gaps": None,
            "candidate_ideas": None,
            "filtered_ideas": None,
            "shortlist_result": None,
            "user_feedback": None,
            "iteration": 0,
            "selected_idea_index": None,
            "deep_plan": None,
        }

        result_state = agent_graph.invoke(initial_state)
        session_id = str(uuid.uuid4())
        sessions[session_id] = result_state

        return {
            "status": "success",
            "session_id": session_id,
            "user_profile": result_state["user_profile"],
            "skill_gaps": result_state["skill_gaps"][:5],
            "shortlist": result_state["shortlist_result"]["shortlist"],
            "iteration": result_state["iteration"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@app.post("/api/feedback")
async def provide_feedback(session_id: str, feedback: str):
    """Loops back through Stage 4-6 with feedback folded in."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    state = sessions[session_id]
    state["user_feedback"] = feedback
    state["selected_idea_index"] = None

    result_state = loop_graph.invoke(state)
    sessions[session_id] = result_state

    return {
        "status": "success",
        "iteration": result_state["iteration"],
        "shortlist": result_state["shortlist_result"]["shortlist"],
    }


@app.post("/api/select")
async def select_idea(session_id: str, idea_index: int):
    """Runs Stage 7 for the chosen idea."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    state = sessions[session_id]
    shortlist = state["shortlist_result"]["shortlist"]
    if idea_index >= len(shortlist):
        raise HTTPException(status_code=400, detail="Invalid idea index")

    state["selected_idea_index"] = idea_index
    state["user_feedback"] = None

    result_state = loop_graph.invoke(state)
    sessions[session_id] = result_state

    return {
        "status": "success",
        "selected_idea": shortlist[idea_index],
        "deep_plan": result_state["deep_plan"],
    }


@app.get("/api/session/{session_id}")
def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)