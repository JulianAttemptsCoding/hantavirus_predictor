# HantaST-PINN-FM: Production Docker Image
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3-pip python3.11-dev \
    git curl wget ca-certificates \
    libgdal-dev gdal-bin libgeos-dev \
    libproj-dev proj-data proj-bin \
    libffi-dev libssl-dev \
    build-essential gfortran \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

RUN pip install --no-cache-dir \
    torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 \
    --index-url https://download.pytorch.org/whl/cu124

RUN pip install --no-cache-dir \
    torch-geometric==2.5.3 \
    torch-scatter torch-sparse torch-cluster \
    -f https://data.pyg.org/whl/torch-2.3.0+cu124.html

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY tests/ ./tests/

COPY setup.py pyproject.toml ./
RUN pip install -e .

RUN mkdir -p outputs/checkpoints outputs/figures outputs/predictions outputs/logs

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import torch; print(torch.cuda.is_available())" || exit 1

CMD ["python", "scripts/train.py", "--config", "config/train_config.yaml"]
