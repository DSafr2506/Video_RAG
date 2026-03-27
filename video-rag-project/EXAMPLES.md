# Примеры использования

## Базовое использование

```python
from embeddings import EmbeddingModel
from indexing import VectorIndex

# Инициализация модели
model = EmbeddingModel("BAAI/bge-m3", device="cuda")

# Создание эмбеддингов
texts = ["Пример текста 1", "Пример текста 2"]
embeddings = model.embed_texts(texts)

# Создание индекса
index = VectorIndex(dimension=embeddings.shape[1])
index.add_vectors(embeddings)

# Поиск
query_embedding = model.embed_texts(["Запрос"])
scores, indices = index.search(query_embedding, k=5)
```

## Работа с чанками

```python
from chunking import build_chunks

segments = [
    {"text": "Первый сегмент", "start": 0, "end": 5},
    {"text": "Второй сегмент", "start": 5, "end": 10},
]

chunks = build_chunks(segments, max_tokens=80, overlap=30)
```

## Полный пайплайн

```python
from main import main

# Запуск всего пайплайна
main()
```

## Настройка параметров

```python
from config import *

# Изменение параметров
MAX_TOKENS = 100
OVERLAP = 40
RETRIEVE_TOPK = 300
```
