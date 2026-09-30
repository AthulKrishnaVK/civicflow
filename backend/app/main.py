

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.graph.workflow import civicflow_graph
from app.rag.evidence import find_evidence


app = FastAPI(
    title="CivicFlow API",
    description="AI Government Process Navigator",
    version="0.1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class GoalRequest(BaseModel):

    goal: str


class WhyRequest(BaseModel):

    claim: str


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "CivicFlow API is running"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# ANALYZE
# ============================================================

@app.post("/analyze")
def analyze(
    request: GoalRequest
):

    initial_state = {

        "user_input": request.goal,

        "intent": {},

        "sources": [],

        "eligibility": {},

        "research": [],

        "documents": {},

        "regulations": {},

        "procedure": {},

        "verification": {}
    }

    result = civicflow_graph.invoke(
        initial_state
    )

    return {

        "input": request.goal,

        "intent": result.get(
            "intent",
            {}
        ),

        "sources": result.get(
            "sources",
            []
        ),

        "research": result.get(
            "research",
            []
        ),

        "eligibility": result.get(
            "eligibility",
            {}
        ),

        "documents": result.get(
            "documents",
            {}
        ),

        "regulations": result.get(
            "regulations",
            {}
        ),

        "procedure": result.get(
            "procedure",
            {}
        ),

        "verification": result.get(
            "verification",
            {}
        )
    }


# ============================================================
# EVIDENCE SEARCH
# ============================================================

@app.post("/evidence")
def evidence(
    query: str
):

    results = find_evidence(
        query,
        limit=5
    )

    return {

        "query": query,

        "evidence": results
    }


# ============================================================
# WHY
# ============================================================

@app.post("/why")
def why(
    request: WhyRequest
):

    evidence = find_evidence(
        request.claim,
        limit=5
    )

    return {

        "claim": request.claim,

        "evidence": evidence
    }