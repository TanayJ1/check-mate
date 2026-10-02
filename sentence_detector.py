from sklearn.metrics.pairwise import cosine_similarity
import re

from semantic_similarity import get_model


def split_into_sentences(text):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def normalize_sentence(sentence):

    sentence = sentence.lower()

    sentence = re.sub(
        r'[^\w\s]',
        '',
        sentence
    )

    sentence = re.sub(
        r'\s+',
        ' ',
        sentence
    )

    return sentence.strip()


def is_exact_match(sentence1, sentence2):

    return (
        normalize_sentence(sentence1)
        ==
        normalize_sentence(sentence2)
    )


def find_sentence_matches(
    text1,
    text2,
    threshold=0.75
):

    sentences1 = split_into_sentences(text1)
    sentences2 = split_into_sentences(text2)

    if not sentences1 or not sentences2:
        return []

    model = get_model()
    embeddings1 = model.encode(sentences1)
    embeddings2 = model.encode(sentences2)

    similarity_matrix = cosine_similarity(
        embeddings1,
        embeddings2
    )

    matches = []

    for i in range(len(sentences1)):

        best_match_index = similarity_matrix[i].argmax()

        best_score = similarity_matrix[
            i
        ][best_match_index]

        if best_score >= threshold:

            matches.append({
                "sentence1": sentences1[i],
                "sentence2": sentences2[best_match_index],
                "similarity": float(best_score),
                "exact_match": is_exact_match(
                    sentences1[i],
                    sentences2[best_match_index]
                )
            })

    return matches


if __name__ == "__main__":

    text1 = """
    Artificial intelligence is transforming healthcare.
    Machine learning helps doctors diagnose diseases.
    Hospitals are adopting digital systems.
    """

    text2 = """
    Healthcare technology is evolving rapidly.
    Machine learning helps doctors diagnose diseases.
    Doctors are using new medical devices.
    """

    matches = find_sentence_matches(
        text1,
        text2,
        threshold=0.75
    )

    for match in matches:

        print("\nMatch found:")

        print(
            "Student 1:",
            match["sentence1"]
        )

        print(
            "Student 2:",
            match["sentence2"]
        )

        print(
            "Similarity:",
            f"{match['similarity']:.2f}"
        )