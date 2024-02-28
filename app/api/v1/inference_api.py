from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict
from app.service import inference_service
from config.config import Version
import logging

router = APIRouter()
logger = logging.getLogger()

@router.get("/inference/stt/version")
async def get_version():
    return {"api_version":Version.echospeak_version,"whisper":Version.whisper_version}

@router.get("/inference/stt/search")
async def get_request_ids():
    
    result = await inference_service.get_request_ids()
    return result


@router.post("/inference/stt/transcribe", response_model=Dict[str, str])
async def transcribe_audio(file: UploadFile = File(...)):

    logger.info(f"requested file name : {file.filename}")

    if file is None:
        raise HTTPException(status_code=400, detail="file is missing")
    
    audio_content = await file.read()
    result = await inference_service.process_audio_and_get_result(audio_content)
    return result