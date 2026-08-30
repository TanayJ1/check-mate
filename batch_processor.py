import json
import os

from itertools import combinations

from plagiarism import calculate_similarity
from semantic_similarity import calculate_semantic_similarity
from report_generator import generate_report


def process_submissions(submissions):

    reports = []

    for student1, student2 in combinations(
        submissions,
        2
    ):

        print(
            f"Comparing "
            f"{student1['name']} "
            f"vs "
            f"{student2['name']}"
        )

        tfidf_score = float(
            calculate_similarity(
                student1["text"],
                student2["text"]
            )
        )

        semantic_score = float(
            calculate_semantic_similarity(
                student1["text"],
                student2["text"]
            )
        )

        report = generate_report(
            student1["name"],
            student2["name"],
            student1["text"],
            student2["text"],
            tfidf_score,
            semantic_score
        )

        reports.append(report)

    return reports


def save_reports(reports):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    with open(
        "reports/plagiarism_report.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            reports,
            file,
            indent=4
        )

if __name__ == "__main__":

    submissions = [

        {
            "name": "Alice",
            "text": """
            Machine learning helps doctors
            diagnose diseases.
            Artificial intelligence is
            transforming healthcare.
            """
        },

        {
            "name": "Bob",
            "text": """
            Machine learning helps doctors
            diagnose diseases.
            AI is changing the healthcare
            industry.
            """
        },

        {
            "name": "Charlie",
            "text": """
            Football is one of the most
            popular sports in the world.
            """
        }
    ]

    reports = process_submissions(
        submissions
    )

    save_reports(
        reports
    )

    print(
        "\nReports generated successfully!"
    )