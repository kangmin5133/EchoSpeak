# import whisper
import torch
from pathlib import Path
from model.melo.api import TTS
from transformers import pipeline

STT_MODEL_PATH = Path(__file__).parent / "pretrained/whisper-large-v2-Ko/"

def load_and_transform_model(device="cuda:0", dtype="float32", batch_size=8, chunk_length=30):
    pipe = pipeline("automatic-speech-recognition",
                    model=STT_MODEL_PATH,
                    device=device,
                    torch_dtype=torch.float16 if dtype == "float16" else torch.float32)
    return pipe


class STTLoader:
    def __init__(self):
        self.model = load_and_transform_model()
        
# melo TTS
class TTSLoader:
    def __init__(self) -> None:
        self.speed = 1.0
        if torch.cuda.is_available():
            self.device = 'cuda:1' 
        else:
            self.device = 'cpu' 
        self.model = TTS(language='KR', device=self.device)
        self.speaker_ids = self.model.hps.data.spk2id
        self.sampling_rate = self.model.hps.data.sampling_rate