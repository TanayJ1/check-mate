from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(text1, text2):

    documents = [text1, text2]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0],
        tfidf_matrix[1]
    )

    return similarity[0][0]

if __name__ == "__main__":

    text1 = """
    Artificial intelligence is transforming the healthcare industry.
    Machine learning helps doctors diagnose diseases more accurately.
    """

    text2 = """
    Artificial intelligence is changing healthcare.
    Machine learning allows doctors to improve disease diagnosis.
    """

    score = calculate_similarity(text1, text2)

    print("Similarity:", score)