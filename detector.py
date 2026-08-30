from plagiarism import calculate_similarity
from semantic_similarity import calculate_semantic_similarity


def calculate_final_score(text1, text2):

    tfidf_score = calculate_similarity(text1, text2)

    semantic_score = calculate_semantic_similarity(text1, text2)

    final_score = (
        0.3 * tfidf_score +
        0.7 * semantic_score
    )

    return {
        "tfidf_score": tfidf_score,
        "semantic_score": semantic_score,
        "final_score": final_score
    }


if __name__ == "__main__":

    text1 = """
    Machine learning helps doctors identify diseases.
    """

    text2 = """
    Artificial intelligence assists physicians in detecting medical conditions.
    """

    result = calculate_final_score(text1, text2)

    print("TF-IDF score:", result["tfidf_score"])
    print("Semantic score:", result["semantic_score"])
    print("Final score:", result["final_score"])