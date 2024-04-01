from fastapi import HTTPException
from model.loader import STTLoader
import json
import glob
from pathlib import Path
import uuid
import numpy as np
from config.config import Config
from io import BytesIO
import logging
import tempfile
import os

logger = logging.getLogger()
STT_MODEL = STTLoader()
def transcribe_audio_from_bytes(audio_file_path: str):
    transcription = STT_MODEL.model(audio_file_path, chunk_length_s=30, batch_size=8)
    return transcription["text"]

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

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio_content)
        temp_file_path = temp_file.name
    try:
        text = transcribe_audio_from_bytes(temp_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(temp_file_path)

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