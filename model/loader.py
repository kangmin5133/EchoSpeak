import whisper
import torch
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "pytorch_model.bin"

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

    # Load HF Model
    hf_state_dict = torch.load(MODEL_PATH, map_location=torch.device('cpu'))  # pytorch_model.bin file

    # Rename layers
    for key in list(hf_state_dict.keys()):
        new_key = hf_to_whisper_states(key)
        hf_state_dict[new_key] = hf_state_dict.pop(key)

    # Init Whisper Model and replace model weights
    model = whisper.load_model(model_name)
    model.load_state_dict(hf_state_dict)

    return model

# 이 부분에서 모델을 로드하고 메모리에 올리는 작업을 수행
model = load_and_transform_model()