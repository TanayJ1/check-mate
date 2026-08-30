def calculate_combined_score(
    tfidf_score,
    semantic_score
):

    score = (
        0.30 * tfidf_score +
        0.70 * semantic_score
    )

    return score


def classify_similarity(score):

    if score >= 0.80:
        return "HIGH"

    elif score >= 0.60:
        return "REVIEW"

    else:
        return "LOW"


if __name__ == "__main__":

    test_cases = [
        (0.90, 0.95),
        (0.60, 0.75),
        (0.20, 0.30)
    ]

    for tfidf, semantic in test_cases:

        score = calculate_combined_score(
            tfidf,
            semantic
        )

        category = classify_similarity(score)

        print(
            f"TF-IDF: {tfidf:.2f} | "
            f"Semantic: {semantic:.2f} | "
            f"Final: {score:.2f} | "
            f"Category: {category}"
        )