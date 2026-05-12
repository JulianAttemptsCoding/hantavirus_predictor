.PHONY: install test lint format docker clean reproduce

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

docker:
	docker build -t hanta-pinn-st:latest .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

reproduce:
	@echo "Reproducing full pipeline..."
	python src/data/ingest.py
	python src/data/process.py
	python src/data/split.py
	python scripts/train.py --config configs/train/pretrain.yaml
	pytest tests/ --tb=short
