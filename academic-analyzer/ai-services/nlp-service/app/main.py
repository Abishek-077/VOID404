from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = FastAPI(title="NLP Analysis Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisRequest(BaseModel):
    student_answer: str
    model_answer: str
    max_marks: int

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "nlp"}

@app.post("/analyze")
async def analyze_answer(request: AnalysisRequest) -> Dict[str, Any]:
    try:
        student = request.student_answer.lower()
        model = request.model_answer.lower()
        
        # Semantic similarity
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([student, model])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        
        # Keyword analysis
        model_words = set(re.findall(r'\b\w{4,}\b', model))
        student_words = set(re.findall(r'\b\w{4,}\b', student))
        keyword_coverage = len(model_words & student_words) / len(model_words) if model_words else 0
        
        # Length ratio
        length_ratio = min(len(student.split()) / len(model.split()), 1.0) if model else 0
        
        # Calculate score
        overall_score = (similarity * 0.5 + keyword_coverage * 0.3 + length_ratio * 0.2) * 100
        estimated_marks = (overall_score / 100) * request.max_marks
        
        return {
            "success": True,
            "overall_score": round(overall_score, 2),
            "estimated_marks": round(estimated_marks, 2),
            "semantic_similarity": round(similarity * 100, 2),
            "keyword_coverage": round(keyword_coverage * 100, 2),
            "completeness": round(length_ratio * 100, 2)
        }
    except Exception as e:
        logger.error(f"Analysis Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
