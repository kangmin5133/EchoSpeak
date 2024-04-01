# EchoSpeak🗣️
> STT(✅) + LLM(not yet) + TTS(✅) REST API service for Korean Language
![](img/echospeak_logo.png)

this project used pre trained korean model from byoussef's whisper-large-v2-ko model [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/byoussef/whisper-large-v2-Ko)

## version compatibility
```sh
python 3.10 +
cuda(11.7) or CPU
```

## Docker Installation
```sh
docker pull kmsjks79/echospeak:latest
# if you want mount your result & logs dir
docker run -d -p {your port}:8000 --name {your container name} \
-v /path/to/host/result:/workspace/result \
-v /path/to/host/logs:/workspace/logs \
kmsjks79/echospeak:latest
# or
docker run -d -p {your port}:8000 --name {your container name} kmsjks79/echospeak:latest
```

## Local Installation

It first requires the command-line tool `ffmpeg` to be installed on your system, which is available from most package managers:
```sh
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

### pytorch
```sh
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
```

### requirements
```sh
pip install -r requirements.txt
```

### download model
```sh
cd model/pretrained
(Ubuntu)
sudo apt install git-all
(MacOS)
brew install git-lfs

git clone https://huggingface.co/byoussef/whisper-large-v2-Ko
```


### Run
```sh
python main.py --port [your port]
```
