"""
Internal MCP Server for Harsh Agarwal's Personal Website
Provides tools for querying personal data, resume info, and opinions
"""
import json
import sqlite3
import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Harsh's Personal MCP Server",
    description="MCP tools for personal website chat agent",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        os.getenv("FRONTEND_URL", "")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "resume.db")

# Load JSON data
def load_json(filename: str) -> dict:
    with open(os.path.join(DATA_DIR, filename), 'r') as f:
        return json.load(f)

# Database helper
def query_db(sql: str, params: tuple = ()) -> list:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, params)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

# ============ MCP Tools ============

class StatusResponse(BaseModel):
    location: dict
    current_activity: str
    current_company: str
    upcoming_trips: list
    timezone: str

@app.get("/mcp/get_personal_status", response_model=StatusResponse)
async def get_personal_status():
    """
    MCP Tool: get_personal_status
    Returns current location, activity, and travel plans
    """
    travel_data = load_json("travel_plans.json")
    return StatusResponse(
        location=travel_data["current_location"],
        current_activity=travel_data["current_activity"],
        current_company=travel_data["current_company"],
        upcoming_trips=travel_data["upcoming_trips"],
        timezone=travel_data["current_location"]["timezone"]
    )


class FootballQuery(BaseModel):
    query: str

class FootballResponse(BaseModel):
    topic: str
    opinion: str
    confidence: str
    related_topics: list

@app.post("/mcp/consult_football_brain", response_model=FootballResponse)
async def consult_football_brain(request: FootballQuery):
    """
    MCP Tool: consult_football_brain
    Returns Harsh's opinions on football topics
    """
    football_data = load_json("football_opinions.json")
    query_lower = request.query.lower()

    # Match query to opinions
    opinions = football_data["opinions"]
    matched_topic = None
    matched_opinion = None

    # Priority keywords mapping
    keywords = {
        "messi": ["messi", "leo", "goat", "greatest"],
        "ronaldo": ["ronaldo", "cr7", "cristiano"],
        "barcelona": ["barcelona", "barca", "fcb", "blaugrana"],
        "real madrid": ["real madrid", "madrid", "los blancos"],
        "el clasico": ["clasico", "el clasico", "rivalry"],
        "lamine yamal": ["lamine", "yamal"],
        "pedri": ["pedri"],
        "premier league": ["premier league", "epl", "english"],
        "world cup 2022": ["world cup", "qatar", "argentina"],
        "champions league": ["champions league", "ucl"],
        "best match": ["best match", "remontada", "6-1", "psg"]
    }

    for topic, kws in keywords.items():
        if any(kw in query_lower for kw in kws):
            matched_topic = topic
            matched_opinion = opinions.get(topic, opinions["current take"])
            break

    if not matched_topic:
        matched_topic = "general"
        matched_opinion = opinions.get("current take", "Barcelona is the best team in the world!")

    # Find related topics
    related = [t for t in opinions.keys() if t != matched_topic][:3]

    return FootballResponse(
        topic=matched_topic.replace("_", " ").title(),
        opinion=matched_opinion,
        confidence="High" if matched_topic in opinions else "Medium",
        related_topics=related
    )


class SQLQuery(BaseModel):
    query: str

class SQLResponse(BaseModel):
    results: list
    row_count: int
    query_executed: str

@app.post("/mcp/query_resume_sql", response_model=SQLResponse)
async def query_resume_sql(request: SQLQuery):
    """
    MCP Tool: query_resume_sql
    Executes SQL queries against the resume database
    Only SELECT queries are allowed for security
    """
    query = request.query.strip()

    # Security: Only allow SELECT queries
    if not query.upper().startswith("SELECT"):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")

    # Block dangerous keywords
    dangerous = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE", "--", ";"]
    if any(d in query.upper() for d in dangerous):
        raise HTTPException(status_code=400, detail="Query contains forbidden keywords")

    try:
        results = query_db(query)
        return SQLResponse(
            results=results,
            row_count=len(results),
            query_executed=query
        )
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"SQL Error: {str(e)}")


# ============ Convenience Endpoints ============

@app.get("/mcp/skills")
async def get_skills(category: Optional[str] = None):
    """Get all skills, optionally filtered by category"""
    if category:
        return query_db("SELECT * FROM skills WHERE category = ?", (category,))
    return query_db("SELECT * FROM skills ORDER BY proficiency DESC")

@app.get("/mcp/experience")
async def get_experience():
    """Get all work experience with projects"""
    experiences = query_db("""
        SELECT * FROM work_experience ORDER BY
        CASE WHEN is_current = 1 THEN 0 ELSE 1 END,
        end_date DESC
    """)

    for exp in experiences:
        projects = query_db(
            "SELECT * FROM projects WHERE work_experience_id = ?",
            (exp["id"],)
        )
        exp["projects"] = projects

    return experiences

@app.get("/mcp/education")
async def get_education():
    """Get education details"""
    education = query_db("SELECT * FROM education")
    courses = query_db("SELECT * FROM courses")
    return {"education": education, "courses": courses}

@app.get("/mcp/achievements")
async def get_achievements():
    """Get all achievements"""
    return query_db("SELECT * FROM achievements ORDER BY year DESC")

@app.get("/mcp/personal_info")
async def get_personal_info():
    """Get personal info"""
    return query_db("SELECT * FROM personal_info")[0]

@app.get("/mcp/football_hot_takes")
async def get_football_hot_takes():
    """Get Harsh's football hot takes"""
    data = load_json("football_opinions.json")
    return {
        "favorite_team": data["favorite_team"],
        "goat": data["goat"],
        "hot_takes": data["hot_takes"]
    }


# ============ Health Check ============

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "harsh-mcp-server"}

@app.get("/")
async def root():
    return {
        "name": "Harsh's Personal MCP Server",
        "version": "1.0.0",
        "tools": [
            "get_personal_status",
            "consult_football_brain",
            "query_resume_sql"
        ],
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
