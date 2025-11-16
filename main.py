import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Course, Lead

app = FastAPI(title="Kazify.ai API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Kazify.ai Backend is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from Kazify.ai backend!"}

# Public: list featured courses
@app.get("/api/courses")
def list_courses(category: Optional[str] = None, featured: Optional[bool] = None, limit: int = 12):
    if db is None:
        return {"courses": []}
    filter_q = {}
    if category:
        filter_q["category"] = category
    if featured is not None:
        filter_q["featured"] = featured
    items = get_documents("course", filter_q, limit)
    # Convert ObjectId to str
    for it in items:
        if isinstance(it.get("_id"), ObjectId):
            it["id"] = str(it.pop("_id"))
    return {"courses": items}

class LeadIn(Lead):
    pass

@app.post("/api/leads")
def create_lead(lead: LeadIn):
    if db is None:
        # In case DB not configured, don't fail the site
        return {"status": "queued", "message": "Database not configured"}
    inserted_id = create_document("lead", lead)
    return {"status": "ok", "id": inserted_id}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
