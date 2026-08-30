def calculate_semantic_similarity(text1, text2):

    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(
        [text1, text2]
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )

    return similarity[0][0]


if __name__ == "__main__":

    text1 = """
    this is an apple
    """

    text2 = """
    Artificial intelligence assists physicians in detecting medical conditions.
    """

    score = calculate_semantic_similarity(
        text1,
        text2
    )

    print(
        "Semantic similarity:",
        score
    )