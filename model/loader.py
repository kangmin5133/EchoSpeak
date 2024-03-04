import whisper
import torch
from pathlib import Path
# from transformers import AutoProcessor, BarkModel
from model.melo.api import TTS

STT_MODEL_PATH = Path(__file__).parent / "pytorch_model.bin"

def load_and_transform_model(model_name='large-v2'):
    def hf_to_whisper_states(text):
        return (text
            .replace("model.", "")
            .replace("layers", "blocks")
            .replace("fc1", "mlp.0")
            .replace("fc2", "mlp.2")
            .replace("final_layer_norm", "mlp_ln")
            .replace(".self_attn.q_proj", ".attn.query")
            .replace(".self_attn.k_proj", ".attn.key")
            .replace(".self_attn.v_proj", ".attn.value")
            .replace(".self_attn_layer_norm", ".attn_ln")
            .replace(".self_attn.out_proj", ".attn.out")
            .replace(".encoder_attn.q_proj", ".cross_attn.query")
            .replace(".encoder_attn.k_proj", ".cross_attn.key")
            .replace(".encoder_attn.v_proj", ".cross_attn.value")
            .replace(".encoder_attn_layer_norm", ".cross_attn_ln")
            .replace(".encoder_attn.out_proj", ".cross_attn.out")
            .replace("decoder.layer_norm.", "decoder.ln.")
            .replace("encoder.layer_norm.", "encoder.ln_post.")
            .replace("embed_tokens", "token_embedding")
            .replace("encoder.embed_positions.weight", "encoder.positional_embedding")
            .replace("decoder.embed_positions.weight", "decoder.positional_embedding")
            .replace("layer_norm", "ln_post")
        )

    # if torch.backends.mps.is_available():  # Check for MacOS Metal support
    #     device = torch.device('mps')

    if torch.cuda.is_available():  # Check for CUDA support
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    # Load HF Model
    hf_state_dict = torch.load(STT_MODEL_PATH, map_location=device)  # pytorch_model.bin file

    # Rename layers
    for key in list(hf_state_dict.keys()):
        new_key = hf_to_whisper_states(key)
        hf_state_dict[new_key] = hf_state_dict.pop(key)

    # Init Whisper Model and replace model weights
    model = whisper.load_model(model_name)
    model.load_state_dict(hf_state_dict)
    model.to(device)
    return model

class STTLoader:
    def __init__(self):
        self.model = load_and_transform_model()
        

# bark TTS
# class TTSLoader:
#     def __init__(self):
#         self.processor = AutoProcessor.from_pretrained("suno/bark")
#         self.model = BarkModel.from_pretrained("suno/bark")

# melo TTS
class TTSLoader:
    def __init__(self) -> None:
        self.speed = 1.0
        if torch.cuda.is_available():
            self.device = 'cuda:0' 
        else:
            self.device = 'cpu' 
        self.model = TTS(language='KR', device=self.device)
        self.speaker_ids = self.model.hps.data.spk2id
        self.sampling_rate = self.model.hps.data.sampling_rate