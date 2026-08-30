from submission_processor import process_assignment

from batch_processor import (
    process_submissions,
    save_reports
)


COURSE_ID = "736893952983"
COURSEWORK_ID = "736896450760"


def run():

    print(
        "Fetching submissions..."
    )

    submissions = process_assignment(
        COURSE_ID,
        COURSEWORK_ID
    )

    print(
        f"Found {len(submissions)} submissions."
    )

    if len(submissions) < 2:

        print(
            "Not enough submissions to compare."
        )

        return

    print(
        "Running plagiarism detection..."
    )

    reports = process_submissions(
        submissions
    )

    save_reports(
        reports
    )

    print(
        f"Generated {len(reports)} comparison reports."
    )


if __name__ == "__main__":

    run()