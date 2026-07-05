import os
import uuid
import json
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import redis

app = FastAPI(
    title="DarkMatterK3 Community Dispatcher API",
    description="API for distributing DarkMatterK3 simulation tasks to the community.",
    version="1.0.0"
)

# Connect to Redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

# Connect to PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "darkmatter"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            port=os.getenv("DB_PORT", 5432)
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Init DB schema
def init_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(255) PRIMARY KEY,
            username VARCHAR(255),
            score INT DEFAULT 0,
            chunks_processed INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS badges (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) REFERENCES users(user_id),
            badge_name VARCHAR(255),
            awarded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS jobs (
            job_id VARCHAR(255) PRIMARY KEY,
            status VARCHAR(50) DEFAULT 'pending',
            assigned_to VARCHAR(255) REFERENCES users(user_id),
            chunk_data JSONB,
            result_data JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        );
        """)
        conn.commit()
        cursor.close()
        conn.close()

# Pydantic models
class JobRequest(BaseModel):
    user_id: str

class JobResult(BaseModel):
    job_id: str
    user_id: str
    wasserstein_distance: float
    result_metadata: Dict[str, Any]

class UserCreate(BaseModel):
    user_id: str
    username: str

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"status": "Community Dispatcher Online", "docs": "/docs"}

@app.post("/users/register")
def register_user(user: UserCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user.user_id,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return {"message": "User already exists", "user_id": user.user_id}
        
    cursor.execute(
        "INSERT INTO users (user_id, username) VALUES (%s, %s)",
        (user.user_id, user.username)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User registered successfully", "user_id": user.user_id}

@app.post("/jobs/request")
def request_job(req: JobRequest):
    job_id = str(uuid.uuid4())
    chunk_data = {"chunk_id": f"chunk-{job_id[:8]}", "data_url": f"gs://{os.getenv('GCS_BUCKET', 'darkmatter-bucket')}/chunks/{job_id}.h5"}
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (req.user_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="User not found. Register first.")
            
        cursor.execute(
            "INSERT INTO jobs (job_id, status, assigned_to, chunk_data) VALUES (%s, %s, %s, %s)",
            (job_id, "processing", req.user_id, json.dumps(chunk_data))
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    return {"job_id": job_id, "chunk_data": chunk_data}

def award_badges(user_id: str, distance: float, chunks_processed: int, cursor):
    points = 10
    if distance > 30:
        points += 50
        cursor.execute("INSERT INTO badges (user_id, badge_name) VALUES (%s, %s)", (user_id, "Golden Ratio"))
    
    if chunks_processed == 1:
        points += 10
        cursor.execute("INSERT INTO badges (user_id, badge_name) VALUES (%s, %s)", (user_id, "First Blood"))
        
    if chunks_processed == 10:
        points += 100
        cursor.execute("INSERT INTO badges (user_id, badge_name) VALUES (%s, %s)", (user_id, "Plasma Weaver"))
        
    return points

@app.post("/jobs/submit")
def submit_result(result: JobResult):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database unavailable")
        
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM jobs WHERE job_id = %s AND assigned_to = %s", (result.job_id, result.user_id))
    job = cursor.fetchone()
    if not job:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found or not assigned to this user")
        
    if job[0] == "completed":
        cursor.close()
        conn.close()
        return {"message": "Job already completed"}
        
    cursor.execute(
        "UPDATE jobs SET status = 'completed', result_data = %s, completed_at = CURRENT_TIMESTAMP WHERE job_id = %s",
        (json.dumps(result.result_metadata), result.job_id)
    )
    
    cursor.execute("SELECT chunks_processed FROM users WHERE user_id = %s", (result.user_id,))
    user_stats = cursor.fetchone()
    chunks_processed = user_stats[0] + 1 if user_stats else 1
    
    points = award_badges(result.user_id, result.wasserstein_distance, chunks_processed, cursor)
    
    cursor.execute(
        "UPDATE users SET score = score + %s, chunks_processed = %s WHERE user_id = %s",
        (points, chunks_processed, result.user_id)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    try:
        redis_client.zincrby("leaderboard", points, result.user_id)
    except:
        pass
    
    return {"message": "Result accepted", "points_earned": points}

@app.get("/leaderboard")
def get_leaderboard(limit: int = 10):
    try:
        leaders = redis_client.zrevrange("leaderboard", 0, limit - 1, withscores=True)
        return [{"user_id": u, "score": s} for u, s in leaders]
    except:
        return []

@app.get("/badges/{user_id}")
def get_user_badges(user_id: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database unavailable")
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT badge_name, awarded_at FROM badges WHERE user_id = %s ORDER BY awarded_at DESC", (user_id,))
    badges = cursor.fetchall()
    cursor.close()
    conn.close()
    return badges
