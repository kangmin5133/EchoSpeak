from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict
from fastapi.responses import StreamingResponse
from app.service import stt_inference_service, tts_inference_service
from config.config import Version
import logging

router = APIRouter()
logger = logging.getLogger()

@router.get("/inference/stt/version")
async def get_version():
    return {"api_version":Version.echospeak_version}

@router.get("/inference/stt/search")
async def get_request_ids():
    
    result = await stt_inference_service.get_request_ids()
    return result

@router.get("/inference/stt/result")
async def get_result_by_id(id:str):
    
    result = await stt_inference_service.get_result_json(id=id)
    return result


@router.post("/inference/stt/transcribe", response_model=Dict[str, str])
async def transcribe_audio(file: UploadFile = File(...)):

    logger.info(f"requested file name : {file.filename}")

    if file is None:
        raise HTTPException(status_code=400, detail="file is missing")
    
    audio_content = await file.read()
    result = await stt_inference_service.process_audio_and_get_result(audio_content)
    return result

@router.post("/inference/tts/generates")
async def generates_audio(text : str):

    logger.info(f"requested TTS text : {text}")

    if text is None:
        raise HTTPException(status_code=400, detail="text is missing")

    audio_buffer = await tts_inference_service.process_text_to_audio(text)
    return StreamingResponse(audio_buffer, media_type="audio/wav")