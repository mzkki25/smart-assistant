### ==== IMPORTS ==== ###

import os
import glob
import logging
import io

from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from PIL import Image
from sentence_transformers import SentenceTransformer

from utils import (
    load_pdf_text, chunk_text, embed_chunks, 
    retrieve_best_chunk, revise_the_sentence,
    image_capt, extract_tags
)
from prompt import IMAGE_CAPTION, PDF_SUMMARY, PDF_SUMMARY_EXTRACTED



### ==== ALL SETUP INITIALIZATION ==== ###

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionInput(BaseModel):
    question: str

UPLOAD_PATH = "uploads/test_experiment.pdf"



### ==== ALL ROUTES ==== ###

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@app.get("/ai_image_page", response_class=HTMLResponse)
def get_ai_image_page(request: Request):
    if os.path.exists("uploads"):
        for file in glob.glob("uploads/*"):
            os.remove(file)
        logger.info("All files in uploads folder have been deleted.")
    else:
        os.makedirs("uploads")

    return templates.TemplateResponse("ai_image_caption.html", {"request": request})

@app.get("/smart_knowledge_page", response_class=HTMLResponse)
def get_smart_knowledge_page(request: Request):
    if os.path.exists("uploads"):
        for file in glob.glob("uploads/*"):
            os.remove(file)
        logger.info("All files in uploads folder have been deleted.")
    else:
        os.makedirs("uploads")

    return templates.TemplateResponse("smart_knowledge_assistant.html", {"request": request})

@app.post("/upload_pdf")
def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    
    with open(UPLOAD_PATH, "wb") as f:
        f.write(file.file.read())

    logger.info(f"File saved as {UPLOAD_PATH}")

    return JSONResponse(content={
        "filename": file.filename,
        "file_location": UPLOAD_PATH,
    })

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        image.save("uploads/uploaded_image.jpg")
        img_path = "uploads/uploaded_image.jpg"

        logger.info(f"Image saved to: {img_path}")
        
        logger.info("Generating caption...")
        caption = image_capt(img_path)

        indonesia_caption = revise_the_sentence(caption, system=IMAGE_CAPTION)

        logger.info(f"Generated caption: {indonesia_caption}")
        tags = extract_tags(caption, top_n=5)
        
        logger.info(f"Extracted tags: {tags}")
        return JSONResponse(content={
            "caption": indonesia_caption,
            "tags": tags,
            "filename": file.filename
        })
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return JSONResponse(status_code=500, content={"message": "Error processing file."})

@app.post("/ask")
def ask_question(payload: QuestionInput):
    if not os.path.exists(UPLOAD_PATH):
        return JSONResponse(status_code=404, content={"error": "No uploaded PDF found."})
    
    query = payload.question
    raw_text = load_pdf_text(UPLOAD_PATH)

    raw_text = revise_the_sentence(raw_text, system=PDF_SUMMARY_EXTRACTED)
    logger.info(f"Raw text from PDF: {raw_text}")

    chunks = chunk_text(raw_text, max_words=300)
    chunk_embeddings = embed_chunks(chunks, model)
    logger.info(f"Number of chunks: {len(chunks)}")

    best_chunk = retrieve_best_chunk(query, chunks, chunk_embeddings, model)
    logger.info(f"Best chunk retrieved: {best_chunk}")

    response = revise_the_sentence(query, system=PDF_SUMMARY + f"\n\nSpesifik Konteks yang Dihasilkan adalah: {best_chunk}")

    logger.info(f"Response generated: {response}")
    return JSONResponse(content={
        "answer": response
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)