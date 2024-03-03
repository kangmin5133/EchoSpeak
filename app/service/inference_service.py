from fastapi import HTTPException
from model.loader import model
import json
import glob
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
        logger.info(f"STT result saved \nfile_name : {unique_id}.json \nid : {unique_id}\ntext : {text}")
        return True
    except Exception as e:
        logger.error(f"Failed to save transcription result from {unique_id}: {e}")
        return False

async def process_audio_and_get_result(audio_content: bytes):
    # 고유 ID 생성
    unique_id = str(uuid.uuid4())
    text = transcribe_audio_from_bytes(audio_content)
    save_result = save_result_as_json(unique_id, text)
    if save_result == False :
        raise HTTPException(status_code=500, detail="Failed to save transcription result.")
    return {"id": unique_id, "text": text}

async def get_request_ids():
    result_dir = Path(Config.RESULT_STORAGE)
    # 해당 디렉토리에 있는 모든 파일의 경로 조회
    files = glob.glob(f"{result_dir}/*.json")
    # 파일 경로에서 파일 이름만 추출
    file_names = [str(Path(file).name).split(".")[0] for file in files]
    return {"ids":file_names}

async def get_result_json(id:str):
    result_dir = Path(Config.RESULT_STORAGE)
    # 해당 디렉토리에 있는 모든 파일의 경로 조회
    files = glob.glob(f"{result_dir}/*.json")
    # 파일 경로에서 파일 이름만 추출
    file_names = [str(Path(file).name).split(".")[0] for file in files]
    if id in file_names:
        with open(str(result_dir)+"/"+id+".json", 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        raise HTTPException(status_code=404, detail=f"result from id ({id}) not found")

    return data