from tqdm import tqdm
from chunking import expand_fragment


class VideoRetriever:
    def __init__(self, indexes, all_chunks, temporal_window=6):
        self.indexes = indexes
        self.all_chunks = all_chunks
        self.temporal_window = temporal_window

    def retrieve(self, topic, query_embeddings, retrieve_topk=200, final_topk=5):
        results = []
        scores, indices = self.indexes[topic].search(query_embeddings, retrieve_topk)

        for q_idx in range(len(query_embeddings)):
            cand_idx = indices[q_idx]

            candidates = []
            file_to_minmax = {}
            file_used = {}
            order = []

            for i in cand_idx:
                chunk = self.all_chunks[topic][i]
                expanded = expand_fragment(chunk, self.temporal_window)
                fl = expanded["video_file"]
                
                if fl not in file_to_minmax:
                    file_to_minmax[fl] = [10 ** 9, 0]
                    file_used[fl] = 0
                    
                if file_used[fl] < 2:
                    file_used[fl] += 1
                    file_to_minmax[fl][0] = min(file_to_minmax[fl][0], expanded["start"])
                    file_to_minmax[fl][1] = max(file_to_minmax[fl][1], expanded["end"])
                    
                if fl not in order:
                    order.append(fl)
                    
            order = order[:final_topk]

            for filename in order:
                candidates.append({
                    "video_file": filename, 
                    "start": file_to_minmax[filename][0], 
                    "end": file_to_minmax[filename][1]
                })

            results.append(candidates)

        return results
