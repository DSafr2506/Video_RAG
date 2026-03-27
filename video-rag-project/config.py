from pathlib import Path

DEVICE = "cuda"
HOME_DIR = Path("data")
TRANSCRIPTS_PKL = HOME_DIR / "transcripts.pkl"
TEST_QUERIES = HOME_DIR / "test.csv"

EMBED_MODEL = "BAAI/bge-m3"
RERANK_MODEL = "BAAI/bge-reranker-large"

MAX_TOKENS = 80
OVERLAP = 30

RETRIEVE_TOPK = 200
FINAL_TOPK = 5

TEMPORAL_WINDOW = 6
