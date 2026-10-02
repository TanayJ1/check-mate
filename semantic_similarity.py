from functools import lru_cache

import numpy as np
from fastembed import TextEmbedding
from sklearn.metrics.pairwise import cosine_similarity

class _Model:
    def __init__(self):
        self._m = TextEmbedding(
            "sentence-transformers/all-MiniLM-L6-v2",
            cache_dir="models",
            threads=1,
        )

    def encode(self, texts, **kwargs):
        single = isinstance(texts, str)
        if single:
            texts = [texts]
        texts = [t[:3000] for t in texts]  # cap very long inputs
        out = np.array(list(self._m.embed(texts, batch_size=8)))
        return out[0] if single else out


@lru_cache(maxsize=1)
def get_model():
    return _Model()


def calculate_semantic_similarity(text1, text2):
    model = get_model()

    embeddings = model.encode([text1, text2])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )

    return float(similarity[0][0])


if __name__ == "__main__":
    text1 = "this is an apple"

    text2 = (
        "Artificial intelligence assists physicians "
        "in detecting medical conditions."
    )

    score = calculate_semantic_similarity(text1, text2)

    print("Semantic similarity:", score)