from fastapi import HTTPException
from scipy.io import wavfile
from model.loader import TTSLoader
import numpy as np
from config.config import Config
from io import BytesIO
import logging

logger = logging.getLogger()
TTS_MODEL = TTSLoader()
# async def process_text_to_audio(text : str):
#     inputs = TTS_MODEL.processor(text)
#     audio_array = TTS_MODEL.model.generate(**inputs)
#     audio_array = audio_array.cpu().numpy().squeeze()
#     sample_rate = TTS_MODEL.model.generation_config.sample_rate

#     audio_buffer = BytesIO()
#     wavfile.write(audio_buffer, rate=sample_rate, data=audio_array)
#     audio_buffer.seek(0)
#     return audio_buffer
async def process_text_to_audio(text : str):
    audio = TTS_MODEL.model.tts_to_file(text, TTS_MODEL.speaker_ids['KR'], output_path=None, speed=TTS_MODEL.speed)
    audio_buffer = BytesIO()
    wavfile.write(audio_buffer, rate=TTS_MODEL.sampling_rate, data=audio)
    audio_buffer.seek(0)
    return audio_buffer
