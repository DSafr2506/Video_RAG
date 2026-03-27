import pickle
import pandas as pd
from pathlib import Path


def validate_transcripts(path):
    print("Проверка transcripts.pkl...")
    
    try:
        with open(path, "rb") as f:
            transcripts = pickle.load(f)
        
        if not isinstance(transcripts, dict):
            print("❌ Транскрипты должны быть словарем")
            return False
        
        print(f"✓ Найдено {len(transcripts)} видео")
        
        for video_file, segments in transcripts.items():
            if not isinstance(segments, list):
                print(f"❌ Сегменты для {video_file} должны быть списком")
                return False
            
            for seg in segments:
                if not all(k in seg for k in ["text", "start", "end"]):
                    print(f"❌ Неверный формат сегмента в {video_file}")
                    return False
        
        print("✓ Формат транскриптов корректен")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при чтении: {e}")
        return False


def validate_video_topics(path):
    print("\nПроверка video_topic.csv...")
    
    try:
        df = pd.read_csv(path)
        
        required_cols = ["video_file", "topic"]
        if not all(col in df.columns for col in required_cols):
            print(f"❌ Требуются колонки: {required_cols}")
            return False
        
        print(f"✓ Найдено {len(df)} записей")
        print(f"✓ Уникальных топиков: {df['topic'].nunique()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при чтении: {e}")
        return False


def validate_test_queries(path):
    print("\nПроверка test_topic.csv...")
    
    try:
        df = pd.read_csv(path)
        
        required_cols = ["query_id", "question", "topic"]
        if not all(col in df.columns for col in required_cols):
            print(f"❌ Требуются колонки: {required_cols}")
            return False
        
        print(f"✓ Найдено {len(df)} запросов")
        print(f"✓ Уникальных топиков: {df['topic'].nunique()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при чтении: {e}")
        return False


def main():
    print("=" * 50)
    print("Валидация данных Video RAG")
    print("=" * 50)
    print()
    
    data_dir = Path("data")
    
    if not data_dir.exists():
        print("❌ Директория data/ не найдена")
        return
    
    results = []
    
    # Проверка транскриптов
    transcripts_path = data_dir / "transcripts.pkl"
    if transcripts_path.exists():
        results.append(validate_transcripts(transcripts_path))
    else:
        print("⚠️  transcripts.pkl не найден")
        results.append(False)
    
    # Проверка video_topic.csv
    video_topic_path = data_dir / "video_topic.csv"
    if video_topic_path.exists():
        results.append(validate_video_topics(video_topic_path))
    else:
        print("⚠️  video_topic.csv не найден")
        results.append(False)
    
    # Проверка test_topic.csv
    test_path = data_dir / "test_topic.csv"
    if test_path.exists():
        results.append(validate_test_queries(test_path))
    else:
        print("⚠️  test_topic.csv не найден")
        results.append(False)
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ Все проверки пройдены!")
    else:
        print("❌ Обнаружены ошибки в данных")
    print("=" * 50)


if __name__ == "__main__":
    main()
