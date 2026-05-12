FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

WORKDIR /workspace
COPY environment.yml .
RUN conda env update -n base -f environment.yml && conda clean -afy

COPY . .
RUN pip install -e .

ENV PYTHONPATH=/workspace/src
ENV CUDA_VISIBLE_DEVICES=0

CMD ["python", "scripts/train.py", "config=default"]
