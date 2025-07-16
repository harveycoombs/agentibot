FROM nvidia/cuda:12.9.1-cudnn-devel-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    python3-pip python3-dev python3-venv git curl && \
    ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /src

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip

COPY src/ .
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "vesper.py"]