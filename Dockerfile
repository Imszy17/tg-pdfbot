FROM python:3.9.0

COPY . /worker
WORKDIR /worker

RUN apt update -qqy \
    && apt install --no-install-recommends git curl ffmpeg -qqy \
    && git clone https://github.com/galihmrd/tessdata vendor/data/tessdata \
    && apt install tesseract-ocr -y \
    && pip install -U -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

CMD python3 -m lib
