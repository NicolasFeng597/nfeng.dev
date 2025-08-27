"""
File for audio project functions.
"""

from fastapi import UploadFile


async def process_audio(file: UploadFile) -> bytes:
    """
    Process audio file and return processed audio as bytes.
    """

    # Read the uploaded file content
    audio_bytes = await file.read()

    # Test processing: return the first half of the audio
    processed_audio = audio_bytes[: len(audio_bytes) // 2]

    print(
        f"Finished process_audio. Original size: {len(audio_bytes)}, Processed size: {len(processed_audio)}"
    )

    return processed_audio
