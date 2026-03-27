# Быстрый старт 🚀

## За 5 минут

### 1. Установка (1 мин)
```bash
./setup.sh
```

### 2. Подготовка данных (2 мин)
Скопируйте файлы в `data/`:
- `transcripts.pkl`
- `video_topic.csv`
- `test_topic.csv`

### 3. Проверка данных (30 сек)
```bash
python validate_data.py
```

### 4. Запуск (1-2 мин)
```bash
python main.py
```

### 5. Результат
Файл `submission.csv` готов! 🎉

## Альтернативный способ

С использованием Make:
```bash
make install
make run
```

## Что дальше?

- Настройте параметры в `config.py`
- Изучите примеры в `EXAMPLES.md`
- Прочитайте FAQ в `FAQ.md`

## Проблемы?

1. Проверьте версию Python: `python --version` (нужен 3.8+)
2. Убедитесь, что данные в правильном формате
3. Посмотрите логи ошибок
4. Создайте issue на GitHub

Удачи! 🍀
