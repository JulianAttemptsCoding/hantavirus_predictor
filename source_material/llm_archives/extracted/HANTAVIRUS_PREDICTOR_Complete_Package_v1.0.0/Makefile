.PHONY: help install test lint format docker train eval deploy clean

help:
	@echo "HantaST-PINN-FM - Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run unit tests"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make docker     - Build Docker image"
	@echo "  make train      - Run training pipeline"
	@echo "  make eval       - Run evaluation"
	@echo "  make deploy     - Start inference API"
	@echo "  make clean      - Clean generated files"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=src --cov-report=term --cov-report=html

lint:
	flake8 src/ tests/ scripts/ --max-line-length=100
	mypy src/ --ignore-missing-imports

format:
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

docker:
	docker build -t hantavirus-predictor:latest .

train:
	python scripts/train.py --config config/train_config.yaml --gpus 4

eval:
	python scripts/evaluate.py \
		--config config/train_config.yaml \
		--checkpoint outputs/checkpoints/hantast_pinn_fm_final.ckpt \
		--run_ablation

deploy:
	python scripts/deploy.py \
		--model_path outputs/checkpoints/hantast_pinn_fm_final.ckpt \
		--port 8000

clean:
	rm -rf outputs/checkpoints/* outputs/figures/* outputs/predictions/*
	rm -rf .pytest_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
