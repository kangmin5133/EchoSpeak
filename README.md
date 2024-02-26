# EcoSpeak🗣️
> STT(✅) + LLM(not yet) + TTS engine for Korean Language

Architechture
![]()


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
download .pkl file from [here]([https://drive.google.com/drive/folders/1iThtzq1aKOaLnbExZe6Zsy8Kv0-l7Dr0](https://huggingface.co/byoussef/whisper-large-v2-Ko/resolve/main/pytorch_model.bin?download=true))
after download, place pytorch_model.bin file to model directory


# Run
```sh
python app.py
```
