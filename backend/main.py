"""
FastAPI backend implementation.

Currently only handles audio; TODO: add more functionalities/OOP
"""

from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from audio import input_audio

app = FastAPI()

# Add CORS to allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],  # Your Astro frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/projects/audio")
async def handle_file(file: UploadFile = File(...)):
    return Response(content=await input_audio(file), media_type="audio/wav")

@app.websocket("/projects/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected")
    try:
        while True:
            data = await websocket.receive_bytes()
            processed_data = input_audio(data)
    except WebSocketDisconnect as e:
        print(f"WebSocket disconnected: code={e.code}, reason={e.reason}")
    except Exception as e:
        print(f"WebSocket exception: {e}")
    finally:
        print("WebSocket closed")