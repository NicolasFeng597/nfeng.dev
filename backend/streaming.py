"""
FastAPI backend for handling continuous audio streaming
"""

from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import time
from typing import List
import numpy as np

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active WebSocket connections
active_connections: List[WebSocket] = []


@app.post("/audio/stream")
async def handle_audio_stream(
    audio_chunk: UploadFile = File(...), timestamp: str = None
):
    """Handle continuous audio chunks"""

    # Read the audio chunk
    chunk_data = await audio_chunk.read()

    # Process the audio chunk
    # This is where you'd add your audio processing logic
    result = await process_audio_chunk(chunk_data, timestamp)

    print(f"Processed chunk: {len(chunk_data)} bytes at {timestamp}")

    return {
        "status": "success",
        "chunk_size": len(chunk_data),
        "timestamp": timestamp,
        "processing_result": result,
    }


@app.post("/audio/raw")
async def handle_raw_audio(request_data: dict):
    """Handle raw audio data arrays"""

    audio_data = request_data.get("audio_data", [])
    sample_rate = request_data.get("sample_rate", 44100)
    timestamp = request_data.get("timestamp")

    # Convert to numpy array for processing
    audio_array = np.array(audio_data, dtype=np.float32)

    # Process raw audio data
    result = await process_raw_audio(audio_array, sample_rate)

    print(f"Processed raw audio: {len(audio_array)} samples at {sample_rate}Hz")

    return {
        "status": "success",
        "samples_processed": len(audio_array),
        "sample_rate": sample_rate,
        "timestamp": timestamp,
        "analysis": result,
    }


@app.websocket("/audio/ws")
async def websocket_audio_stream(websocket: WebSocket):
    """WebSocket endpoint for real-time audio streaming"""

    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            # Receive audio data
            data = await websocket.receive_bytes()

            # Process the audio data
            result = await process_websocket_audio(data)

            # Send response back
            response = {
                "status": "processed",
                "data_size": len(data),
                "timestamp": time.time(),
                "result": result,
            }

            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("WebSocket client disconnected")


async def process_audio_chunk(chunk_data: bytes, timestamp: str):
    """Process audio chunk - implement your audio analysis here"""

    # Example: Simple analysis
    chunk_size = len(chunk_data)

    # You could add:
    # - Audio format detection
    # - Frequency analysis
    # - Speech recognition
    # - Noise detection
    # - etc.

    return {
        "chunk_processed": True,
        "size": chunk_size,
        "analysis": "Basic processing completed",
    }


async def process_raw_audio(audio_array: np.ndarray, sample_rate: int):
    """Process raw audio array"""

    # Example audio analysis
    rms = np.sqrt(np.mean(audio_array**2))  # Root Mean Square (volume)
    peak = np.max(np.abs(audio_array))  # Peak amplitude

    # Simple frequency analysis
    fft = np.fft.fft(audio_array)
    frequencies = np.fft.fftfreq(len(audio_array), 1 / sample_rate)
    dominant_freq = frequencies[np.argmax(np.abs(fft[: len(fft) // 2]))]

    return {
        "rms_level": float(rms),
        "peak_amplitude": float(peak),
        "dominant_frequency": float(dominant_freq),
        "sample_count": len(audio_array),
    }


async def process_websocket_audio(data: bytes):
    """Process WebSocket audio data"""

    # Basic processing
    data_size = len(data)

    # Add your real-time processing here

    return {"processed": True, "size": data_size, "type": "websocket_audio"}


@app.get("/audio/status")
async def get_streaming_status():
    """Get current streaming status"""

    return {
        "active_websocket_connections": len(active_connections),
        "server_time": time.time(),
        "status": "running",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
