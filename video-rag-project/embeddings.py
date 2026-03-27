import torch
import numpy as np
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel


class EmbeddingModel:
    def __init__(self, model_name, device="cuda"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(device).eval()

    def embed_texts(self, texts, batch_size=32):
        embeddings = []

        for i in tqdm(range(0, len(texts), batch_size)):
            batch = texts[i:i+batch_size]

            inputs = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                return_tensors="pt",
                max_length=512
            ).to(self.device)

            with torch.no_grad():
                output = self.model(**inputs)
                emb = output.last_hidden_state[:,0]

            emb = torch.nn.functional.normalize(emb, dim=1)
            embeddings.append(emb.cpu().numpy())

        return np.vstack(embeddings)
