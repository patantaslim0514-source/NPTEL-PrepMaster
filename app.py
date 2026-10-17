import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from pdf_processor import PDFProcessor
from ai_generator import AIGenerator
from sample_data import SAMPLE_COURSES

load_dotenv()

app = FastAPI(
    title="NPTEL PrepMaster AI",
    description="Interactive NPTEL Exam Prep & PDF Study Kit Generator",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_generator = AIGenerator()

# Models
class GenerateRequest(BaseModel):
    text: str
    filename: Optional[str] = "lecture.pdf"
    num_mcqs: Optional[int] = 10
    difficulty: Optional[str] = "All Levels"
    focus_mode: Optional[str] = "Comprehensive"
    api_key: Optional[str] = None

class DoubtRequest(BaseModel):
    doubt: str
    context_text: str
    api_key: Optional[str] = None

# API Routes
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "NPTEL PrepMaster AI",
        "has_env_gemini_key": bool(os.getenv("GEMINI_API_KEY"))
    }

@app.get("/api/sample-courses")
async def get_sample_courses():
    courses_summary = []
    for cid, data in SAMPLE_COURSES.items():
        courses_summary.append({
            "id": cid,
            "title": data["title"],
            "instructor": data["instructor"],
            "week": data["week"],
            "overview": data["overview"],
            "total_pages": data["total_pages"],
            "total_words": data["total_words"]
        })
    return {"courses": courses_summary}

@app.get("/api/sample-courses/{course_id}")
async def get_sample_course_detail(course_id: str):
    if course_id not in SAMPLE_COURSES:
        raise HTTPException(status_code=404, detail="Sample course not found")
    data = SAMPLE_COURSES[course_id]
    return {
        "success": True,
        "is_sample": True,
        "data": data
    }

@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="The uploaded PDF file is empty.")
    
    # Max size check (e.g. 25MB)
    if len(contents) > 25 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="PDF file size exceeds 25MB limit.")
        
    result = PDFProcessor.extract_text_from_bytes(contents, filename=file.filename)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to parse PDF"))
        
    return result

@app.post("/api/generate")
async def generate_kit(req: GenerateRequest):
    if not req.text or len(req.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Document text is empty or too short.")
        
    study_kit = ai_generator.generate_study_kit(
        pdf_text=req.text,
        filename=req.filename or "lecture.pdf",
        num_mcqs=req.num_mcqs or 10,
        difficulty=req.difficulty or "All Levels",
        focus_mode=req.focus_mode or "Comprehensive",
        custom_api_key=req.api_key
    )
    
    return {
        "success": True,
        "data": study_kit
    }

@app.post("/api/chat-doubt")
async def chat_doubt(req: DoubtRequest):
    if not req.doubt or len(req.doubt.strip()) == 0:
        raise HTTPException(status_code=400, detail="Doubt question cannot be empty.")
        
    answer = ai_generator.answer_doubt(
        doubt=req.doubt,
        context_text=req.context_text,
        custom_api_key=req.api_key
    )
    
    return {
        "success": True,
        "answer": answer
    }

# Mount static folder
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "NPTEL PrepMaster AI backend is running. static/index.html not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
