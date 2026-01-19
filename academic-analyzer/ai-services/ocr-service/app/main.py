from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from pdf2image import convert_from_bytes
import cv2
import numpy as np
from typing import Dict
import logging

app = FastAPI(title="OCR Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ocr"}

@app.post("/extract")
async def extract_text(file: UploadFile = File(...)) -> Dict:
    try:
        contents = await file.read()
        
        if file.content_type == "application/pdf":
            images = convert_from_bytes(contents, dpi=300)
            text_parts = []
            
            for img in images:
                img_array = np.array(img)
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                text = pytesseract.image_to_string(gray)
                text_parts.append(text)
            
            full_text = "\n\n".join(text_parts)
        else:
            img_array = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            full_text = pytesseract.image_to_string(gray)
        
        return {
            "success": True,
            "text": full_text,
            "pages": len(images) if file.content_type == "application/pdf" else 1
        }
    except Exception as e:
        logger.error(f"OCR Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
