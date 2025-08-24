"""
FastAPI backend implementation.

Currently only handles audio; TODO: add more functionalities/OOP
"""

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import test

app = FastAPI()

# Add CORS to allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],  # Your Astro frontend
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/test")
async def base_msg():
    return {"message": "Base dir msg"}


@app.post("/test")
async def handle_file(file: UploadFile = None):
    if file is None:
        print("No file received")
        return {"message": "No file provided"}

    content = await file.read()

    return {
        "message": "File received successfully",
        "filename": file.filename,
        "size": len(content),
        "content_type": file.content_type
    }
