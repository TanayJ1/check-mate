import os

from classroom_service import get_student_name

from drive_service import (
    get_file,
    download_file
)

from text_extractor import extract_text


DOWNLOAD_DIR = "downloads"


def process_submission(
    course_id,
    submission
):

    user_id = submission.get(
        "userId"
    )

    if not user_id:
        return None

    student_name = get_student_name(
        course_id,
        user_id
    )

    assignment_submission = submission.get(
        "assignmentSubmission"
    )

    if not assignment_submission:
        return None

    attachments = assignment_submission.get(
        "attachments",
        []
    )

    if not attachments:
        return None

    attachment = attachments[0]

    drive_file = attachment.get(
        "driveFile"
    )

    if not drive_file:
        return None

    file_id = drive_file.get(
        "id"
    )

    if not file_id:
        return None

    file_info = get_file(
        file_id
    )

    file_name = file_info["name"]

    mime_type = file_info["mimeType"]

    os.makedirs(
        DOWNLOAD_DIR,
        exist_ok=True
    )

    file_path = os.path.join(
        DOWNLOAD_DIR,
        file_name
    )

    download_file(
        file_id,
        file_path
    )

    text = extract_text(
        file_path,
        mime_type
    )

    return {
        "name": student_name,
        "text": text
    }

def process_assignment(
    course_id,
    coursework_id
):

    from classroom_service import get_submissions

    submissions = get_submissions(
        course_id,
        coursework_id
    )

    processed = []

    for submission in submissions:

        try:

            result = process_submission(
                course_id,
                submission
            )

            if result and result["text"].strip():

                processed.append(
                    result
                )

        except Exception as e:

            print(
                "Error processing submission:",
                e
            )

    return processed

if __name__ == "__main__":

    COURSE_ID = "736893952983"
    COURSEWORK_ID = "772366203215"  

    submissions = process_assignment(
        COURSE_ID,
        COURSEWORK_ID
    )

    for submission in submissions:

        print(
            "\nSTUDENT:",
            submission["name"]
        )

        print(
            "TEXT PREVIEW:"
        )

        print(
            submission["text"][:500]
        )