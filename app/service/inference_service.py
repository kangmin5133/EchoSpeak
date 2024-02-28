from fastapi import HTTPException
from model.loader import model
import json
from pathlib import Path
import uuid
import whisper
import numpy as np
from config.config import Config
from io import BytesIO
import logging

logger = logging.getLogger()

def transcribe_audio_from_bytes(audio_bytes: bytes):
    audio_data = BytesIO(audio_bytes)

    audio_bytes = audio_data.getvalue()  # BytesIO 객체에서 바이트 데이터 추출

    # np.int16 타입으로 변환하기 전에, 바이트 배열의 길이가 2의 배수인지 확인하고, 필요한 경우 패딩 추가
    if len(audio_bytes) % 2 == 1:
        # 길이가 홀수인 경우, 0 바이트를 추가하여 패딩
        audio_bytes += b'\x00'

    waveform = np.frombuffer(audio_bytes, np.int16).astype(np.float32) / 32768.0
    audio = whisper.pad_or_trim(waveform).reshape(1, -1)
    transcription = whisper.transcribe(model, audio)["text"]
    return transcription

def save_result_as_json(unique_id: str, text: str):
    try:
        storage_path = Path(Config.RESULT_STORAGE)
        storage_path.mkdir(parents=True, exist_ok=True)

        filename = storage_path / f"{unique_id}.json"
        data = {"id": unique_id, "text": text}
        with open(filename, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
        return True
    except Exception as e:
        logger.info(f"Failed to save transcription result from {unique_id}: {e}")
        return False

async def process_audio_and_get_result(audio_content: bytes):
    # 고유 ID 생성
    unique_id = str(uuid.uuid4())
    text = transcribe_audio_from_bytes(audio_content)
    save_result = save_result_as_json(unique_id, text)
    if save_result == False :
        raise HTTPException(status_code=500, detail="Failed to save transcription result.")
    return {"id": unique_id, "text": text}