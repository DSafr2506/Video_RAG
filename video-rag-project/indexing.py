import faiss


class VectorIndex:
    def __init__(self, dimension, hnsw_m=32, ef_search=128):
        self.index = faiss.IndexHNSWFlat(dimension, hnsw_m)
        self.index.hnsw.efSearch = ef_search

    def add_vectors(self, vectors):
        self.index.add(vectors)

    def search(self, query_vectors, k):
        return self.index.search(query_vectors, k)

    @property
    def size(self):
        return self.index.ntotal
