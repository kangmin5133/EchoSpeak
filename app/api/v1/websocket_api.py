from fastapi import WebSocket, WebSocketDisconnect
from model.loader import model  # 모델 로드
import whisper
import traceback
import base64
import numpy as np
from app.utils.audio_process import process_wav_bytes

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"messege arrived length {len(data)}, type {type(data)}")

            data_bytes = base64.b64decode(data) 
            # audio = await process_wav_bytes(bytes(data_bytes))
            waveform = np.frombuffer(data_bytes, np.int16).astype(np.float32) / 32768.0
            audio = whisper.pad_or_trim(waveform).reshape(1, -1)
            transcription = whisper.transcribe(model, audio)
            print("transcription : ",transcription)
            await websocket.send_text(transcription["text"])
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    except Exception as e:
        traceback.print_exc()