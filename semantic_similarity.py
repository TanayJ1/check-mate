
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


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