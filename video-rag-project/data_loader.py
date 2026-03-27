import pickle
import pandas as pd


def load_transcripts(path):
    with open(path, "rb") as f:
        transcripts = pickle.load(f)
    return transcripts


def load_video_topics(path):
    video_topic = pd.read_csv(path)
    video_to_topic = {}
    for _, row in video_topic.iterrows():
        video_to_topic[row["video_file"].split('.')[0]] = row["topic"]
    return video_to_topic


def load_test_queries(path):
    return pd.read_csv(path)
