from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity

from semantic_similarity import get_model


def load_submissions(folder):

    submissions = {}

    folder_path = Path(folder)

    for file_path in folder_path.glob("*.txt"):

        student_id = file_path.stem

        text = file_path.read_text(
            encoding="utf-8"
        )

        submissions[student_id] = text

    return submissions


def generate_embeddings(submissions):

    student_ids = list(submissions.keys())

    texts = list(submissions.values())

    embeddings = get_model().encode(texts)

    return student_ids, embeddings


def calculate_similarity_matrix(embeddings):

    return cosine_similarity(embeddings)


def find_suspicious_pairs(
    student_ids,
    similarity_matrix,
    threshold=0.70
):

    results = []

    n = len(student_ids)

    for i in range(n):

        for j in range(i + 1, n):

            score = similarity_matrix[i][j]

            if score >= threshold:

                results.append({
                    "student1": student_ids[i],
                    "student2": student_ids[j],
                    "similarity": float(score)
                })

    return results


def rank_results(results):

    return sorted(
        results,
        key=lambda x: x["similarity"],
        reverse=True
    )


if __name__ == "__main__":

    submissions = load_submissions(
        "submissions"
    )

    print(
        f"Loaded {len(submissions)} submissions"
    )

    student_ids, embeddings = generate_embeddings(
        submissions
    )

    similarity_matrix = calculate_similarity_matrix(
        embeddings
    )

    results = find_suspicious_pairs(
        student_ids,
        similarity_matrix,
        threshold=0.70
    )

    results = rank_results(results)

    print("\nSuspicious submissions:\n")

    for result in results:

        print(
            f"{result['student1']} <-> "
            f"{result['student2']} : "
            f"{result['similarity']:.2f}"
        )