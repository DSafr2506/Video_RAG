#!/bin/bash

echo "🚀 Video RAG Setup Script"
echo "========================="
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Установите Python 3.8+"
    exit 1
fi

echo "✓ Python найден: $(python3 --version)"
echo ""

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
python3 -m venv venv

# Активация
echo "🔧 Активация окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Установка завершена!"
echo ""
echo "Для запуска проекта:"
echo "  1. Активируйте окружение: source venv/bin/activate"
echo "  2. Поместите данные в директорию data/"
echo "  3. Запустите: python main.py"
echo ""
