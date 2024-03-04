FROM python:3.11

RUN apt-get update && \
    apt-get install -y gcc libffi-dev musl-dev && \
    apt-get install -y ffmpeg && \
    apt-get install -y build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

WORKDIR /workspace

COPY . /workspace

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/workspace/model"
RUN python model/melo/init_downloads.py

CMD ["python", "main.py"]
# CMD ["bash"]
