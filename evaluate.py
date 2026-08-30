from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from evaluation_data import evaluation_pairs
from semantic_similarity import calculate_semantic_similarity
from plagiarism import calculate_similarity
from scoring import calculate_combined_score


def predict(text1, text2):

    tfidf_score = calculate_similarity(
        text1,
        text2
    )

    semantic_score = calculate_semantic_similarity(
        text1,
        text2
    )

    final_score = calculate_combined_score(
        tfidf_score,
        semantic_score
    )

    prediction = 1 if final_score >= 0.70 else 0

    return prediction