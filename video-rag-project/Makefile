.PHONY: install test clean run help

help:
	@echo "Доступные команды:"
	@echo "  make install  - Установить зависимости"
	@echo "  make test     - Запустить тесты"
	@echo "  make run      - Запустить основной скрипт"
	@echo "  make clean    - Очистить временные файлы"

install:
	pip install -r requirements.txt

test:
	cd tests && python test_chunking.py

run:
	python main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
