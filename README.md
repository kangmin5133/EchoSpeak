# EcoSpeak🗣️
> STT(✅) + LLM(not yet) + TTS engine for Korean Language


## Architechture
![]()

this project used pre trained korean model from byoussef's whisper-large-v2-ko model [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/byoussef/whisper-large-v2-Ko)


## version compatibility
```sh
python 3.10 +
cuda(11.7) or CPU 
```

## pytorch installation
### pytorch
```sh
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
```

## requirements
```sh
openai-whisper==20231117
transformers==4.35.2
huggingface-hub==0.20.3
huggingface==0.0.1
uvicorn==0.27.1
fastapi==0.109.2
```

## download models
```sh
clone git@github.com:kangmin5133/EcoSpeak.git
cd model
```
download pytorch_model.bin file from [here](https://huggingface.co/byoussef/whisper-large-v2-Ko/resolve/main/pytorch_model.bin?download=true)
after download, place pytorch_model.bin file to model directory


# Run
```sh
python app.py
```
