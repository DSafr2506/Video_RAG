import torch
import pandas as pd
from tqdm import tqdm

from config import *
from data_loader import load_transcripts, load_video_topics, load_test_queries
from chunking import build_chunks
from embeddings import EmbeddingModel
from indexing import VectorIndex
from retriever import VideoRetriever


def prepare_chunks(transcripts, video_to_topic):
    all_chunks = {}
    total_chunks = 0

    for video_file, segments in tqdm(transcripts.items(), desc="Building chunks"):
        if len(segments) == 0:
            continue
            
        topic = video_to_topic.get(video_file.split('.')[0])
        if not topic:
            continue
            
        if topic not in all_chunks:
            all_chunks[topic] = []

        chunks = build_chunks(segments, MAX_TOKENS, OVERLAP)
        total_chunks += len(chunks)

        for ch in chunks:
            all_chunks[topic].append({
                "video_file": video_file,
                "start": ch["start"],
                "end": ch["end"],
                "text": ch["text"]
            })

    print(f"Total chunks: {total_chunks}")
    return all_chunks


def build_indexes(all_chunks, embedding_model):
    chunk_embeddings = {}
    indexes = {}

    for topic in all_chunks.keys():
        chunk_texts = [c["text"] for c in all_chunks[topic]]
        chunk_embeddings[topic] = embedding_model.embed_texts(chunk_texts)

        dim = chunk_embeddings[topic].shape[1]
        index = VectorIndex(dim)
        index.add_vectors(chunk_embeddings[topic])
        indexes[topic] = index

        print(f"Index for topic '{topic}': {index.size} vectors")

    return indexes


def generate_submission(results, query_ids, output_path="submission.csv"):
    submission = []
    
    for qid, res in zip(query_ids, results):
        row = {"query_id": qid}

        for rank in range(FINAL_TOPK):
            if rank >= len(res):
                r = {"video_file": "", "start": 0, "end": 0}
            else:
                r = res[rank]

            row[f"video_file_{rank+1}"] = r["video_file"][7:].split('.')[0]
            row[f"start_{rank+1}"] = r["start"]
            row[f"end_{rank+1}"] = r["end"]

        submission.append(row)

    submission_df = pd.DataFrame(submission)
    submission_df.to_csv(output_path, index=False)
    print(f"Submission saved to {output_path}")


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    print("Loading data...")
    transcripts = load_transcripts(TRANSCRIPTS_PKL)
    video_to_topic = load_video_topics("data/video_topic.csv")
    test_df = load_test_queries("data/test_topic.csv")

    print(f"Loaded {len(transcripts)} videos")

    all_chunks = prepare_chunks(transcripts, video_to_topic)

    print("Initializing embedding model...")
    embedding_model = EmbeddingModel(EMBED_MODEL, device)

    print("Building indexes...")
    indexes = build_indexes(all_chunks, embedding_model)

    print("Processing queries...")
    retriever = VideoRetriever(indexes, all_chunks, TEMPORAL_WINDOW)
    
    all_results = []
    all_query_ids = []

    for topic in tqdm(all_chunks.keys(), desc="Processing topics"):
        topic_queries = test_df[test_df.topic == topic]
        queries = topic_queries["question"].tolist()
        query_ids = topic_queries["query_id"].tolist()

        if len(queries) == 0:
            continue

        query_embeddings = embedding_model.embed_texts(queries)
        results = retriever.retrieve(topic, query_embeddings, RETRIEVE_TOPK, FINAL_TOPK)

        all_results.extend(results)
        all_query_ids.extend(query_ids)

    print("Generating submission...")
    generate_submission(all_results, all_query_ids)

    print("Done!")


if __name__ == "__main__":
    main()
