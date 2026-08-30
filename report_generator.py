import json

from scoring import (
    calculate_combined_score,
    classify_similarity
)

from sentence_detector import (
    find_sentence_matches,
    split_into_sentences
)


def generate_report(
    student1,
    student2,
    text1,
    text2,
    tfidf_score,
    semantic_score
):

    final_score = calculate_combined_score(
        tfidf_score,
        semantic_score
    )

    risk = classify_similarity(
        final_score
    )

    matches = find_sentence_matches(
        text1,
        text2,
        threshold=0.75
    )

    sentences1 = split_into_sentences(text1)

    matching_ratio = (
        len(matches) / len(sentences1)
        if sentences1
        else 0
    )

    exact_matches = sum(
        1
        for match in matches
        if match["exact_match"]
    )

    report = {

        "student1": student1,

        "student2": student2,

        "tfidf_similarity": round(
            tfidf_score,
            3
        ),

        "semantic_similarity": round(
            semantic_score,
            3
        ),

        "final_score": round(
            final_score,
            3
        ),

        "matching_sentence_ratio": round(
            matching_ratio,
            3
        ),

        "risk": risk,

        "matching_sentences": len(matches),

        "exact_matches": exact_matches,

        "evidence": matches
    }

    return report


if __name__ == "__main__":

    text1 = """
    Machine learning helps doctors diagnose diseases.
    Artificial intelligence is transforming healthcare.
    Hospitals are adopting digital systems.
    """

    text2 = """
    Machine learning helps doctors diagnose diseases.
    AI is changing the healthcare industry.
    Doctors are using modern medical devices.
    """

    report = generate_report(
        "Alice",
        "Bob",
        text1,
        text2,
        0.72,
        0.89
    )

    print(
        json.dumps(
            report,
            indent=4
        )
    )